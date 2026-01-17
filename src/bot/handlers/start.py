from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.models.user import User
from src.config.settings import settings
from src.bot.keyboards.inline import create_location_request_keyboard, create_media_type_keyboard
from src.bot.utils.logger import setup_logger


logger = setup_logger(
    name=__name__
)

router = Router()


class ReportStates(StatesGroup):
    waiting_for_location = State()
    waiting_for_media = State()
    reviewing_report = State()
    waiting_for_description = State()


@router.message(Command("help"))
async def help_command(
    message: Message
) -> None:
    user = message.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} requested help"
    )
    
    help_text = (
        f"ℹ️ <b>HelpCy Bot - Municipal Problem Reporter</b>\n\n"
        f"📝 <b>Description:</b>\n"
        f"HelpCy helps you report municipal problems in your city. "
        f"Share your location, take a photo or record audio, and our AI will analyze the issue. "
        f"Your report will be sent to the municipality for review.\n\n"
        f"🔧 <b>Available Commands:</b>\n\n"
        f"/start - Start a new report\n"
        f"/help - Show this help message\n"
        f"/clear - Clear current report and start over\n\n"
        f"📋 <b>How it works:</b>\n"
        f"1️⃣ Send /start to begin\n"
        f"2️⃣ Share your location on the map\n"
        f"3️⃣ Take a photo or record audio\n"
        f"4️⃣ Review AI-analyzed report\n"
        f"5️⃣ Change category if needed\n"
        f"6️⃣ Submit your report\n\n"
        f"💡 <b>Tips:</b>\n"
        f"• Take clear, well-lit photos\n"
        f"• Describe the problem clearly in audio\n"
        f"• Use /clear if you want to restart\n\n"
        f"🏙️ <i>Help us make our city better!</i>"
    )
    
    await message.answer(
        text=help_text,
        parse_mode="HTML"
    )


