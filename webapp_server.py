from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import asyncio
import logging
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.route('/map.html')
def serve_map():
    return send_from_directory('webapp', 'map.html')

@app.route('/camera.html')
def serve_camera():
    return send_from_directory('webapp', 'camera.html')

@app.route('/edit_description.html')
def serve_edit_description():
    return send_from_directory('webapp', 'edit_description.html')

@app.route('/location', methods=['POST'])
def handle_location():
    data = request.json
    user_id = data.get('user_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    logger.info(f"Received location from user {user_id}: {latitude}, {longitude}")
    
    asyncio.run(send_to_telegram(user_id, latitude, longitude))
    
    return jsonify({'ok': True})

async def send_to_telegram(user_id, lat, lng):
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.storage.memory import MemoryStorage
    
    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Save location to FSM state
        state = FSMContext(storage=storage, key=f"user_{user_id}")
        await state.update_data(latitude=float(lat), longitude=float(lng))
        
        message_text = (
            f"✅ Location received!\n\n"
            f"Latitude: {lat}\n"
            f"Longitude: {lng}\n\n"
            f"What would you like to share?"
        )
        
        await bot.send_message(
            chat_id=user_id,
            text=message_text
        )
        
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📷 Photo", callback_data="media_photo"),
                    InlineKeyboardButton(text="🎵 Audio", callback_data="media_audio")
                ]
            ]
        )
        
        await bot.send_message(
            chat_id=user_id,
            text="Choose media type:",
            reply_markup=keyboard
        )
        
    finally:
        await bot.session.close()


async def save_photo_data_to_state(user_id, category, subcategory, description):
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.storage.memory import MemoryStorage
    
    storage = MemoryStorage()
    
    try:
        state = FSMContext(storage=storage, key=f"user_{user_id}")
        await state.update_data(
            category=category,
            subcategory=subcategory,
            description=description
        )
        logger.info(f"Saved to FSM: category={category}, subcategory={subcategory}")
    except Exception as e:
        logger.error(f"Error saving to FSM: {e}")


