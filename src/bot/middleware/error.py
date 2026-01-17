from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, ErrorEvent
import traceback

from src.bot.utils.logger import setup_logger


logger = setup_logger(
    name=__name__
)


class ErrorHandlerMiddleware(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(
                event,
                data
            )
        except Exception as e:
            logger.error(
                msg=f"Error handling update: {e}",
                exc_info=True
            )
            
            tb_list = traceback.format_exception(
                type(e),
                e,
                e.__traceback__
            )
            tb_string = "".join(tb_list)
            
            logger.error(
                msg=f"Traceback:\n{tb_string}"
            )
            
            if isinstance(event, Message):
                await event.answer(
                    text="An error occurred while processing your request. Please try again later."
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    text="An error occurred. Please try again.",
                    show_alert=True
                )
            
            raise
