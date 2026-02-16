"""
Telegram Handlers

Production-ready handlers for all Telegram update types.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable, Any
from abc import ABC, abstractmethod

from telegram import Update, Bot
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

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


class BaseHandler(ABC):
    """Base handler class"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        self.bot = bot
        self.api_service = api_service
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle the update"""
        pass

    async def _can_handle(self, update: TelegramUpdate) -> bool:
        """Check if handler can process this update"""
        return True


class MessageHandler(BaseHandler):
    """Handle text and media messages"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        super().__init__(bot, api_service)
        self.commands: Dict[str, Callable] = {}
        self.middleware: List[Callable] = []

    def register_command(self, command: str, handler: Callable):
        """Register a command handler"""
        self.commands[command.lower()] = handler

    def add_middleware(self, middleware: Callable):
        """Add middleware to message processing"""
        self.middleware.append(middleware)

    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle incoming message"""
        if not update.message or not update.message.text:
            return False

        message = update.message
        text = message.text.strip()

        # Apply middleware
        for middleware_func in self.middleware:
            try:
                result = await middleware_func(update, context)
                if result is False:  # Middleware blocked the message
                    return False
            except Exception as e:
                self.logger.error(f"Middleware error: {e}")

        # Check if it's a command
        if text.startswith("/"):
            parts = text[1:].split(" ", 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if command in self.commands:
                try:
                    await self.commands[command](update, context, args)
                    return True
                except Exception as e:
                    self.logger.error(f"Command handler error for {command}: {e}")
                    await self.api_service.send_message(
                        message.chat.id,
                        "Sorry, there was an error processing your command.",
                    )
        else:
            # Handle regular message
            await self._handle_text_message(update, context)

        return True

    async def _handle_text_message(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle regular text messages"""
        message = update.message

        # Echo for demo
        await self.api_service.send_message(
            message.chat.id, f"You said: {message.text}"
        )


class CommandHandler(BaseHandler):
    """Handle bot commands"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        super().__init__(bot, api_service)
        self.commands: Dict[str, Callable] = {}
        self.admin_commands: Dict[str, Callable] = {}
        self.admin_users: List[int] = []

    def register_command(
        self, command: str, handler: Callable, admin_only: bool = False
    ):
        """Register a command"""
        if admin_only:
            self.admin_commands[command.lower()] = handler
        else:
            self.commands[command.lower()] = handler

    def set_admin_users(self, user_ids: List[int]):
        """Set admin user IDs"""
        self.admin_users = user_ids

    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle command"""
        if not update.message or not update.message.text:
            return False

        message = update.message
        text = message.text.strip()

        if not text.startswith("/"):
            return False

        parts = text[1:].split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # Check admin commands
        if command in self.admin_commands:
            if message.from_user and message.from_user.id in self.admin_users:
                try:
                    await self.admin_commands[command](update, context, args)
                    return True
                except Exception as e:
                    self.logger.error(f"Admin command error for {command}: {e}")
            else:
                await self.api_service.send_message(
                    message.chat.id, "This command is for admins only."
                )
                return True

        # Check regular commands
        if command in self.commands:
            try:
                await self.commands[command](update, context, args)
                return True
            except Exception as e:
                self.logger.error(f"Command error for {command}: {e}")
                await self.api_service.send_message(
                    message.chat.id,
                    "Sorry, there was an error processing your command.",
                )

        return False


class CallbackHandler(BaseHandler):
    """Handle callback queries from inline keyboards"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        super().__init__(bot, api_service)
        self.callbacks: Dict[str, Callable] = {}

    def register_callback(self, pattern: str, handler: Callable):
        """Register a callback handler"""
        self.callbacks[pattern] = handler

    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle callback query"""
        if not update.callback_query:
            return False

        callback_query = update.callback_query
        data = callback_query.data

        if not data:
            return False

        # Find matching callback handler
        for pattern, handler in self.callbacks.items():
            if pattern in data:
                try:
                    await handler(update, context)
                    return True
                except Exception as e:
                    self.logger.error(f"Callback handler error for {pattern}: {e}")

        # Default callback handling
        await callback_query.answer("Unknown action")
        return True


class InlineHandler(BaseHandler):
    """Handle inline queries"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        super().__init__(bot, api_service)
        self.inline_handlers: Dict[str, Callable] = {}

    def register_inline_handler(self, query_prefix: str, handler: Callable):
        """Register an inline query handler"""
        self.inline_handlers[query_prefix] = handler

    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle inline query"""
        if not update.inline_query:
            return False

        inline_query = update.inline_query
        query = inline_query.query.lower()

        # Find matching handler
        for prefix, handler in self.inline_handlers.items():
            if query.startswith(prefix):
                try:
                    await handler(update, context)
                    return True
                except Exception as e:
                    self.logger.error(f"Inline handler error for {prefix}: {e}")

        return False


