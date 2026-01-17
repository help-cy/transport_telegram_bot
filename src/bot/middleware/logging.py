from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.bot.utils.logger import setup_logger


logger = setup_logger(
    name=__name__
)


class LoggingMiddleware(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = None
        log_message = "Unknown event"
        
        if isinstance(event, Message):
            user = event.from_user
            if user:
                user_info = f"User {user.id} (@{user.username})"
                
                if event.web_app_data:
                    log_message = f"{user_info} sent web_app_data"
                elif event.text:
                    log_message = f"{user_info} sent message: {event.text}"
                elif event.location:
                    log_message = f"{user_info} sent location"
                else:
                    log_message = f"{user_info} sent message (unknown type)"
            
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            if user:
                user_info = f"User {user.id} (@{user.username})"
                log_message = f"{user_info} clicked button: {event.data}"
        
        logger.info(
            msg=log_message
        )
        
        return await handler(
            event,
            data
        )
