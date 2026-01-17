from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.config.settings import settings
from src.bot.handlers import start
from src.bot.middleware.logging import LoggingMiddleware
from src.bot.middleware.error import ErrorHandlerMiddleware
from src.bot.utils.logger import setup_logger


logger = setup_logger(
    name=__name__,
    level=settings.bot.log_level
)


class BotService:
    
    def __init__(
        self,
        token: str
    ):
        self.token = token
        self.bot = None
        self.dispatcher = None
    
    def _create_bot(
        self
    ) -> Bot:
        bot = Bot(
            token=self.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )
        
        logger.info(
            msg="Bot instance created"
        )
        
        return bot
    
    def _create_dispatcher(
        self
    ) -> Dispatcher:
        from aiogram.fsm.storage.memory import MemoryStorage
        
        storage = MemoryStorage()
        dispatcher = Dispatcher(
            storage=storage
        )
        
        dispatcher.message.middleware(
            middleware=ErrorHandlerMiddleware()
        )
        dispatcher.callback_query.middleware(
            middleware=ErrorHandlerMiddleware()
        )
        
        dispatcher.message.middleware(
            middleware=LoggingMiddleware()
        )
        dispatcher.callback_query.middleware(
            middleware=LoggingMiddleware()
        )
        
        dispatcher.include_router(
            router=start.router
        )
        
        logger.info(
            msg="Dispatcher configured with all handlers and middleware"
        )
        
        return dispatcher
    
    def build(
        self
    ) -> tuple[Bot, Dispatcher]:
        logger.info(
            msg="Building bot application..."
        )
        
        self.bot = self._create_bot()
        self.dispatcher = self._create_dispatcher()
        
        logger.info(
            msg="Bot application built successfully"
        )
        
        return self.bot, self.dispatcher
    
    async def start(
        self
    ) -> None:
        if not self.bot or not self.dispatcher:
            self.build()
        
        logger.info(
            msg="Starting bot..."
        )
        
        await self.dispatcher.start_polling(
            self.bot
        )
    
    async def stop(
        self
    ) -> None:
        if not self.bot:
            return
        
        logger.info(
            msg="Stopping bot..."
        )
        
        await self.bot.session.close()
        
        logger.info(
            msg="Bot stopped successfully"
        )
