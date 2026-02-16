"""
Telegram Database Models

SQLAlchemy models for persistent storage of Telegram data.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
    JSON,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), nullable=True)
    is_bot = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen = Column(DateTime, nullable=True)

    # Relationships
    messages = relationship("Message", back_populates="user")
    chat_memberships = relationship("ChatMember", back_populates="user")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "language_code": self.language_code,
            "is_bot": self.is_bot,
            "is_premium": self.is_premium,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
        }


class Chat(Base):
    """Chat model"""

    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    type = Column(String(20), nullable=False)  # private, group, supergroup, channel
    title = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    invite_link = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="chat")
    members = relationship("ChatMember", back_populates="chat")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "type": self.type,
            "title": self.title,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "description": self.description,
            "invite_link": self.invite_link,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Message(Base):
    """Message model"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    text = Column(Text, nullable=True)
    caption = Column(Text, nullable=True)
    message_type = Column(String(50), nullable=False)
    media_type = Column(String(50), nullable=True)
    file_id = Column(String(255), nullable=True)
    reply_to_message_id = Column(Integer, nullable=True)
    forward_from = Column(JSON, nullable=True)
    entities = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="messages")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "text": self.text,
            "caption": self.caption,
            "message_type": self.message_type,
            "media_type": self.media_type,
            "file_id": self.file_id,
            "reply_to_message_id": self.reply_to_message_id,
            "forward_from": self.forward_from,
            "entities": self.entities,
            "metadata": self.metadata,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ChatMember(Base):
    """Chat member model"""

    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(
        String(50), nullable=False
    )  # creator, administrator, member, restricted, left, kicked
    custom_title = Column(String(255), nullable=True)
    is_anonymous = Column(Boolean, default=False)
    can_be_edited = Column(Boolean, default=False)
    can_manage_chat = Column(Boolean, default=False)
    can_post_messages = Column(Boolean, default=False)
    can_edit_messages = Column(Boolean, default=False)
    can_delete_messages = Column(Boolean, default=False)
    can_manage_video_chats = Column(Boolean, default=False)
    can_restrict_members = Column(Boolean, default=False)
    can_promote_members = Column(Boolean, default=False)
    can_change_info = Column(Boolean, default=False)
    can_invite_users = Column(Boolean, default=False)
    can_pin_messages = Column(Boolean, default=False)
    can_manage_topics = Column(Boolean, default=False)
    joined_at = Column(DateTime, nullable=True)
    promoted_at = Column(DateTime, nullable=True)
    left_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "status": self.status,
            "custom_title": self.custom_title,
            "is_anonymous": self.is_anonymous,
            "can_be_edited": self.can_be_edited,
            "can_manage_chat": self.can_manage_chat,
            "can_post_messages": self.can_post_messages,
            "can_edit_messages": self.can_edit_messages,
            "can_delete_messages": self.can_delete_messages,
            "can_manage_video_chats": self.can_manage_video_chats,
            "can_restrict_members": self.can_restrict_members,
            "can_promote_members": self.can_promote_members,
            "can_change_info": self.can_change_info,
            "can_invite_users": self.can_invite_users,
            "can_pin_messages": self.can_pin_messages,
            "can_manage_topics": self.can_manage_topics,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "promoted_at": self.promoted_at.isoformat() if self.promoted_at else None,
            "left_at": self.left_at.isoformat() if self.left_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BotCommand(Base):
    """Bot command model"""

    __tablename__ = "bot_commands"

    id = Column(Integer, primary_key=True)
    command = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    is_enabled = Column(Boolean, default=True)
    is_admin_only = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "command": self.command,
            "description": self.description,
            "is_enabled": self.is_enabled,
            "is_admin_only": self.is_admin_only,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserSession(Base):
    """User session model"""

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    session_data = Column(JSON, nullable=True)
    current_state = Column(String(100), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    chat = relationship("Chat")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "chat_id": self.chat_id,
            "session_data": self.session_data,
            "current_state": self.current_state,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BotLog(Base):
    """Bot activity log model"""

    __tablename__ = "bot_logs"

    id = Column(Integer, primary_key=True)
    level = Column(String(20), nullable=False)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=True)
    update_type = Column(String(50), nullable=True)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")
    chat = relationship("Chat")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "level": self.level,
            "message": self.message,
            "user_id": self.user_id,
            "chat_id": self.chat_id,
            "update_type": self.update_type,
            "extra_data": self.extra_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class BotStats(Base):
    """Bot statistics model"""

    __tablename__ = "bot_stats"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, index=True)
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_chats = Column(Integer, default=0)
    active_chats = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    messages_received = Column(Integer, default=0)
    commands_used = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "total_users": self.total_users,
            "active_users": self.active_users,
            "total_chats": self.total_chats,
            "active_chats": self.active_chats,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "commands_used": self.commands_used,
            "errors_count": self.errors_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
