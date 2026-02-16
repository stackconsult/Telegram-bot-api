"""
Core Telegram Bot Components

Production-ready core components for Telegram bot applications.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from telegram import Update, Bot, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    filters,
)
from telegram.request import BaseRequest

from ..config.settings import settings
from ..models.telegram_models import (
    TelegramUpdate,
    TelegramMessage,
    TelegramUser,
    TelegramChat,
)
from ..services.api_service import TelegramAPIService
from ..utils.keyboards import KeyboardBuilder
from ..utils.formatters import MessageFormatter

logger = logging.getLogger(__name__)


class BotMode(str, Enum):
    """Bot operation modes"""

    POLLING = "polling"
    WEBHOOK = "webhook"
    WEBHOOK_APP = "webhook_app"


@dataclass
class BotConfig:
    """Bot configuration"""

    token: str
    mode: BotMode = BotMode.POLLING
    webhook_url: Optional[str] = None
    webhook_path: str = "/webhook"
    admin_users: List[int] = field(default_factory=list)
    allowed_users: List[int] = field(default_factory=list)
    rate_limit_per_minute: int = 30
    enable_logging: bool = True
    log_level: str = "INFO"


class WebhookManager:
    """Manages Telegram bot webhooks"""

    def __init__(self, bot: Bot, config: BotConfig):
        self.bot = bot
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.WebhookManager")

    async def setup_webhook(self) -> bool:
        """Setup webhook for the bot"""
        try:
            if not self.config.webhook_url:
                self.logger.error("Webhook URL not configured")
                return False

            webhook_url = f"{self.config.webhook_url}{self.config.webhook_path}"

            await self.bot.set_webhook(
                url=webhook_url,
                secret_token=self.config.token,
                max_connections=40,
                allowed_updates=None,
            )

            self.logger.info(f"Webhook set to: {webhook_url}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to setup webhook: {e}")
            return False

    async def remove_webhook(self) -> bool:
        """Remove webhook and switch to polling"""
        try:
            await self.bot.delete_webhook()
            self.logger.info("Webhook removed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove webhook: {e}")
            return False

    async def get_webhook_info(self) -> Dict[str, Any]:
        """Get current webhook information"""
        try:
            info = await self.bot.get_webhook_info()
            return {
                "url": info.url,
                "has_custom_certificate": info.has_custom_certificate,
                "pending_update_count": info.pending_update_count,
                "last_error_date": info.last_error_date,
                "last_error_message": info.last_error_message,
                "max_connections": info.max_connections,
                "allowed_updates": info.allowed_updates,
            }
        except Exception as e:
            self.logger.error(f"Failed to get webhook info: {e}")
            return {}


class UpdateProcessor:
    """Processes Telegram updates"""

    def __init__(self, config: BotConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.UpdateProcessor")
        self.handlers: Dict[str, List[Callable]] = {
            "message": [],
            "command": [],
            "callback_query": [],
            "inline_query": [],
            "edited_message": [],
            "channel_post": [],
            "edited_channel_post": [],
            "chosen_inline_result": [],
            "shipping_query": [],
            "pre_checkout_query": [],
            "poll": [],
            "poll_answer": [],
            "my_chat_member": [],
            "chat_member": [],
            "chat_join_request": [],
        }

    def register_handler(self, update_type: str, handler: Callable):
        """Register handler for specific update type"""
        if update_type in self.handlers:
            self.handlers[update_type].append(handler)
        else:
            self.logger.warning(f"Unknown update type: {update_type}")

    async def process_update(self, update: Update) -> bool:
        """Process incoming update"""
        try:
            # Convert to our model
            telegram_update = TelegramUpdate.from_telegram_update(update)

            # Determine update type and route to handlers
            update_type = self._get_update_type(update)

            if update_type in self.handlers:
                for handler in self.handlers[update_type]:
                    try:
                        await handler(telegram_update)
                    except Exception as e:
                        self.logger.error(f"Handler error for {update_type}: {e}")
                        continue
                return True
            else:
                self.logger.warning(f"No handlers for update type: {update_type}")
                return False

        except Exception as e:
            self.logger.error(f"Error processing update: {e}")
            return False

    def _get_update_type(self, update: Update) -> str:
        """Determine update type"""
        if update.message:
            return "message"
        elif update.edited_message:
            return "edited_message"
        elif update.channel_post:
            return "channel_post"
        elif update.edited_channel_post:
            return "edited_channel_post"
        elif update.callback_query:
            return "callback_query"
        elif update.inline_query:
            return "inline_query"
        elif update.chosen_inline_result:
            return "chosen_inline_result"
        elif update.shipping_query:
            return "shipping_query"
        elif update.pre_checkout_query:
            return "pre_checkout_query"
        elif update.poll:
            return "poll"
        elif update.poll_answer:
            return "poll_answer"
        elif update.my_chat_member:
            return "my_chat_member"
        elif update.chat_member:
            return "chat_member"
        elif update.chat_join_request:
            return "chat_join_request"
        else:
            return "unknown"


class TelegramBot:
    """Main Telegram bot class with production features"""

    def __init__(self, config: Optional[BotConfig] = None):
        self.config = config or BotConfig(
            token=settings.BOT_TOKEN,
            mode=BotMode.WEBHOOK if settings.WEBHOOK_URL else BotMode.POLLING,
            webhook_url=settings.WEBHOOK_URL,
            admin_users=[settings.ADMIN_USER_ID] if settings.ADMIN_USER_ID else [],
        )

        self.bot: Optional[Bot] = None
        self.application: Optional[Application] = None
        self.webhook_manager: Optional[WebhookManager] = None
        self.update_processor: UpdateProcessor = UpdateProcessor(self.config)
        self.api_service: Optional[TelegramAPIService] = None

        self.logger = logging.getLogger(__name__)
        self._is_running = False

        # Setup logging
        if self.config.enable_logging:
            logging.basicConfig(level=getattr(logging, self.config.log_level))

    async def initialize(self) -> bool:
        """Initialize the bot and all components"""
        try:
            self.logger.info("Initializing Telegram Bot...")

            # Create bot application
            self.application = Application.builder().token(self.config.token).build()
            self.bot = self.application.bot

            # Initialize services
            self.api_service = TelegramAPIService(self.bot)
            self.webhook_manager = WebhookManager(self.bot, self.config)

            # Setup webhook if needed
            if self.config.mode == BotMode.WEBHOOK:
                success = await self.webhook_manager.setup_webhook()
                if not success:
                    self.logger.error("Failed to setup webhook")
                    return False

            # Register default handlers
            await self._register_default_handlers()

            self.logger.info("Bot initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize bot: {e}")
            return False

    async def _register_default_handlers(self):
        """Register default update handlers"""
        if not self.application:
            return

        # Message handlers
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND, self._handle_message
        )
        self.application.add_handler(message_handler)

        # Command handlers
        command_handler = CommandHandler("start", self._handle_start)
        self.application.add_handler(command_handler)

        command_handler = CommandHandler("help", self._handle_help)
        self.application.add_handler(command_handler)

        # Callback query handlers
        callback_handler = CallbackQueryHandler(self._handle_callback_query)
        self.application.add_handler(callback_handler)

        # Inline query handlers
        inline_handler = InlineQueryHandler(self._handle_inline_query)
        self.application.add_handler(inline_handler)

    async def start(self) -> bool:
        """Start the bot"""
        try:
            if not self.application:
                self.logger.error("Bot not initialized")
                return False

            await self.application.initialize()
            await self.application.start()

            if self.config.mode == BotMode.POLLING:
                await self.application.updater.start_polling()
                self.logger.info("Bot started in polling mode")
            else:
                await self.application.updater.start_webhook(
                    listen="0.0.0.0",
                    port=8000,
                    url_path=self.config.webhook_path,
                    webhook_url=f"{self.config.webhook_url}{self.config.webhook_path}",
                )
                self.logger.info("Bot started in webhook mode")

            self._is_running = True
            return True

        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            return False

    async def stop(self):
        """Stop the bot gracefully"""
        try:
            if self.application:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()

            self._is_running = False
            self.logger.info("Bot stopped")

        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")

    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> bool:
        """Send a message"""
        try:
            if self.bot:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                    **kwargs,
                )
                return True
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
        return False

    async def _handle_message(self, update: Update, context):
        """Handle incoming messages"""
        try:
            message = update.message
            user_id = message.from_user.id

            # Check if user is allowed
            if self.config.allowed_users and user_id not in self.config.allowed_users:
                await message.reply_text(
                    "Sorry, you're not authorized to use this bot."
                )
                return

            # Process message through update processor
            await self.update_processor.process_update(update)

            # Echo message for demo
            await message.reply_text(f"Received: {message.text}")

        except Exception as e:
            self.logger.error(f"Error handling message: {e}")

    async def _handle_start(self, update: Update, context):
        """Handle /start command"""
        try:
            message = update.message
            welcome_text = (
                "🤖 Welcome to the Telegram Bot API Template!\n\n"
                "This is a production-ready bot with comprehensive features.\n\n"
                "Available commands:\n"
                "/help - Show help\n"
                "/status - Check bot status"
            )

            await message.reply_text(welcome_text)

        except Exception as e:
            self.logger.error(f"Error handling start command: {e}")

    async def _handle_help(self, update: Update, context):
        """Handle /help command"""
        try:
            message = update.message
            help_text = (
                "📚 **Bot Help**\n\n"
                "**Commands:**\n"
                "/start - Start the bot\n"
                "/help - Show this help\n"
                "/status - Check bot status\n\n"
                "**Features:**\n"
                "• Message handling\n"
                "• Command processing\n"
                "• Callback queries\n"
                "• Inline queries\n"
                "• Webhook support\n"
                "• Rate limiting\n"
                "• User management"
            )

            await message.reply_text(help_text, parse_mode="Markdown")

        except Exception as e:
            self.logger.error(f"Error handling help command: {e}")

    async def _handle_callback_query(self, update: Update, context):
        """Handle callback queries"""
        try:
            callback_query = update.callback_query
            await callback_query.answer()

            # Process callback through update processor
            await self.update_processor.process_update(update)

        except Exception as e:
            self.logger.error(f"Error handling callback query: {e}")

    async def _handle_inline_query(self, update: Update, context):
        """Handle inline queries"""
        try:
            inline_query = update.inline_query

            # Process inline query through update processor
            await self.update_processor.process_update(update)

        except Exception as e:
            self.logger.error(f"Error handling inline query: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get bot status"""
        return {
            "is_running": self._is_running,
            "mode": self.config.mode.value,
            "token_configured": bool(self.config.token),
            "webhook_configured": bool(self.config.webhook_url),
            "admin_users": len(self.config.admin_users),
            "allowed_users": len(self.config.allowed_users),
            "rate_limit": self.config.rate_limit_per_minute,
        }

    async def get_me(self) -> Optional[Dict[str, Any]]:
        """Get bot information"""
        try:
            if self.bot:
                bot_info = await self.bot.get_me()
                return {
                    "id": bot_info.id,
                    "is_bot": bot_info.is_bot,
                    "first_name": bot_info.first_name,
                    "username": bot_info.username,
                    "can_join_groups": bot_info.can_join_groups,
                    "can_read_all_group_messages": bot_info.can_read_all_group_messages,
                    "supports_inline_queries": bot_info.supports_inline_queries,
                }
        except Exception as e:
            self.logger.error(f"Failed to get bot info: {e}")
        return None


# Global bot instance
bot_instance = TelegramBot()


async def main():
    """Main entry point"""
    try:
        if await bot_instance.initialize():
            if await bot_instance.start():
                # Keep running
                while bot_instance._is_running:
                    await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down bot...")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot_instance.stop()


if __name__ == "__main__":
    asyncio.run(main())
