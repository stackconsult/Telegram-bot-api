"""
Telegram Utilities

Production-ready utilities for Telegram bot development.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json
import hashlib
import re

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


class KeyboardBuilder:
    """Builder for creating inline and reply keyboards"""

    def __init__(self):
        self.buttons: List[List[InlineKeyboardButton]] = []
        self.reply_buttons: List[List[KeyboardButton]] = []

    def add_inline_button(
        self, text: str, callback_data: str, url: Optional[str] = None
    ) -> "KeyboardBuilder":
        """Add inline button"""
        button = InlineKeyboardButton(text=text, callback_data=callback_data, url=url)
        if not self.buttons:
            self.buttons.append([])
        self.buttons[-1].append(button)
        return self

    def add_inline_row(self, buttons: List[Dict[str, str]]) -> "KeyboardBuilder":
        """Add a row of inline buttons"""
        row = []
        for btn_data in buttons:
            button = InlineKeyboardButton(
                text=btn_data["text"],
                callback_data=btn_data.get("callback_data"),
                url=btn_data.get("url"),
            )
            row.append(button)
        self.buttons.append(row)
        return self

    def new_row(self) -> "KeyboardBuilder":
        """Start a new row"""
        if self.buttons and self.buttons[-1]:
            self.buttons.append([])
        return self

    def add_reply_button(
        self, text: str, request_contact: bool = False, request_location: bool = False
    ) -> "KeyboardBuilder":
        """Add reply keyboard button"""
        button = KeyboardButton(
            text=text,
            request_contact=request_contact,
            request_location=request_location,
        )
        if not self.reply_buttons:
            self.reply_buttons.append([])
        self.reply_buttons[-1].append(button)
        return self

    def add_reply_row(self, buttons: List[str]) -> "KeyboardBuilder":
        """Add a row of reply buttons"""
        row = [KeyboardButton(text=btn) for btn in buttons]
        self.reply_buttons.append(row)
        return self

    def new_reply_row(self) -> "KeyboardBuilder":
        """Start a new reply row"""
        if self.reply_buttons and self.reply_buttons[-1]:
            self.reply_buttons.append([])
        return self

    def build_inline(self) -> InlineKeyboardMarkup:
        """Build inline keyboard"""
        return InlineKeyboardMarkup(self.buttons) if self.buttons else None

    def build_reply(
        self, resize_keyboard: bool = True, one_time_keyboard: bool = False
    ) -> ReplyKeyboardMarkup:
        """Build reply keyboard"""
        return (
            ReplyKeyboardMarkup(
                self.reply_buttons,
                resize_keyboard=resize_keyboard,
                one_time_keyboard=one_time_keyboard,
            )
            if self.reply_buttons
            else None
        )

    def clear(self) -> "KeyboardBuilder":
        """Clear all buttons"""
        self.buttons.clear()
        self.reply_buttons.clear()
        return self


class MessageFormatter:
    """Utility for formatting Telegram messages"""

    @staticmethod
    def bold(text: str) -> str:
        """Format text as bold"""
        return f"*{text}*"

    @staticmethod
    def italic(text: str) -> str:
        """Format text as italic"""
        return f"_{text}_"

    @staticmethod
    def code(text: str) -> str:
        """Format text as code"""
        return f"`{text}`"

    @staticmethod
    def pre(text: str) -> str:
        """Format text as pre-formatted block"""
        return f"```{text}```"

    @staticmethod
    def link(text: str, url: str) -> str:
        """Create a link"""
        return f"[{text}]({url})"

    @staticmethod
    def mention(user_id: int, username: Optional[str] = None) -> str:
        """Create a mention"""
        if username:
            return f"@{username}"
        else:
            return f"[user](tg://user?id={user_id})"

    @staticmethod
    def escape_markdown(text: str) -> str:
        """Escape markdown special characters"""
        escape_chars = r"_*[]()~`>#+-=|{}.!"
        return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    @staticmethod
    def format_list(items: List[str], numbered: bool = False) -> str:
        """Format a list"""
        if numbered:
            return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
        else:
            return "\n".join(f"• {item}" for item in items)

    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]]) -> str:
        """Format a simple table"""
        if not rows:
            return ""

        # Calculate column widths
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        # Format header
        header_row = " | ".join(
            header.ljust(col_widths[i]) for i, header in enumerate(headers)
        )
        separator = "-".join([""] * (len(header_row) + 2))

        # Format rows
        table_rows = [header_row, separator]
        for row in rows:
            formatted_row = " | ".join(
                str(cell).ljust(col_widths[i]) if i < len(col_widths) else str(cell)
                for i, cell in enumerate(row)
            )
            table_rows.append(formatted_row)

        return "\n".join(table_rows)

    @staticmethod
    def truncate_text(text: str, max_length: int = 4096, suffix: str = "...") -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        return text[: max_length - len(suffix)] + suffix


class Validators:
    """Input validation utilities"""

    @staticmethod
    def is_valid_user_id(user_id: Union[str, int]) -> bool:
        """Validate user ID"""
        try:
            uid = int(user_id)
            return uid > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_chat_id(chat_id: Union[str, int]) -> bool:
        """Validate chat ID"""
        try:
            cid = int(chat_id)
            return cid != 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_token(token: str) -> bool:
        """Validate bot token format"""
        if not token or len(token) < 46:
            return False

        # Basic format check: numbers:numbers:token
        pattern = r"^\d+:[A-Za-z0-9_-]{35}$"
        return bool(re.match(pattern, token))

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$"
        return bool(re.match(pattern, url))

    @staticmethod
    def sanitize_text(text: str, max_length: int = 4096) -> str:
        """Sanitize text for Telegram"""
        if not text:
            return ""

        # Remove null bytes and control characters
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length]

        return text.strip()


class FileHelper:
    """File handling utilities"""

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension"""
        return filename.split(".")[-1].lower() if "." in filename else ""

    @staticmethod
    def is_image_file(filename: str) -> bool:
        """Check if file is an image"""
        image_extensions = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
        return FileHelper.get_file_extension(filename) in image_extensions

    @staticmethod
    def is_video_file(filename: str) -> bool:
        """Check if file is a video"""
        video_extensions = {"mp4", "avi", "mov", "wmv", "flv", "webm", "mkv"}
        return FileHelper.get_file_extension(filename) in video_extensions

    @staticmethod
    def is_audio_file(filename: str) -> bool:
        """Check if file is an audio file"""
        audio_extensions = {"mp3", "wav", "ogg", "flac", "aac", "m4a"}
        return FileHelper.get_file_extension(filename) in audio_extensions

    @staticmethod
    def is_document_file(filename: str) -> bool:
        """Check if file is a document"""
        doc_extensions = {
            "pdf",
            "doc",
            "docx",
            "txt",
            "rtf",
            "odt",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
        }
        return FileHelper.get_file_extension(filename) in doc_extensions

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)

        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1

        return f"{size:.1f} {size_names[i]}"

    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """Generate unique filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_obj = hashlib.md5(original_filename.encode())
        hash_hex = hash_obj.hexdigest()[:8]

        extension = FileHelper.get_file_extension(original_filename)
        name_without_ext = (
            original_filename.rsplit(".", 1)[0]
            if "." in original_filename
            else original_filename
        )

        return (
            f"{name_without_ext}_{timestamp}_{hash_hex}.{extension}"
            if extension
            else f"{name_without_ext}_{timestamp}_{hash_hex}"
        )


class RateLimiter:
    """Simple rate limiter for bot operations"""

    def __init__(self, max_requests: int = 30, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, List[float]] = {}

    async def check_limit(self, key: str) -> bool:
        """Check if request is allowed"""
        current_time = asyncio.get_event_loop().time()

        if key not in self.requests:
            self.requests[key] = []

        # Remove old requests
        cutoff_time = current_time - self.time_window
        self.requests[key] = [
            req_time for req_time in self.requests[key] if req_time > cutoff_time
        ]

        # Check limit
        if len(self.requests[key]) >= self.max_requests:
            return False

        # Add current request
        self.requests[key].append(current_time)
        return True

    def get_remaining_requests(self, key: str) -> int:
        """Get remaining requests for key"""
        if key not in self.requests:
            return self.max_requests

        current_time = asyncio.get_event_loop().time()
        cutoff_time = current_time - self.time_window

        # Count recent requests
        recent_requests = [
            req_time for req_time in self.requests[key] if req_time > cutoff_time
        ]
        return max(0, self.max_requests - len(recent_requests))

    def get_reset_time(self, key: str) -> Optional[float]:
        """Get time when limit resets"""
        if key not in self.requests or not self.requests[key]:
            return None

        oldest_request = min(self.requests[key])
        return oldest_request + self.time_window


class ContextHelper:
    """Helper for working with CallbackContext"""

    @staticmethod
    def set_user_data(context: CallbackContext, key: str, value: Any) -> None:
        """Set user data in context"""
        if not hasattr(context, "user_data"):
            context.user_data = {}
        context.user_data[key] = value

    @staticmethod
    def get_user_data(context: CallbackContext, key: str, default: Any = None) -> Any:
        """Get user data from context"""
        if not hasattr(context, "user_data"):
            return default
        return context.user_data.get(key, default)

    @staticmethod
    def set_chat_data(context: CallbackContext, key: str, value: Any) -> None:
        """Set chat data in context"""
        if not hasattr(context, "chat_data"):
            context.chat_data = {}
        context.chat_data[key] = value

    @staticmethod
    def get_chat_data(context: CallbackContext, key: str, default: Any = None) -> Any:
        """Get chat data from context"""
        if not hasattr(context, "chat_data"):
            return default
        return context.chat_data.get(key, default)

    @staticmethod
    def set_bot_data(context: CallbackContext, key: str, value: Any) -> None:
        """Set bot data in context"""
        if not hasattr(context, "bot_data"):
            context.bot_data = {}
        context.bot_data[key] = value

    @staticmethod
    def get_bot_data(context: CallbackContext, key: str, default: Any = None) -> Any:
        """Get bot data from context"""
        if not hasattr(context, "bot_data"):
            return default
        return context.bot_data.get(key, default)


class StateMachine:
    """Simple state machine for conversation flow"""

    def __init__(self):
        self.states: Dict[str, Dict[str, str]] = {}
        self.current_states: Dict[str, str] = {}

    def add_state(self, state_name: str, transitions: Dict[str, str]):
        """Add a state with transitions"""
        self.states[state_name] = transitions

    def set_state(self, key: str, state_name: str):
        """Set current state for key"""
        if state_name in self.states:
            self.current_states[key] = state_name
        else:
            raise ValueError(f"Unknown state: {state_name}")

    def get_state(self, key: str) -> Optional[str]:
        """Get current state for key"""
        return self.current_states.get(key)

    def transition(self, key: str, trigger: str) -> bool:
        """Transition to next state"""
        current_state = self.get_state(key)
        if not current_state:
            return False

        transitions = self.states.get(current_state, {})
        next_state = transitions.get(trigger)

        if next_state:
            self.set_state(key, next_state)
            return True

        return False

    def reset(self, key: str):
        """Reset state for key"""
        self.current_states.pop(key, None)


class AsyncLock:
    """Simple async lock for preventing concurrent operations"""

    def __init__(self):
        self._locks: Dict[str, asyncio.Lock] = {}

    async def acquire(self, key: str) -> asyncio.Lock:
        """Acquire lock for key"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def with_lock(self, key: str, coro):
        """Execute coroutine with lock"""
        lock = await self.acquire(key)
        async with lock:
            return await coro

    def cleanup(self, key: str):
        """Clean up lock for key"""
        self._locks.pop(key, None)


