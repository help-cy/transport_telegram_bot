from aiogram import Router, F
from aiogram.types import Message

from src.bot.keyboards.reply import create_main_menu_keyboard, create_back_keyboard
from src.bot.utils.logger import setup_logger


logger = setup_logger(
    name=__name__
)

router = Router()


@router.message(F.text.lower().contains("help"))
async def handle_help_button(
    message: Message
) -> None:
    help_text = (
        "📋 *Help Section*\n\n"
        "Here you can find answers to common questions:\n\n"
        "• How to use this bot?\n"
        "• What features are available?\n"
        "• How to contact support?\n\n"
        "Use the back button to return to the main menu."
    )
    
    back_keyboard = create_back_keyboard()
    
    await message.answer(
        text=help_text,
        parse_mode="Markdown",
        reply_markup=back_keyboard
    )


@router.message(F.text.lower().contains("info"))
async def handle_info_button(
    message: Message
) -> None:
    info_text = (
        "ℹ️ *Information*\n\n"
        "Bot Name: HelpCy Bot\n"
        "Version: 1.0.0\n"
        "Last Updated: 2026-01-17\n\n"
        "This is a modern Telegram bot built with "
        "clean architecture principles."
    )
    
    back_keyboard = create_back_keyboard()
    
    await message.answer(
        text=info_text,
        parse_mode="Markdown",
        reply_markup=back_keyboard
    )


@router.message(F.text.lower().contains("settings"))
async def handle_settings_button(
    message: Message
) -> None:
    settings_text = (
        "⚙️ *Settings*\n\n"
        "Here you can configure your preferences:\n\n"
        "• Language: English\n"
        "• Notifications: Enabled\n"
        "• Theme: Default\n\n"
        "More settings coming soon!"
    )
    
    back_keyboard = create_back_keyboard()
    
    await message.answer(
        text=settings_text,
        parse_mode="Markdown",
        reply_markup=back_keyboard
    )


@router.message(F.text.lower().contains("back"))
async def handle_back_button(
    message: Message
) -> None:
    welcome_text = (
        "🏠 Back to Main Menu\n\n"
        "Choose an option from the menu below:"
    )
    
    main_keyboard = create_main_menu_keyboard()
    
    await message.answer(
        text=welcome_text,
        reply_markup=main_keyboard
    )


@router.message()
async def handle_other_messages(
    message: Message
) -> None:
    await message.answer(
        text="I don't understand that command. Try using the menu buttons!"
    )
