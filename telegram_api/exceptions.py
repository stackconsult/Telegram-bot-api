"""
Telegram Exceptions

Custom exceptions for Telegram bot operations.
"""


class TelegramAPIError(Exception):
    """Base exception for Telegram API errors"""

    def __init__(
        self, message: str, error_code: int = None, response_data: dict = None
    ):
        super().__init__(message)
        self.error_code = error_code
        self.response_data = response_data or {}


class ValidationError(TelegramAPIError):
    """Raised when input validation fails"""

    pass


class AuthenticationError(TelegramAPIError):
    """Raised when authentication fails"""

    pass


class RateLimitError(TelegramAPIError):
    """Raised when rate limit is exceeded"""

    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message)
        self.retry_after = retry_after


class ChatNotFoundError(TelegramAPIError):
    """Raised when chat is not found"""

    pass


class UserNotFoundError(TelegramAPIError):
    """Raised when user is not found"""

    pass


class PermissionError(TelegramAPIError):
    """Raised when permission is denied"""

    pass


class MessageNotFoundError(TelegramAPIError):
    """Raised when message is not found"""

    pass


class FileError(TelegramAPIError):
    """Raised when file operations fail"""

    pass


class WebhookError(TelegramAPIError):
    """Raised when webhook operations fail"""

    pass


class BotBlockedError(TelegramAPIError):
    """Raised when bot is blocked by user"""

    pass


class ChatAdminRequiredError(TelegramAPIError):
    """Raised when chat admin privileges are required"""

    pass


class TooManyRequestsError(RateLimitError):
    """Raised when too many requests are made"""

    pass
