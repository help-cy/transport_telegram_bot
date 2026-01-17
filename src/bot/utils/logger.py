import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: str = "INFO"
) -> logging.Logger:
    logger = logging.getLogger(
        name=name
    )
    
    log_level = getattr(
        logging,
        level.upper(),
        logging.INFO
    )
    logger.setLevel(
        level=log_level
    )
    
    if not logger.handlers:
        handler = logging.StreamHandler(
            stream=sys.stdout
        )
        handler.setLevel(
            level=log_level
        )
        
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(
            fmt=formatter
        )
        
        logger.addHandler(
            hdlr=handler
        )
    
    return logger
