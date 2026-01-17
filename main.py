import asyncio
import signal
import sys

from src.config.settings import settings
from src.services.bot_service import BotService
from src.bot.utils.logger import setup_logger


logger = setup_logger(
    name=__name__,
    level=settings.bot.log_level
)


async def main() -> None:
    bot_service = BotService(
        token=settings.bot.token
    )
    
    bot_service.build()
    
    def signal_handler(
        sig,
        frame
    ):
        logger.info(
            msg="Received shutdown signal, stopping bot..."
        )
        sys.exit(0)
    
    signal.signal(
        signalnum=signal.SIGINT,
        handler=signal_handler
    )
    signal.signal(
        signalnum=signal.SIGTERM,
        handler=signal_handler
    )
    
    try:
        logger.info(
            msg="Bot started successfully! Press Ctrl+C to stop."
        )
        
        await bot_service.start()
        
    except KeyboardInterrupt:
        logger.info(
            msg="Keyboard interrupt received"
        )
    except Exception as e:
        logger.error(
            msg=f"Unexpected error: {e}",
            exc_info=True
        )
    finally:
        await bot_service.stop()


if __name__ == "__main__":
    try:
        asyncio.run(
            main=main()
        )
    except KeyboardInterrupt:
        logger.info(
            msg="Application stopped by user"
        )
