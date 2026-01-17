from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from aiogram.types import User as AiogramUser


@dataclass
class User:
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_telegram_user(
        cls,
        telegram_user: AiogramUser
    ) -> "User":
        return cls(
            user_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            language_code=telegram_user.language_code,
            created_at=datetime.now()
        )