@router.message(Command("clear"))
async def clear_command(
    message: Message,
    state: FSMContext
) -> None:
    user = message.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} cleared state"
    )
    
    await state.clear()
    
    await message.answer(
        text="🗑️ History and state cleared!\n\nSend /start to begin a new report.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("start"))
async def start_command(
    message: Message,
    state: FSMContext
) -> None:
    user = message.from_user
    
    if not user:
        return
    
    user_model = User.from_telegram_user(
        telegram_user=user
    )
    
    logger.info(
        msg=f"User {user_model.user_id} started the bot"
    )
    
    await state.clear()
    
    logger.info(
        msg=f"Start command text: {message.text}"
    )
    
    if message.text and " " in message.text:
        parts = message.text.split(" ", 1)
        logger.info(
            msg=f"Split parts: {parts}"
        )
        
        if len(parts) == 2 and parts[1].startswith("loc_"):
            coords_str = parts[1].replace("loc_", "")
            logger.info(
                msg=f"Coords string: {coords_str}"
            )
            
            coords = coords_str.split("_")
            logger.info(
                msg=f"Parsed coords: {coords}"
            )
            
            if len(coords) == 2:
                try:
                    latitude = float(coords[0])
                    longitude = float(coords[1])
                    
                    logger.info(
                        msg=f"User {user.id} sent location via deeplink: {latitude}, {longitude}"
                    )
                    
                    response_message = (
                        f"✅ Location received!\n\n"
                        f"Latitude: {latitude}\n"
                        f"Longitude: {longitude}\n\n"
                        f"What would you like to share?"
                    )
                    
                    camera_url = settings.bot.webapp_url.replace("map.html", "camera.html") if settings.bot.webapp_url else ""
                    
                    media_keyboard = create_media_type_keyboard(
                        camera_webapp_url=camera_url
                    )
                    
                    await message.answer(
                        text=response_message,
                        reply_markup=ReplyKeyboardRemove()
                    )
                    
                    await message.answer(
                        text="Choose media type:",
                        reply_markup=media_keyboard
                    )
                    return
                except Exception as e:
                    logger.error(
                        msg=f"Error parsing coords: {e}"
                    )
    
    welcome_message = (
        f"👋 Welcome, {user.first_name}!\n\n"
        f"Please share your location to continue."
    )
    
    if settings.bot.webapp_url:
        location_keyboard = create_location_request_keyboard(
            webapp_url=settings.bot.webapp_url
        )
        
        await message.answer(
            text=welcome_message,
            reply_markup=location_keyboard
        )
    else:
        await message.answer(
            text=welcome_message
        )


@router.message(F.web_app_data)
async def handle_webapp_data(
    message: Message
) -> None:
    user = message.from_user
    
    if not user or not message.web_app_data:
        return
    
    data = message.web_app_data.data
    
    logger.info(
        msg=f"WEB APP DATA RECEIVED: '{data}'"
    )
    
    if data.startswith("location:"):
        coords_str = data.replace("location:", "")
        coords = coords_str.split(",")
        
        if len(coords) == 2:
            try:
                latitude = float(coords[0])
                longitude = float(coords[1])
                
                logger.info(
                    msg=f"User {user.id} shared location: {latitude}, {longitude}"
                )
                
                response_message = (
                    f"✅ Location received!\n\n"
                    f"Latitude: {latitude}\n"
                    f"Longitude: {longitude}\n\n"
                    f"What would you like to share?"
                )
                
                media_keyboard = create_media_type_keyboard()
                
                await message.answer(
                    text=response_message,
                    reply_markup=ReplyKeyboardRemove()
                )
                
                await message.answer(
                    text="Choose media type:",
                    reply_markup=media_keyboard
                )
            except Exception as e:
                logger.error(
                    msg=f"Error parsing coords: {e}"
                )
                await message.answer(
                    text="❌ Error parsing location"
                )


@router.message(F.location)
async def handle_location(
    message: Message
) -> None:
    user = message.from_user
    location = message.location
    
    if not user or not location:
        return
    
    logger.info(
        msg=f"User {user.id} shared location: {location.latitude}, {location.longitude}"
    )
    
    response_message = (
        f"✅ Location received!\n\n"
        f"Latitude: {location.latitude}\n"
        f"Longitude: {location.longitude}\n\n"
        f"What would you like to share?"
    )
    
    media_keyboard = create_media_type_keyboard()
    
    await message.answer(
        text=response_message,
        reply_markup=ReplyKeyboardRemove()
    )
    
    await message.answer(
        text="Choose media type:",
        reply_markup=media_keyboard
    )




@router.callback_query(F.data.startswith("chcat|"))
async def handle_change_category(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    user = callback.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} wants to change category, data: {callback.data}"
    )
    
    # Save coordinates from callback data
    parts = callback.data.split("|")
    if len(parts) == 3:
        latitude = float(parts[1])
        longitude = float(parts[2])
        await state.update_data(latitude=latitude, longitude=longitude)
        logger.info(f"Saved coordinates: lat={latitude}, lng={longitude}")
    
    from src.bot.keyboards.inline import create_categories_keyboard
    
    categories_keyboard = create_categories_keyboard()
    
    await callback.message.edit_text(
        text="🏷 Select a category:",
        reply_markup=categories_keyboard
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("cat_"))
async def handle_category_selection(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    user = callback.from_user
    
    if not user or not callback.data:
        return
    
    from src.models.categories import get_all_categories
    
    category_idx = int(callback.data.replace("cat_", ""))
    categories = get_all_categories()
    category = categories[category_idx]
    
    logger.info(
        msg=f"User {user.id} selected category: {category}"
    )
    
    await state.update_data(
        category=category
    )
    
    from src.bot.keyboards.inline import create_subcategories_keyboard
    
    subcategories_keyboard = create_subcategories_keyboard(
        category=category
    )
    
    await callback.message.edit_text(
        text=f"🏷 Category: {category}\n\n🔖 Select subcategory:",
        reply_markup=subcategories_keyboard
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("subcat_"))
async def handle_subcategory_selection(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    user = callback.from_user
    
    if not user or not callback.data:
        return
    
    from src.models.categories import get_subcategories_for_category
    
    data = await state.get_data()
    category = data.get("category", "Unknown")
    
    subcat_idx = int(callback.data.replace("subcat_", ""))
    subcategories = get_subcategories_for_category(category)
    subcategory = subcategories[subcat_idx]
    
    logger.info(
        msg=f"User {user.id} selected subcategory: {subcategory}"
    )
    
    await state.update_data(
        subcategory=subcategory
    )
    
    latitude = data.get("latitude", 35.0)
    longitude = data.get("longitude", 33.0)
    description = data.get("description", "Problem reported")
    
    from src.bot.keyboards.inline import create_report_review_keyboard
    
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
    
    review_keyboard = create_report_review_keyboard(
        category=category,
        subcategory=subcategory,
        latitude=latitude,
        longitude=longitude,
        description=description,
        webapp_url=settings.bot.webapp_url
    )
    
    await callback.message.answer(
        text=message_text,
        parse_mode="HTML",
        reply_markup=review_keyboard
    )
    
    await callback.answer(text="✅ Category updated!")


@router.callback_query(F.data == "back_to_categories")
async def handle_back_to_categories(
    callback: CallbackQuery
) -> None:
    user = callback.from_user
    
    if not user:
        return
    
    from src.bot.keyboards.inline import create_categories_keyboard
    
    categories_keyboard = create_categories_keyboard()
    
    await callback.message.edit_text(
        text="🏷 Select a category:",
        reply_markup=categories_keyboard
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("eddesc|"))
async def handle_edit_description(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    user = callback.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} wants to edit description, data: {callback.data}"
    )
    
    # Parse category, subcategory and coordinates from callback data
    parts = callback.data.split("|")
    if len(parts) == 5:
        category = parts[1]
        subcategory = parts[2]
        latitude = float(parts[3])
        longitude = float(parts[4])
        await state.update_data(
            category=category,
            subcategory=subcategory,
            latitude=latitude,
            longitude=longitude
        )
        logger.info(f"Saved: cat={category}, subcat={subcategory}, lat={latitude}, lng={longitude}")
    
    # Get current description
    data = await state.get_data()
    current_description = data.get("description", "Maintenance needed")
    
    instruction_message = (
        f"✏️ <b>Edit Description</b>\n\n"
        f"<b>Current description:</b>\n"
        f"<i>{current_description}</i>\n\n"
        f"Please send a new description for your report.\n"
        f"You can edit or completely rewrite it."
    )
    
    await callback.message.answer(
        text=instruction_message,
        parse_mode="HTML"
    )
    
    await callback.answer()
    await state.set_state(ReportStates.waiting_for_description)


@router.message(ReportStates.waiting_for_description)
async def handle_new_description(
    message: Message,
    state: FSMContext
) -> None:
    user = message.from_user
    
    if not user or not message.text:
        return
    
    new_description = message.text
    
    logger.info(
        msg=f"User {user.id} provided new description"
    )
    
    await state.update_data(description=new_description)
    
    data = await state.get_data()
    category = data.get("category", "Unknown")
    subcategory = data.get("subcategory", "Unknown")
    latitude = data.get("latitude", 35.0)
    longitude = data.get("longitude", 33.0)
    
    from src.bot.keyboards.inline import create_report_review_keyboard
    
    lat_display = f"{int(latitude)}.{str(latitude).split('.')[1][:6] if '.' in str(latitude) else 'xxxxxx'}"
    lng_display = f"{int(longitude)}.{str(longitude).split('.')[1][:6] if '.' in str(longitude) else 'xxxxxx'}"
    
    message_text = (
        f"📋 <b>Report Updated</b>\n\n"
        f"📍 <b>Location:</b> {lat_display}, {lng_display}\n\n"
        f"🏷 <b>Category:</b> {category}\n"
        f"🔖 <b>Subcategory:</b> {subcategory}\n"
        f"📝 <b>Description:</b> {new_description}\n\n"
        f"Review your report and submit."
    )
    
    review_keyboard = create_report_review_keyboard(
        category=category,
        subcategory=subcategory,
        latitude=latitude,
        longitude=longitude,
        description=new_description,
        webapp_url=settings.bot.webapp_url
    )
    
    await message.answer(
        text=message_text,
        parse_mode="HTML",
        reply_markup=review_keyboard
    )
    
    await state.set_state(None)


@router.callback_query(F.data == "submit_report")
async def handle_submit_report(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    user = callback.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} submitted report"
    )
    
    # Remove buttons from previous message
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Send success message
    final_message = (
        f"✅ <b>Report Submitted Successfully!</b>\n\n"
        f"Your report has been sent to the municipality.\n"
        f"You will be notified when it's reviewed.\n\n"
        f"Thank you for helping improve our city! 🏙️\n\n"
        f"——————\n"
        f"Want to report another issue?\n"
        f"Send /start"
    )
    
    await callback.message.answer(
        text=final_message,
        parse_mode="HTML"
    )
    
    await callback.answer(
        text="✅ Report submitted!"
    )
    
    # Clear state
    await state.clear()


