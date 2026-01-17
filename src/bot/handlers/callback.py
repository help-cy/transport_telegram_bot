from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.bot.utils.logger import setup_logger


logger = setup_logger(
    name=__name__
)

router = Router()


@router.callback_query(F.data == "get_started")
async def handle_get_started_callback(
    callback: CallbackQuery
) -> None:
    user = callback.from_user
    
    if not user:
        return
    
    logger.info(
        msg=f"User {user.id} clicked 'Get Started'"
    )
    
    message_text = (
        "🚀 Great! Let's get started.\n\n"
        "You can now use the menu buttons below to navigate "
        "through different features of this bot."
    )
    
    if callback.message:
        await callback.message.edit_text(
            text=message_text
        )
    
    await callback.answer()


@router.callback_query()
async def handle_other_callbacks(
    callback: CallbackQuery
) -> None:
    logger.warning(
        msg=f"Unknown callback data: {callback.data}"
    )
    
    await callback.answer(
        text="Unknown action"
    )