class MediaHandler(BaseHandler):
    """Handle media messages (photo, video, audio, etc.)"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        super().__init__(bot, api_service)
        self.media_handlers: Dict[str, Callable] = {}

    def register_media_handler(self, media_type: str, handler: Callable):
        """Register a media handler"""
        self.media_handlers[media_type] = handler

    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle media message"""
        if not update.message:
            return False

        message = update.message

        # Determine media type
        media_type = None
        if message.photo:
            media_type = "photo"
        elif message.video:
            media_type = "video"
        elif message.audio:
            media_type = "audio"
        elif message.voice:
            media_type = "voice"
        elif message.document:
            media_type = "document"
        elif message.sticker:
            media_type = "sticker"
        elif message.animation:
            media_type = "animation"
        elif message.video_note:
            media_type = "video_note"

        if not media_type:
            return False

        # Handle media
        if media_type in self.media_handlers:
            try:
                await self.media_handlers[media_type](update, context)
                return True
            except Exception as e:
                self.logger.error(f"Media handler error for {media_type}: {e}")

        # Default media handling
        await self._handle_default_media(update, context, media_type)
        return True

    async def _handle_default_media(
        self,
        update: TelegramUpdate,
        context: ContextTypes.DEFAULT_TYPE,
        media_type: str,
    ):
        """Default media handling"""
        message = update.message

        # Get file info for logging
        file_info = f"{media_type} received"
        if message.caption:
            file_info += f" with caption: {message.caption}"

        self.logger.info(f"Media received in chat {message.chat.id}: {file_info}")

        # Acknowledge receipt
        await self.api_service.send_message(
            message.chat.id, f"✅ {media_type.title()} received!"
        )


class ChatMemberHandler(BaseHandler):
    """Handle chat member updates (join, leave, promote, etc.)"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        super().__init__(bot, api_service)
        self.member_handlers: Dict[str, Callable] = {}

    def register_member_handler(self, event_type: str, handler: Callable):
        """Register a chat member event handler"""
        self.member_handlers[event_type] = handler

    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle chat member updates"""
        # Handle different member update types
        if update.chat_member:
            return await self._handle_chat_member(update, context)
        elif update.my_chat_member:
            return await self._handle_my_chat_member(update, context)
        elif update.chat_join_request:
            return await self._handle_chat_join_request(update, context)

        return False

    async def _handle_chat_member(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle chat member updates"""
        chat_member = update.chat_member
        self.logger.info(f"Chat member update in {chat_member.chat.id}")
        return True

    async def _handle_my_chat_member(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle bot's own chat member updates"""
        my_chat_member = update.my_chat_member
        self.logger.info(f"My chat member update in {my_chat_member.chat.id}")
        return True

    async def _handle_chat_join_request(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle chat join requests"""
        join_request = update.chat_join_request
        self.logger.info(
            f"Chat join request in {join_request.chat.id} from {join_request.from_user.id}"
        )
        return True


class PollHandler(BaseHandler):
    """Handle poll updates"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        super().__init__(bot, api_service)
        self.poll_handlers: Dict[str, Callable] = {}

    def register_poll_handler(self, poll_type: str, handler: Callable):
        """Register a poll handler"""
        self.poll_handlers[poll_type] = handler

    async def handle(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle poll updates"""
        if update.poll:
            return await self._handle_poll(update, context)
        elif update.poll_answer:
            return await self._handle_poll_answer(update, context)

        return False

    async def _handle_poll(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle poll updates"""
        poll = update.poll
        self.logger.info(f"Poll update: {poll.question}")
        return True

    async def _handle_poll_answer(
        self, update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """Handle poll answers"""
        poll_answer = update.poll_answer
        self.logger.info(f"Poll answer from {poll_answer.user.id}")
        return True


# Handler Factory
class HandlerFactory:
    """Factory for creating and managing handlers"""

    def __init__(self, bot: Bot, api_service: TelegramAPIService):
        self.bot = bot
        self.api_service = api_service
        self.handlers: Dict[str, BaseHandler] = {}

    def create_handler(self, handler_type: str) -> BaseHandler:
        """Create a handler instance"""
        if handler_type == "message":
            return MessageHandler(self.bot, self.api_service)
        elif handler_type == "command":
            return CommandHandler(self.bot, self.api_service)
        elif handler_type == "callback":
            return CallbackHandler(self.bot, self.api_service)
        elif handler_type == "inline":
            return InlineHandler(self.bot, self.api_service)
        elif handler_type == "media":
            return MediaHandler(self.bot, self.api_service)
        elif handler_type == "chat_member":
            return ChatMemberHandler(self.bot, self.api_service)
        elif handler_type == "poll":
            return PollHandler(self.bot, self.api_service)
        else:
            raise ValueError(f"Unknown handler type: {handler_type}")

    def register_handler(self, handler_type: str, handler: BaseHandler):
        """Register a handler instance"""
        self.handlers[handler_type] = handler

    def get_handler(self, handler_type: str) -> Optional[BaseHandler]:
        """Get a registered handler"""
        return self.handlers.get(handler_type)

    def create_all_handlers(self) -> Dict[str, BaseHandler]:
        """Create all standard handlers"""
        handler_types = [
            "message",
            "command",
            "callback",
            "inline",
            "media",
            "chat_member",
            "poll",
        ]

        for handler_type in handler_types:
            try:
                handler = self.create_handler(handler_type)
                self.register_handler(handler_type, handler)
            except Exception as e:
                logger.error(f"Failed to create {handler_type} handler: {e}")

        return self.handlers