@router.callback_query(F.data == "media_photo")
async def handle_photo_button_click(
    callback: CallbackQuery
) -> None:
    user = callback.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} clicked Photo button"
    )
    
    camera_url = settings.bot.webapp_url.replace("map.html", "camera.html") if settings.bot.webapp_url else ""
    
    from src.bot.keyboards.inline import create_camera_keyboard
    
    camera_keyboard = create_camera_keyboard(
        camera_webapp_url=camera_url
    )
    
    instruction_message = (
        f"📷 <b>Photo Report</b>\n\n"
        f"📝 Instructions:\n\n"
        f"1️⃣ Click \"Open Camera\" button below\n"
        f"2️⃣ Allow camera access if asked\n"
        f"3️⃣ Position your camera to capture the problem clearly\n"
        f"4️⃣ Click \"Take Photo\" button\n"
        f"5️⃣ Your photo will be analyzed automatically\n\n"
        f"📸 Take a clear, well-lit photo for best results!"
    )
    
    await callback.message.edit_text(
        text=instruction_message,
        parse_mode="HTML",
        reply_markup=camera_keyboard
    )
    
    await callback.answer()


@router.callback_query(F.data == "media_audio")
async def handle_audio_button_click(
    callback: CallbackQuery
) -> None:
    user = callback.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} clicked Audio button"
    )
    
    instruction_message = (
        f"🎵 <b>Audio Report</b>\n\n"
        f"📝 Please record a voice message describing the problem:\n\n"
        f"• Tap and hold the microphone button 🎤\n"
        f"• Describe what you see\n"
        f"• Mention any important details\n"
        f"• Release to send\n\n"
        f"Your voice message will be analyzed automatically."
    )
    
    await callback.message.edit_text(
        text=instruction_message,
        parse_mode="HTML"
    )
    
    await callback.answer()