# Utility functions
async def safe_send_message(
    api_service, chat_id: Union[int, str], text: str, **kwargs
) -> bool:
    """Safely send a message with error handling"""
    try:
        result = await api_service.send_message(chat_id, text, **kwargs)
        return result is not None
    except Exception as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
        return False


async def safe_edit_message(
    api_service, chat_id: Union[int, str], message_id: int, text: str, **kwargs
) -> bool:
    """Safely edit a message with error handling"""
    try:
        result = await api_service.edit_message_text(
            chat_id, message_id, text, **kwargs
        )
        return result is not None
    except Exception as e:
        logger.error(f"Failed to edit message {message_id} in {chat_id}: {e}")
        return False


def parse_command_args(text: str) -> tuple[str, str]:
    """Parse command and arguments from message text"""
    if not text.startswith("/"):
        return "", text

    parts = text[1:].split(" ", 1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    return command, args


def extract_entities(message) -> List[Dict[str, Any]]:
    """Extract entities from message"""
    entities = []
    if hasattr(message, "entities") and message.entities:
        for entity in message.entities:
            entities.append(
                {
                    "type": entity.type,
                    "offset": entity.offset,
                    "length": entity.length,
                    "url": getattr(entity, "url", None),
                    "user": getattr(entity, "user", None),
                }
            )
    return entities
