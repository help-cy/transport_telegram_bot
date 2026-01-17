from dataclasses import dataclass
from typing import Optional
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)


@dataclass
class BotConfig:
    token: str
    log_level: str = "INFO"
    webapp_url: str = ""
    
    @classmethod
    def from_env(cls) -> "BotConfig":
        token = os.getenv(
            key="BOT_TOKEN"
        )
        if not token:
            raise ValueError("BOT_TOKEN environment variable is required")
        
        log_level = os.getenv(
            key="LOG_LEVEL",
            default="INFO"
        )
        
        webapp_url = os.getenv(
            key="WEBAPP_URL",
            default=""
        )
        
        return cls(
            token=token,
            log_level=log_level,
            webapp_url=webapp_url
        )


@dataclass
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4o"
    max_tokens: int = 500
    temperature: float = 0.7
    
    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        api_key = os.getenv(
            key="OPENAI_API_KEY"
        )
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        model = os.getenv(
            key="OPENAI_MODEL",
            default="gpt-4o"
        )
        
        max_tokens = int(
            os.getenv(
                key="OPENAI_MAX_TOKENS",
                default="500"
            )
        )
        
        temperature = float(
            os.getenv(
                key="OPENAI_TEMPERATURE",
                default="0.7"
            )
        )
        
        return cls(
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )


@dataclass
class WebhookConfig:
    host: Optional[str] = None
    path: str = "/webhook"
    url: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "WebhookConfig":
        host = os.getenv(
            key="WEBHOOK_HOST"
        )
        path = os.getenv(
            key="WEBHOOK_PATH",
            default="/webhook"
        )
        url = os.getenv(
            key="WEBHOOK_URL"
        )
        
        return cls(
            host=host,
            path=path,
            url=url
        )


@dataclass
class Settings:
    bot: BotConfig
    webhook: WebhookConfig
    openai: OpenAIConfig
    
    @classmethod
    def load(cls) -> "Settings":
        bot_config = BotConfig.from_env()
        webhook_config = WebhookConfig.from_env()
        openai_config = OpenAIConfig.from_env()
        
        return cls(
            bot=bot_config,
            webhook=webhook_config,
            openai=openai_config
        )


settings = Settings.load()
