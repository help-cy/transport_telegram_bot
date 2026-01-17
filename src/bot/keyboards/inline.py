from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Tuple


def create_location_request_keyboard(
    webapp_url: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="📍 Share My Location",
                web_app=WebAppInfo(
                    url=webapp_url
                )
            )
        ]
    ]
    
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def create_media_type_keyboard(
    camera_webapp_url: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="📷 Photo",
                callback_data="media_photo"
            ),
            InlineKeyboardButton(
                text="🎵 Audio",
                callback_data="media_audio"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def create_camera_keyboard(
    camera_webapp_url: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="📸 Open Camera",
                web_app=WebAppInfo(
                    url=camera_webapp_url
                )
            )
        ]
    ]
    
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def create_report_review_keyboard(
    category: str = "",
    subcategory: str = "",
    latitude: float = 0.0,
    longitude: float = 0.0,
    description: str = "",
    webapp_url: str = ""
) -> InlineKeyboardMarkup:
    from urllib.parse import quote
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Build edit description URL with parameters
    if webapp_url:
        base_url = webapp_url.rsplit('/', 1)[0]  # Remove map.html
        edit_url = f"{base_url}/edit_description.html?desc={quote(description)}&cat={quote(category)}&subcat={quote(subcategory)}&lat={latitude}&lng={longitude}"
        logger.info(f"Edit URL: {edit_url}")
    else:
        edit_url = ""
        logger.warning("No webapp_url provided!")
    
    keyboard = []
    
    # Change Category button
    keyboard.append([
        InlineKeyboardButton(
            text="🔄 Change Category",
            callback_data=f"chcat|{latitude}|{longitude}"
        )
    ])
    
    # Edit Description button - only add if webapp_url exists
    if edit_url:
        keyboard.append([
            InlineKeyboardButton(
                text="✏️ Edit Description",
                web_app=WebAppInfo(url=edit_url)
            )
        ])
    
    # Submit button
    keyboard.append([
        InlineKeyboardButton(
            text="✅ Submit",
            callback_data="submit_report"
        )
    ])
    
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def create_categories_keyboard() -> InlineKeyboardMarkup:
    from src.models.categories import get_all_categories
    
    categories = get_all_categories()
    keyboard = []
    
    for idx, category in enumerate(categories):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=category,
                    callback_data=f"cat_{idx}"
                )
            ]
        )
    
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def create_subcategories_keyboard(
    category: str
) -> InlineKeyboardMarkup:
    from src.models.categories import get_subcategories_for_category
    
    subcategories = get_subcategories_for_category(
        category=category
    )
    
    keyboard = []
    
    for idx, subcat in enumerate(subcategories):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=subcat,
                    callback_data=f"subcat_{idx}"
                )
            ]
        )
    
    keyboard.append(
        [
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data="back_to_categories"
            )
        ]
    )
    
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
