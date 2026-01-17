import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, User as AiogramUser

from src.bot.handlers.start import start_command, help_command, info_command


@pytest.mark.asyncio
async def test_start_command():
    message = MagicMock(
        spec=Message
    )
    
    aiogram_user = MagicMock(
        spec=AiogramUser
    )
    aiogram_user.id = 12345
    aiogram_user.username = "testuser"
    aiogram_user.first_name = "Test"
    aiogram_user.last_name = "User"
    aiogram_user.language_code = "en"
    
    message.from_user = aiogram_user
    message.answer = AsyncMock()
    
    await start_command(
        message=message
    )
    
    message.answer.assert_called_once()
    
    call_args = message.answer.call_args
    assert "Welcome" in call_args[1]["text"]


@pytest.mark.asyncio
async def test_help_command():
    message = MagicMock(
        spec=Message
    )
    
    aiogram_user = MagicMock(
        spec=AiogramUser
    )
    aiogram_user.id = 12345
    
    message.from_user = aiogram_user
    message.answer = AsyncMock()
    
    await help_command(
        message=message
    )
    
    message.answer.assert_called_once()
    
    call_args = message.answer.call_args
    assert "Available Commands" in call_args[1]["text"]