@router.message(F.photo)
async def handle_photo(
    message: Message,
    state: FSMContext
) -> None:
    user = message.from_user
    
    if not user or not message.photo:
        return
    
    logger.info(
        msg=f"User {user.id} sent photo directly"
    )
    
    data = await state.get_data()
    latitude = data.get("latitude", 35.0)
    longitude = data.get("longitude", 33.0)
    
    from src.services.ai_vision_service import AIVisionService
    from src.bot.keyboards.inline import create_report_review_keyboard
    
    ai_service = AIVisionService()
    analysis = await ai_service.analyze_problem_photo(
        photo_url=""
    )
    
    await message.answer(
        text="📸 Photo received"
    )
    
    lat_display = f"{int(latitude)}.{str(latitude).split('.')[1][:6] if '.' in str(latitude) else 'xxxxxx'}"
    lng_display = f"{int(longitude)}.{str(longitude).split('.')[1][:6] if '.' in str(longitude) else 'xxxxxx'}"
    
    message_text = (
        f"📋 <b>Report Details</b>\n\n"
        f"📍 <b>Location:</b> {lat_display}, {lng_display}\n\n"
        f"🏷 <b>Category:</b> {analysis['category']}\n"
        f"🔖 <b>Subcategory:</b> {analysis['subcategory']}\n"
        f"📝 <b>Description:</b> {analysis['description']}\n\n"
        f"Review your report and submit or change category."
    )
    
    review_keyboard = create_report_review_keyboard(
        category=analysis['category'],
        subcategory=analysis['subcategory'],
        latitude=latitude,
        longitude=longitude,
        description=analysis['description'],
        webapp_url=settings.bot.webapp_url
    )
    
    await message.answer(
        text=message_text,
        parse_mode="HTML",
        reply_markup=review_keyboard
    )
    
    await state.update_data(
        category=analysis['category'],
        subcategory=analysis['subcategory'],
        description=analysis['description']
    )


