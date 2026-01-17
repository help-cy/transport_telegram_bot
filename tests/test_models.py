from unittest.mock import MagicMock
from telegram import User as TelegramUser

from src.models.user import User


def test_user_from_telegram_user():
    telegram_user = MagicMock(
        spec=TelegramUser
    )
    telegram_user.id = 12345
    telegram_user.username = "testuser"
    telegram_user.first_name = "Test"
    telegram_user.last_name = "User"
    telegram_user.language_code = "en"
    
    user = User.from_telegram_user(
        telegram_user=telegram_user
    )
    
    assert user.user_id == 12345
    assert user.username == "testuser"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.language_code == "en"
    assert user.created_at is not None