@app.route('/upload-photo', methods=['POST'])
def handle_photo_upload():
    import base64
    import requests
    import asyncio
    
    try:
        logger.info(f"Upload photo endpoint hit!")
        
        data = request.json
        user_id = data.get('user_id')
        photo_base64 = data.get('photo')
        latitude = data.get('latitude', 35.0)
        longitude = data.get('longitude', 33.0)
        
        logger.info(f"Received photo from user {user_id}, photo size: {len(photo_base64) if photo_base64 else 0}")
        logger.info(f"Location: {latitude}, {longitude}")
        
        if not photo_base64:
            logger.error("No photo data received!")
            return jsonify({'ok': False, 'error': 'No photo data'}), 400
        
        # Send processing message immediately
        processing_response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            json={
                'chat_id': user_id,
                'text': '🔄 <b>Processing image...</b>\n\nAI is analyzing your photo. This may take a few moments.',
                'parse_mode': 'HTML'
            },
            timeout=5
        )
        logger.info(f"Processing message sent: {processing_response.status_code}")
        
        # Real AI analysis with OpenAI Vision
        logger.info("Starting AI analysis with OpenAI Vision...")
        photo_data_url = f"data:image/jpeg;base64,{photo_base64}"
        
        from src.services.ai_vision_service import AIVisionService
        ai_service = AIVisionService()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        analysis = loop.run_until_complete(
            ai_service.analyze_problem_photo(photo_url=photo_data_url)
        )
        loop.close()
        
        category = analysis['category']
        subcategory = analysis['subcategory']
        description = analysis['description']
        
        logger.info(f"AI analysis: category={category}, subcategory={subcategory}, description={description[:50]}...")
        
        # Decode photo
        photo_bytes = base64.b64decode(photo_base64)
        logger.info(f"Photo decoded, size: {len(photo_bytes)} bytes")
        
        # Send photo to Telegram
        files = {'photo': ('photo.jpg', photo_bytes, 'image/jpeg')}
        photo_response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto',
            data={'chat_id': user_id, 'caption': '📸 Photo received'},
            files=files,
            timeout=10
        )
        
        logger.info(f"Photo sent response: {photo_response.status_code}, body: {photo_response.text[:200]}")
        
        # Send message with buttons
        lat_display = f"{int(latitude)}.{str(latitude).split('.')[1][:6] if '.' in str(latitude) else 'xxxxxx'}"
        lng_display = f"{int(longitude)}.{str(longitude).split('.')[1][:6] if '.' in str(longitude) else 'xxxxxx'}"
        
        message_text = (
            f"📋 <b>Report Details</b>\n\n"
            f"📍 <b>Location:</b> {lat_display}, {lng_display}\n\n"
            f"🏷 <b>Category:</b> {category}\n"
            f"🔖 <b>Subcategory:</b> {subcategory}\n"
            f"📝 <b>Description:</b> {description}\n\n"
            f"Review your report and submit or change category."
        )
        
        # Build edit description URL
        from urllib.parse import quote
        webapp_url = os.getenv("WEBAPP_URL", "")
        if webapp_url:
            base_url = webapp_url.rsplit('/', 1)[0]
            edit_url = f"{base_url}/edit_description.html?desc={quote(description)}&cat={quote(category)}&subcat={quote(subcategory)}&lat={latitude}&lng={longitude}"
            logger.info(f"Edit URL for upload-photo: {edit_url}")
        else:
            edit_url = ""
            logger.warning("No WEBAPP_URL in env!")
        
        keyboard_buttons = [
            [{"text": "🔄 Change Category", "callback_data": f"chcat|{latitude}|{longitude}"}],
            [{"text": "✅ Submit", "callback_data": "submit_report"}]
        ]
        
        # Add Edit Description button only if webapp_url exists
        if edit_url:
            keyboard_buttons.insert(1, [{"text": "✏️ Edit Description", "web_app": {"url": edit_url}}])
        
        keyboard = {"inline_keyboard": keyboard_buttons}
        
        logger.info(f"Sending message with buttons...")
        message_response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            json={
                'chat_id': user_id,
                'text': message_text,
                'parse_mode': 'HTML',
                'reply_markup': keyboard
            },
            timeout=10
        )
        
        logger.info(f"Message sent response: {message_response.status_code}, body: {message_response.text[:200]}")
        
        # Save to FSM state
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            save_photo_data_to_state(
                user_id=user_id,
                category=category,
                subcategory=subcategory,
                description=description
            )
        )
        loop.close()
        
        logger.info(f"Complete! category={category}, subcategory={subcategory}, lat={latitude}, lng={longitude}")
        
        return jsonify({'ok': True})
        
    except Exception as e:
        logger.error(f"Error in handle_photo_upload: {e}", exc_info=True)
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/update-description', methods=['POST'])
def handle_update_description():
    import requests
    
    try:
        logger.info("Update description endpoint hit!")
        
        data = request.json
        user_id = data.get('user_id')
        description = data.get('description')
        category = data.get('category')
        subcategory = data.get('subcategory')
        latitude = data.get('latitude', 0.0)
        longitude = data.get('longitude', 0.0)
        
        logger.info(f"User {user_id} updating description: {description[:50]}...")
        
        # Send updated report
        lat_display = f"{int(latitude)}.{str(latitude).split('.')[1][:6] if '.' in str(latitude) else 'xxxxxx'}"
        lng_display = f"{int(longitude)}.{str(longitude).split('.')[1][:6] if '.' in str(longitude) else 'xxxxxx'}"
        
        message_text = (
            f"📋 <b>Report Updated</b>\n\n"
            f"📍 <b>Location:</b> {lat_display}, {lng_display}\n\n"
            f"🏷 <b>Category:</b> {category}\n"
            f"🔖 <b>Subcategory:</b> {subcategory}\n"
            f"📝 <b>Description:</b> {description}\n\n"
            f"Review your report and submit."
        )
        
        # Build edit description URL
        from urllib.parse import quote
        webapp_url = os.getenv("WEBAPP_URL", "")
        if webapp_url:
            base_url = webapp_url.rsplit('/', 1)[0]
            edit_url = f"{base_url}/edit_description.html?desc={quote(description)}&cat={quote(category)}&subcat={quote(subcategory)}&lat={latitude}&lng={longitude}"
            logger.info(f"Edit URL for update-description: {edit_url}")
        else:
            edit_url = ""
            logger.warning("No WEBAPP_URL in env!")
        
        keyboard_buttons = [
            [{"text": "🔄 Change Category", "callback_data": f"chcat|{latitude}|{longitude}"}],
            [{"text": "✅ Submit", "callback_data": "submit_report"}]
        ]
        
        # Add Edit Description button only if webapp_url exists
        if edit_url:
            keyboard_buttons.insert(1, [{"text": "✏️ Edit Description", "web_app": {"url": edit_url}}])
        
        keyboard = {"inline_keyboard": keyboard_buttons}
        
        response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            json={
                'chat_id': user_id,
                'text': message_text,
                'parse_mode': 'HTML',
                'reply_markup': keyboard
            }
        )
        
        logger.info(f"Message sent: {response.status_code}")
        
        return jsonify({'ok': True})
        
    except Exception as e:
        logger.error(f"Error updating description: {e}", exc_info=True)
        return jsonify({'ok': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