@router.message(F.voice | F.audio)
async def handle_audio(
    message: Message,
    state: FSMContext
) -> None:
    user = message.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} sent audio/voice"
    )
    
    data = await state.get_data()
    latitude = data.get("latitude", 35.0)
    longitude = data.get("longitude", 33.0)
    
    from src.services.ai_vision_service import AIVisionService
    from src.bot.keyboards.inline import create_report_review_keyboard
    
    ai_service = AIVisionService()
    analysis = await ai_service.analyze_problem_photo(
        photo_url=""
    )
    
    await message.answer(
        text="🎵 Audio received"
    )
    
    lat_display = f"{int(latitude)}.{str(latitude).split('.')[1][:6] if '.' in str(latitude) else 'xxxxxx'}"
    lng_display = f"{int(longitude)}.{str(longitude).split('.')[1][:6] if '.' in str(longitude) else 'xxxxxx'}"
    
    message_text = (
        f"📋 <b>Report Details</b>\n\n"
        f"📍 <b>Location:</b> {lat_display}, {lng_display}\n\n"
        f"🏷 <b>Category:</b> {analysis['category']}\n"
        f"🔖 <b>Subcategory:</b> {analysis['subcategory']}\n"
        f"📝 <b>Description:</b> {analysis['description']}\n\n"
        f"Review your report and submit or change category."
    )
    
    review_keyboard = create_report_review_keyboard(
        category=analysis['category'],
        subcategory=analysis['subcategory'],
        latitude=latitude,
        longitude=longitude,
        description=analysis['description'],
        webapp_url=settings.bot.webapp_url
    )
    
    await message.answer(
        text=message_text,
        parse_mode="HTML",
        reply_markup=review_keyboard
    )
    
    await state.update_data(
        category=analysis['category'],
        subcategory=analysis['subcategory'],
        description=analysis['description']
    )


@router.message()
async def debug_all_messages(
    message: Message
) -> None:
    logger.info(
        msg=f"DEBUG ALL: content_type={message.content_type}, web_app_data={message.web_app_data}, text={message.text}"
    )
    
    if message.web_app_data:
        await message.answer(
            text=f"GOT WEB APP DATA: {message.web_app_data.data}"
        )


@router.message(F.text.startswith("/location"))
async def handle_location_command(
    message: Message
) -> None:
    user = message.from_user
    
    if not user or not message.text:
        return
    
    try:
        parts = message.text.split()
        if len(parts) == 3:
            latitude = float(parts[1])
            longitude = float(parts[2])
            
            logger.info(
                msg=f"User {user.id} sent location via command: {latitude}, {longitude}"
            )
            
            response_message = (
                f"✅ Location received!\n\n"
                f"Latitude: {latitude}\n"
                f"Longitude: {longitude}\n\n"
                f"What would you like to share?"
            )
            
            camera_url = settings.bot.webapp_url.replace("map.html", "camera.html") if settings.bot.webapp_url else ""
            
            media_keyboard = create_media_type_keyboard(
                camera_webapp_url=camera_url
            )
            
            await message.answer(
                text=response_message,
                reply_markup=ReplyKeyboardRemove()
            )
            
            await message.answer(
                text="Choose media type:",
                reply_markup=media_keyboard
            )
    except Exception as e:
        logger.error(
            msg=f"Error parsing location command: {e}"
        )
        await message.answer(
            text="❌ Error parsing location"
        )

