"""
Comprehensive test suite for Telegram Bot API

Tests all major components and functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from typing import Dict, Any

# Import all components to test
from telegram_api.core import TelegramBot, BotConfig, BotMode, WebhookManager, UpdateProcessor
from telegram_api.models.telegram_models import TelegramUser, TelegramChat, TelegramMessage, TelegramUpdate
from telegram_api.services.api_service import TelegramAPIService
from telegram_api.handlers import MessageHandler, CommandHandler, CallbackHandler
from telegram_api.utils import KeyboardBuilder, MessageFormatter, Validators
from telegram_api.exceptions import TelegramAPIError, ValidationError

class TestTelegramModels:
    """Test Telegram data models"""
    
    def test_telegram_user_creation(self):
        """Test TelegramUser model creation"""
        user = TelegramUser(
            id=12345,
            is_bot=False,
            first_name="John",
            username="john_doe",
            last_name="Doe"
        )
        
        assert user.id == 12345
        assert user.is_bot is False
        assert user.first_name == "John"
        assert user.username == "john_doe"
        assert user.last_name == "Doe"
    
    def test_telegram_user_to_dict(self):
        """Test TelegramUser serialization"""
        user = TelegramUser(
            id=12345,
            is_bot=False,
            first_name="John"
        )
        
        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)
        assert user_dict["id"] == 12345
        assert user_dict["first_name"] == "John"
    
    def test_telegram_chat_creation(self):
        """Test TelegramChat model creation"""
        chat = TelegramChat(
            id=67890,
            type="private",
            first_name="John"
        )
        
        assert chat.id == 67890
        assert chat.type == "private"
        assert chat.first_name == "John"
    
    def test_telegram_message_creation(self):
        """Test TelegramMessage model creation"""
        user = TelegramUser(id=12345, is_bot=False, first_name="John")
        chat = TelegramChat(id=67890, type="private")
        
        message = TelegramMessage(
            message_id=1,
            date=datetime.utcnow(),
            chat=chat,
            from_user=user,
            text="Hello, World!"
        )
        
        assert message.message_id == 1
        assert message.text == "Hello, World!"
        assert message.chat == chat
        assert message.from_user == user

class TestBotConfig:
    """Test bot configuration"""
    
    def test_bot_config_creation(self):
        """Test BotConfig creation"""
        config = BotConfig(
            token="test_token",
            mode=BotMode.POLLING,
            admin_users=[12345]
        )
        
        assert config.token == "test_token"
        assert config.mode == BotMode.POLLING
        assert 12345 in config.admin_users
    
    def test_bot_config_defaults(self):
        """Test BotConfig default values"""
        config = BotConfig(token="test_token")
        
        assert config.token == "test_token"
        assert config.mode == BotMode.POLLING
        assert config.admin_users == []
        assert config.rate_limit_per_minute == 30

class TestKeyboardBuilder:
    """Test keyboard builder utility"""
    
    def test_inline_keyboard_builder(self):
        """Test inline keyboard building"""
        keyboard = (
            KeyboardBuilder()
            .add_inline_button("Button 1", "data1")
            .new_row()
            .add_inline_button("Button 2", "data2")
            .build_inline()
        )
        
        assert keyboard is not None
        assert len(keyboard.inline_keyboard) == 2
        assert len(keyboard.inline_keyboard[0]) == 1
        assert len(keyboard.inline_keyboard[1]) == 1
    
    def test_reply_keyboard_builder(self):
        """Test reply keyboard building"""
        keyboard = (
            KeyboardBuilder()
            .add_reply_button("Button 1")
            .new_reply_row()
            .add_reply_button("Button 2")
            .build_reply()
        )
        
        assert keyboard is not None
        assert len(keyboard.keyboard) == 2
        assert len(keyboard.keyboard[0]) == 1
        assert len(keyboard.keyboard[1]) == 1

class TestMessageFormatter:
    """Test message formatter utility"""
    
    def test_bold_formatting(self):
        """Test bold formatting"""
        result = MessageFormatter.bold("test")
        assert result == "*test*"
    
    def test_italic_formatting(self):
        """Test italic formatting"""
        result = MessageFormatter.italic("test")
        assert result == "_test_"
    
    def test_code_formatting(self):
        """Test code formatting"""
        result = MessageFormatter.code("test")
        assert result == "`test`"
    
    def test_pre_formatting(self):
        """Test pre formatting"""
        result = MessageFormatter.pre("test")
        assert result == "```test```"
    
    def test_link_formatting(self):
        """Test link formatting"""
        result = MessageFormatter.link("text", "https://example.com")
        assert result == "[text](https://example.com)"
    
    def test_escape_markdown(self):
        """Test markdown escaping"""
        result = MessageFormatter.escape_markdown("*test*")
        assert r"\*test\*" in result
    
    def test_format_list(self):
        """Test list formatting"""
        items = ["item1", "item2", "item3"]
        result = MessageFormatter.format_list(items)
        assert "• item1" in result
        assert "• item2" in result
        assert "• item3" in result
    
    def test_truncate_text(self):
        """Test text truncation"""
        long_text = "a" * 100
        result = MessageFormatter.truncate_text(long_text, 50)
        assert len(result) <= 53  # 50 + "..."
        assert result.endswith("...")

class TestValidators:
    """Test validation utilities"""
    
    def test_valid_user_id(self):
        """Test valid user ID validation"""
        assert Validators.is_valid_user_id(12345) is True
        assert Validators.is_valid_user_id("12345") is True
        assert Validators.is_valid_user_id(0) is False
        assert Validators.is_valid_user_id(-1) is False
        assert Validators.is_valid_user_id("abc") is False
    
    def test_valid_chat_id(self):
        """Test valid chat ID validation"""
        assert Validators.is_valid_chat_id(12345) is True
        assert Validators.is_valid_chat_id("12345") is True
        assert Validators.is_valid_chat_id(0) is False
        assert Validators.is_valid_chat_id("abc") is False
    
    def test_valid_token(self):
        """Test bot token validation"""
        valid_token = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
        assert Validators.is_valid_token(valid_token) is True
        assert Validators.is_valid_token("invalid") is False
        assert Validators.is_valid_token("") is False
    
    def test_valid_url(self):
        """Test URL validation"""
        assert Validators.is_valid_url("https://example.com") is True
        assert Validators.is_valid_url("http://example.com") is True
        assert Validators.is_valid_url("ftp://example.com") is False
        assert Validators.is_valid_url("not_a_url") is False
    
    def test_sanitize_text(self):
        """Test text sanitization"""
        text = "Hello\x00World\x01"
        result = Validators.sanitize_text(text)
        assert result == "HelloWorld"
        
        long_text = "a" * 5000
        result = Validators.sanitize_text(long_text, 100)
        assert len(result) <= 100

class TestTelegramAPIError:
    """Test custom exceptions"""
    
    def test_telegram_api_error(self):
        """Test base Telegram API error"""
        error = TelegramAPIError("Test error", 400, {"detail": "Bad request"})
        assert str(error) == "Test error"
        assert error.error_code == 400
        assert error.response_data["detail"] == "Bad request"
    
    def test_validation_error(self):
        """Test validation error"""
        error = ValidationError("Invalid input")
        assert isinstance(error, TelegramAPIError)
        assert str(error) == "Invalid input"
    
    def test_rate_limit_error(self):
        """Test rate limit error"""
        error = RateLimitError("Too many requests", 60)
        assert error.retry_after == 60

class TestMessageHandler:
    """Test message handler"""
    
    @pytest.fixture
    def mock_bot(self):
        """Mock bot instance"""
        bot = Mock()
        return bot
    
    @pytest.fixture
    def mock_api_service(self):
        """Mock API service"""
        service = AsyncMock()
        return service
    
    @pytest.fixture
    def message_handler(self, mock_bot, mock_api_service):
        """Create message handler instance"""
        return MessageHandler(mock_bot, mock_api_service)
    
    @pytest.mark.asyncio
    async def test_handle_text_message(self, message_handler, mock_api_service):
        """Test handling text messages"""
        # Create mock update
        mock_update = Mock()
        mock_message = Mock()
        mock_message.text = "Hello, bot!"
        mock_message.from_user = Mock()
        mock_message.from_user.id = 12345
        mock_update.message = mock_message
        
        # Create TelegramUpdate
        telegram_update = TelegramUpdate(
            update_id=1,
            message=TelegramMessage(
                message_id=1,
                date=datetime.utcnow(),
                chat=TelegramChat(id=67890, type="private"),
                from_user=TelegramUser(id=12345, is_bot=False, first_name="John"),
                text="Hello, bot!"
            )
        )
        
        # Mock context
        mock_context = Mock()
        
        # Test handling
        result = await message_handler.handle(telegram_update, mock_context)
        assert result is True
        
        # Verify API service was called
        mock_api_service.send_message.assert_called_once()

class TestCommandHandler:
    """Test command handler"""
    
    @pytest.fixture
    def mock_bot(self):
        """Mock bot instance"""
        bot = Mock()
        return bot
    
    @pytest.fixture
    def mock_api_service(self):
        """Mock API service"""
        service = AsyncMock()
        return service
    
    @pytest.fixture
    def command_handler(self, mock_bot, mock_api_service):
        """Create command handler instance"""
        handler = CommandHandler(mock_bot, mock_api_service)
        handler.set_admin_users([12345])
        return handler
    
    @pytest.mark.asyncio
    async def test_handle_regular_command(self, command_handler, mock_api_service):
        """Test handling regular commands"""
        # Register a test command
        async def test_command(update, context, args):
            await mock_api_service.send_message(update.message.chat.id, "Command executed")
        
        command_handler.register_command("test", test_command)
        
        # Create mock update with command
        mock_message = Mock()
        mock_message.text = "/test arg1"
        mock_message.chat = Mock()
        mock_message.chat.id = 67890
        mock_message.from_user = Mock()
        mock_message.from_user.id = 12345
        mock_update = Mock()
        mock_update.message = mock_message
        
        # Create TelegramUpdate
        telegram_update = TelegramUpdate(
            update_id=1,
            message=TelegramMessage(
                message_id=1,
                date=datetime.utcnow(),
                chat=TelegramChat(id=67890, type="private"),
                from_user=TelegramUser(id=12345, is_bot=False, first_name="John"),
                text="/test arg1"
            )
        )
        
        # Mock context
        mock_context = Mock()
        
        # Test handling
        result = await command_handler.handle(telegram_update, mock_context)
        assert result is True
        
        # Verify command was executed
        mock_api_service.send_message.assert_called_once_with(67890, "Command executed")

class TestTelegramBot:
    """Test main Telegram bot class"""
    
    @pytest.fixture
    def bot_config(self):
        """Create test bot configuration"""
        return BotConfig(
            token="test_token",
            mode=BotMode.POLLING,
            admin_users=[12345]
        )
    
    @pytest.fixture
    def telegram_bot(self, bot_config):
        """Create Telegram bot instance"""
        return TelegramBot(bot_config)
    
    def test_bot_initialization(self, telegram_bot):
        """Test bot initialization"""
        assert telegram_bot.config.token == "test_token"
        assert telegram_bot.config.mode == BotMode.POLLING
        assert 12345 in telegram_bot.config.admin_users
    
    def test_bot_status(self, telegram_bot):
        """Test bot status"""
        status = telegram_bot.get_status()
        assert isinstance(status, dict)
        assert "is_running" in status
        assert "mode" in status
        assert "token_configured" in status
        assert status["mode"] == "polling"
        assert status["token_configured"] is True

# Integration tests
class TestIntegration:
    """Integration tests for multiple components"""
    
    @pytest.mark.asyncio
    async def test_full_message_flow(self):
        """Test complete message processing flow"""
        # This would test the entire flow from update to response
        # Mock the entire stack and verify integration
        pass
    
    @pytest.mark.asyncio
    async def test_database_integration(self):
        """Test database service integration"""
        # Test database operations with actual models
        pass

# Performance tests
class TestPerformance:
    """Performance tests"""
    
    @pytest.mark.asyncio
    async def test_message_processing_performance(self):
        """Test message processing performance"""
        # Measure processing time for messages
        pass
    
    @pytest.mark.asyncio
    async def test_concurrent_handling(self):
        """Test concurrent message handling"""
        # Test handling multiple updates simultaneously
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
