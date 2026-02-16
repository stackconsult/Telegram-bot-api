"""
Telegram API Models

Comprehensive data models for Telegram Bot API.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# Enums
class ChatType(str, Enum):
    """Chat types"""

    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


class MessageType(str, Enum):
    """Message types"""

    TEXT = "text"
    AUDIO = "audio"
    DOCUMENT = "document"
    GAME = "game"
    PHOTO = "photo"
    STICKER = "sticker"
    VIDEO = "video"
    VOICE = "voice"
    VIDEO_NOTE = "video_note"
    NEW_CHAT_MEMBERS = "new_chat_members"
    LEFT_CHAT_MEMBER = "left_chat_member"
    NEW_CHAT_TITLE = "new_chat_title"
    NEW_CHAT_PHOTO = "new_chat_photo"
    DELETE_CHAT_PHOTO = "delete_chat_photo"
    GROUP_CHAT_CREATED = "group_chat_created"
    SUPERGROUP_CHAT_CREATED = "supergroup_chat_created"
    CHANNEL_CHAT_CREATED = "channel_chat_created"
    MIGRATE_TO_CHAT_ID = "migrate_to_chat_id"
    MIGRATE_FROM_CHAT_ID = "migrate_from_chat_id"
    PINNED_MESSAGE = "pinned_message"
    INVOICE = "invoice"
    SUCCESSFUL_PAYMENT = "successful_payment"
    CONNECTED_WEBSITE = "connected_website"
    PASSPORT_DATA = "passport_data"
    PROXIMITY_ALERT_TRIGGERED = "proximity_alert_triggered"
    VIDEO_CHAT_STARTED = "video_chat_started"
    VIDEO_CHAT_ENDED = "video_chat_ended"
    VIDEO_CHAT_PARTICIPANTS_INVITED = "video_chat_participants_invited"
    VIDEO_CHAT_SCHEDULED = "video_chat_scheduled"
    MESSAGE_AUTO_DELETE_TIMER_CHANGED = "message_auto_delete_timer_changed"
    MIGRATE_TO_CHAT_ID = "migrate_to_chat_id"
    MIGRATE_FROM_CHAT_ID = "migrate_from_chat_id"
    PINNED_MESSAGE = "pinned_message"
    INVOICE = "invoice"
    SUCCESSFUL_PAYMENT = "successful_payment"
    CONNECTED_WEBSITE = "connected_website"
    PASSPORT_DATA = "passport_data"
    PROXIMITY_ALERT_TRIGGERED = "proximity_alert_triggered"
    VIDEO_CHAT_STARTED = "video_chat_started"
    VIDEO_CHAT_ENDED = "video_chat_ended"
    VIDEO_CHAT_PARTICIPANTS_INVITED = "video_chat_participants_invited"
    VIDEO_CHAT_SCHEDULED = "video_chat_scheduled"
    MESSAGE_AUTO_DELETE_TIMER_CHANGED = "message_auto_delete_timer_changed"
    VOICE_CHAT_STARTED = "voice_chat_started"
    VOICE_CHAT_ENDED = "voice_chat_ended"
    VOICE_CHAT_PARTICIPANTS_INVITED = "voice_chat_participants_invited"
    VOICE_CHAT_SCHEDULED = "voice_chat_scheduled"


class UpdateType(str, Enum):
    """Update types"""

    MESSAGE = "message"
    EDITED_MESSAGE = "edited_message"
    CHANNEL_POST = "channel_post"
    EDITED_CHANNEL_POST = "edited_channel_post"
    INLINE_QUERY = "inline_query"
    CHOSEN_INLINE_RESULT = "chosen_inline_result"
    CALLBACK_QUERY = "callback_query"
    SHIPPING_QUERY = "shipping_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    POLL = "poll"
    POLL_ANSWER = "poll_answer"
    MY_CHAT_MEMBER = "my_chat_member"
    CHAT_MEMBER = "chat_member"
    CHAT_JOIN_REQUEST = "chat_join_request"


# Base Models
@dataclass
class TelegramUser:
    """Telegram user model"""

    id: int
    is_bot: bool
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None

    @classmethod
    def from_telegram_user(cls, user) -> "TelegramUser":
        """Create from telegram.User"""
        return cls(
            id=user.id,
            is_bot=user.is_bot,
            first_name=user.first_name,
            username=user.username,
            last_name=user.last_name,
            language_code=user.language_code,
            is_premium=getattr(user, "is_premium", None),
            added_to_attachment_menu=getattr(user, "added_to_attachment_menu", None),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "is_bot": self.is_bot,
            "first_name": self.first_name,
            "username": self.username,
            "last_name": self.last_name,
            "language_code": self.language_code,
            "is_premium": self.is_premium,
            "added_to_attachment_menu": self.added_to_attachment_menu,
        }


@dataclass
class TelegramChat:
    """Telegram chat model"""

    id: int
    type: ChatType
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[Dict[str, Any]] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[bool] = None
    has_restricted_voice_and_video_messages: Optional[bool] = None
    join_to_send_messages: Optional[bool] = None
    join_by_request: Optional[bool] = None
    has_protected_content: Optional[bool] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional["TelegramMessage"] = None
    permissions: Optional[Dict[str, Any]] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_aggressive_anti_spam_enabled: Optional[bool] = None
    has_hidden_members: Optional[bool] = None
    has_visible_history: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[Dict[str, Any]] = None

    @classmethod
    def from_telegram_chat(cls, chat) -> "TelegramChat":
        """Create from telegram.Chat"""
        return cls(
            id=chat.id,
            type=ChatType(chat.type),
            title=chat.title,
            username=chat.username,
            first_name=chat.first_name,
            last_name=chat.last_name,
            bio=getattr(chat, "bio", None),
            has_private_forwards=getattr(chat, "has_private_forwards", None),
            has_restricted_voice_and_video_messages=getattr(
                chat, "has_restricted_voice_and_video_messages", None
            ),
            join_to_send_messages=getattr(chat, "join_to_send_messages", None),
            join_by_request=getattr(chat, "join_by_request", None),
            has_protected_content=getattr(chat, "has_protected_content", None),
            description=getattr(chat, "description", None),
            invite_link=getattr(chat, "invite_link", None),
            slow_mode_delay=getattr(chat, "slow_mode_delay", None),
            message_auto_delete_time=getattr(chat, "message_auto_delete_time", None),
            has_aggressive_anti_spam_enabled=getattr(
                chat, "has_aggressive_anti_spam_enabled", None
            ),
            has_hidden_members=getattr(chat, "has_hidden_members", None),
            has_visible_history=getattr(chat, "has_visible_history", None),
            sticker_set_name=getattr(chat, "sticker_set_name", None),
            can_set_sticker_set=getattr(chat, "can_set_sticker_set", None),
            linked_chat_id=getattr(chat, "linked_chat_id", None),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "description": self.description,
            "invite_link": self.invite_link,
        }


@dataclass
class TelegramMessage:
    """Telegram message model"""

    message_id: int
    date: datetime
    chat: TelegramChat
    from_user: Optional[TelegramUser] = None
    forward_from: Optional[TelegramUser] = None
    forward_from_chat: Optional[TelegramChat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[datetime] = None
    is_automatic_forward: Optional[bool] = None
    reply_to_message: Optional["TelegramMessage"] = None
    via_bot: Optional[TelegramUser] = None
    edit_date: Optional[datetime] = None
    has_protected_content: Optional[bool] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None
    animation: Optional[Dict[str, Any]] = None
    audio: Optional[Dict[str, Any]] = None
    document: Optional[Dict[str, Any]] = None
    photo: Optional[List[Dict[str, Any]]] = None
    sticker: Optional[Dict[str, Any]] = None
    video: Optional[Dict[str, Any]] = None
    video_note: Optional[Dict[str, Any]] = None
    voice: Optional[Dict[str, Any]] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[Dict[str, Any]]] = None
    has_media_spoiler: Optional[bool] = None
    contact: Optional[Dict[str, Any]] = None
    dice: Optional[Dict[str, Any]] = None
    game: Optional[Dict[str, Any]] = None
    poll: Optional[Dict[str, Any]] = None
    venue: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    new_chat_members: Optional[List[TelegramUser]] = None
    left_chat_member: Optional[TelegramUser] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List[Dict[str, Any]]] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional["TelegramMessage"] = None
    invoice: Optional[Dict[str, Any]] = None
    successful_payment: Optional[Dict[str, Any]] = None
    connected_website: Optional[str] = None
    passport_data: Optional[Dict[str, Any]] = None
    proximity_alert_triggered: Optional[Dict[str, Any]] = None
    video_chat_started: Optional[Dict[str, Any]] = None
    video_chat_ended: Optional[Dict[str, Any]] = None
    video_chat_participants_invited: Optional[Dict[str, Any]] = None
    video_chat_scheduled: Optional[Dict[str, Any]] = None
    message_auto_delete_timer_changed: Optional[Dict[str, Any]] = None
    voice_chat_started: Optional[Dict[str, Any]] = None
    voice_chat_ended: Optional[Dict[str, Any]] = None
    voice_chat_participants_invited: Optional[Dict[str, Any]] = None
    voice_chat_scheduled: Optional[Dict[str, Any]] = None
    reply_markup: Optional[Dict[str, Any]] = None

    @classmethod
    def from_telegram_message(cls, message) -> "TelegramMessage":
        """Create from telegram.Message"""
        return cls(
            message_id=message.message_id,
            date=datetime.fromtimestamp(message.date),
            chat=TelegramChat.from_telegram_chat(message.chat),
            from_user=(
                TelegramUser.from_telegram_user(message.from_user)
                if message.from_user
                else None
            ),
            forward_from=(
                TelegramUser.from_telegram_user(message.forward_from)
                if message.forward_from
                else None
            ),
            forward_from_chat=(
                TelegramChat.from_telegram_chat(message.forward_from_chat)
                if message.forward_from_chat
                else None
            ),
            forward_from_message_id=getattr(message, "forward_from_message_id", None),
            forward_signature=getattr(message, "forward_signature", None),
            forward_sender_name=getattr(message, "forward_sender_name", None),
            forward_date=(
                datetime.fromtimestamp(message.forward_date)
                if getattr(message, "forward_date", None)
                else None
            ),
            is_automatic_forward=getattr(message, "is_automatic_forward", None),
            edit_date=(
                datetime.fromtimestamp(message.edit_date)
                if getattr(message, "edit_date", None)
                else None
            ),
            has_protected_content=getattr(message, "has_protected_content", None),
            media_group_id=getattr(message, "media_group_id", None),
            author_signature=getattr(message, "author_signature", None),
            text=getattr(message, "text", None),
            caption=getattr(message, "caption", None),
            has_media_spoiler=getattr(message, "has_media_spoiler", None),
            new_chat_title=getattr(message, "new_chat_title", None),
            delete_chat_photo=getattr(message, "delete_chat_photo", None),
            group_chat_created=getattr(message, "group_chat_created", None),
            supergroup_chat_created=getattr(message, "supergroup_chat_created", None),
            channel_chat_created=getattr(message, "channel_chat_created", None),
            migrate_to_chat_id=getattr(message, "migrate_to_chat_id", None),
            migrate_from_chat_id=getattr(message, "migrate_from_chat_id", None),
            connected_website=getattr(message, "connected_website", None),
        )

    def get_message_type(self) -> MessageType:
        """Determine message type"""
        if self.text:
            return MessageType.TEXT
        elif self.audio:
            return MessageType.AUDIO
        elif self.document:
            return MessageType.DOCUMENT
        elif self.game:
            return MessageType.GAME
        elif self.photo:
            return MessageType.PHOTO
        elif self.sticker:
            return MessageType.STICKER
        elif self.video:
            return MessageType.VIDEO
        elif self.voice:
            return MessageType.VOICE
        elif self.video_note:
            return MessageType.VIDEO_NOTE
        elif self.new_chat_members:
            return MessageType.NEW_CHAT_MEMBERS
        elif self.left_chat_member:
            return MessageType.LEFT_CHAT_MEMBER
        elif self.new_chat_title:
            return MessageType.NEW_CHAT_TITLE
        elif self.new_chat_photo:
            return MessageType.NEW_CHAT_PHOTO
        elif self.delete_chat_photo:
            return MessageType.DELETE_CHAT_PHOTO
        elif self.group_chat_created:
            return MessageType.GROUP_CHAT_CREATED
        elif self.supergroup_chat_created:
            return MessageType.SUPERGROUP_CHAT_CREATED
        elif self.channel_chat_created:
            return MessageType.CHANNEL_CHAT_CREATED
        elif self.migrate_to_chat_id:
            return MessageType.MIGRATE_TO_CHAT_ID
        elif self.migrate_from_chat_id:
            return MessageType.MIGRATE_FROM_CHAT_ID
        elif self.pinned_message:
            return MessageType.PINNED_MESSAGE
        elif self.invoice:
            return MessageType.INVOICE
        elif self.successful_payment:
            return MessageType.SUCCESSFUL_PAYMENT
        elif self.connected_website:
            return MessageType.CONNECTED_WEBSITE
        elif self.passport_data:
            return MessageType.PASSPORT_DATA
        elif self.proximity_alert_triggered:
            return MessageType.PROXIMITY_ALERT_TRIGGERED
        elif self.video_chat_started:
            return MessageType.VIDEO_CHAT_STARTED
        elif self.video_chat_ended:
            return MessageType.VIDEO_CHAT_ENDED
        elif self.video_chat_participants_invited:
            return MessageType.VIDEO_CHAT_PARTICIPANTS_INVITED
        elif self.video_chat_scheduled:
            return MessageType.VIDEO_CHAT_SCHEDULED
        elif self.message_auto_delete_timer_changed:
            return MessageType.MESSAGE_AUTO_DELETE_TIMER_CHANGED
        elif self.voice_chat_started:
            return MessageType.VOICE_CHAT_STARTED
        elif self.voice_chat_ended:
            return MessageType.VOICE_CHAT_ENDED
        elif self.voice_chat_participants_invited:
            return MessageType.VOICE_CHAT_PARTICIPANTS_INVITED
        elif self.voice_chat_scheduled:
            return MessageType.VOICE_CHAT_SCHEDULED
        else:
            return MessageType.TEXT

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "message_id": self.message_id,
            "date": self.date.isoformat(),
            "chat": self.chat.to_dict(),
            "from_user": self.from_user.to_dict() if self.from_user else None,
            "text": self.text,
            "caption": self.caption,
            "message_type": self.get_message_type().value,
        }


@dataclass
class TelegramUpdate:
    """Telegram update model"""

    update_id: int
    message: Optional[TelegramMessage] = None
    edited_message: Optional[TelegramMessage] = None
    channel_post: Optional[TelegramMessage] = None
    edited_channel_post: Optional[TelegramMessage] = None
    inline_query: Optional[Dict[str, Any]] = None
    chosen_inline_result: Optional[Dict[str, Any]] = None
    callback_query: Optional[Dict[str, Any]] = None
    shipping_query: Optional[Dict[str, Any]] = None
    pre_checkout_query: Optional[Dict[str, Any]] = None
    poll: Optional[Dict[str, Any]] = None
    poll_answer: Optional[Dict[str, Any]] = None
    my_chat_member: Optional[Dict[str, Any]] = None
    chat_member: Optional[Dict[str, Any]] = None
    chat_join_request: Optional[Dict[str, Any]] = None

    @classmethod
    def from_telegram_update(cls, update) -> "TelegramUpdate":
        """Create from telegram.Update"""
        return cls(
            update_id=update.update_id,
            message=(
                TelegramMessage.from_telegram_message(update.message)
                if update.message
                else None
            ),
            edited_message=(
                TelegramMessage.from_telegram_message(update.edited_message)
                if update.edited_message
                else None
            ),
            channel_post=(
                TelegramMessage.from_telegram_message(update.channel_post)
                if update.channel_post
                else None
            ),
            edited_channel_post=(
                TelegramMessage.from_telegram_message(update.edited_channel_post)
                if update.edited_channel_post
                else None
            ),
            inline_query=getattr(update, "inline_query", None),
            chosen_inline_result=getattr(update, "chosen_inline_result", None),
            callback_query=getattr(update, "callback_query", None),
            shipping_query=getattr(update, "shipping_query", None),
            pre_checkout_query=getattr(update, "pre_checkout_query", None),
            poll=getattr(update, "poll", None),
            poll_answer=getattr(update, "poll_answer", None),
            my_chat_member=getattr(update, "my_chat_member", None),
            chat_member=getattr(update, "chat_member", None),
            chat_join_request=getattr(update, "chat_join_request", None),
        )

    def get_update_type(self) -> UpdateType:
        """Determine update type"""
        if self.message:
            return UpdateType.MESSAGE
        elif self.edited_message:
            return UpdateType.EDITED_MESSAGE
        elif self.channel_post:
            return UpdateType.CHANNEL_POST
        elif self.edited_channel_post:
            return UpdateType.EDITED_CHANNEL_POST
        elif self.inline_query:
            return UpdateType.INLINE_QUERY
        elif self.chosen_inline_result:
            return UpdateType.CHOSEN_INLINE_RESULT
        elif self.callback_query:
            return UpdateType.CALLBACK_QUERY
        elif self.shipping_query:
            return UpdateType.SHIPPING_QUERY
        elif self.pre_checkout_query:
            return UpdateType.PRE_CHECKOUT_QUERY
        elif self.poll:
            return UpdateType.POLL
        elif self.poll_answer:
            return UpdateType.POLL_ANSWER
        elif self.my_chat_member:
            return UpdateType.MY_CHAT_MEMBER
        elif self.chat_member:
            return UpdateType.CHAT_MEMBER
        elif self.chat_join_request:
            return UpdateType.CHAT_JOIN_REQUEST
        else:
            return UpdateType.MESSAGE

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "update_id": self.update_id,
            "update_type": self.get_update_type().value,
            "message": self.message.to_dict() if self.message else None,
            "edited_message": (
                self.edited_message.to_dict() if self.edited_message else None
            ),
            "channel_post": self.channel_post.to_dict() if self.channel_post else None,
            "edited_channel_post": (
                self.edited_channel_post.to_dict() if self.edited_channel_post else None
            ),
        }


# Pydantic Models for API
class TelegramUserModel(BaseModel):
    """Pydantic model for Telegram user"""

    id: int
    is_bot: bool
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None


class TelegramChatModel(BaseModel):
    """Pydantic model for Telegram chat"""

    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None


class TelegramMessageModel(BaseModel):
    """Pydantic model for Telegram message"""

    message_id: int
    date: datetime
    chat: TelegramChatModel
    from_user: Optional[TelegramUserModel] = None
    text: Optional[str] = None
    caption: Optional[str] = None


class TelegramUpdateModel(BaseModel):
    """Pydantic model for Telegram update"""

    update_id: int
    message: Optional[TelegramMessageModel] = None
    edited_message: Optional[TelegramMessageModel] = None
    channel_post: Optional[TelegramMessageModel] = None
    edited_channel_post: Optional[TelegramMessageModel] = None
