"""
Telegram Database Services

Database services for persistent storage operations.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, delete, func, and_, or_

from ..models.database_models import (
    User,
    Chat,
    Message,
    ChatMember,
    BotCommand,
    UserSession,
    BotLog,
    BotStats,
)
from ..models.telegram_models import TelegramUser, TelegramChat, TelegramMessage
from ..config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseService:
    """Main database service"""

    def __init__(self, database_url: str = None):
        self.database_url = database_url or settings.DATABASE_URL
        self.engine = None
        self.async_session = None

    async def initialize(self):
        """Initialize database connection"""
        try:
            self.engine = create_async_engine(self.database_url, echo=False)
            self.async_session = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            logger.info("Database service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    async def create_tables(self):
        """Create all tables"""
        try:
            from ..models.database_models import Base

            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    async def get_session(self) -> AsyncSession:
        """Get database session"""
        return self.async_session()

    async def close(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")


class UserService:
    """User database service"""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    async def get_or_create_user(self, telegram_user: TelegramUser) -> User:
        """Get or create user from Telegram user"""
        async with self.db_service.get_session() as session:
            # Try to get existing user
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_user.id)
            )
            user = result.scalar_one_or_none()

            if user:
                # Update existing user
                user.username = telegram_user.username
                user.first_name = telegram_user.first_name
                user.last_name = telegram_user.last_name
                user.language_code = telegram_user.language_code
                user.is_premium = telegram_user.is_premium
                user.last_seen = datetime.utcnow()
                user.updated_at = datetime.utcnow()
            else:
                # Create new user
                user = User(
                    telegram_id=telegram_user.id,
                    username=telegram_user.username,
                    first_name=telegram_user.first_name,
                    last_name=telegram_user.last_name,
                    language_code=telegram_user.language_code,
                    is_bot=telegram_user.is_bot,
                    is_premium=telegram_user.is_premium,
                    last_seen=datetime.utcnow(),
                )
                session.add(user)

            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by database ID"""
        async with self.db_service.get_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    async def update_user_last_seen(self, telegram_id: int):
        """Update user last seen timestamp"""
        async with self.db_service.get_session() as session:
            await session.execute(
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(last_seen=datetime.utcnow(), updated_at=datetime.utcnow())
            )
            await session.commit()

    async def get_active_users_count(self, days: int = 30) -> int:
        """Get count of active users in last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(func.count(User.id)).where(User.last_seen >= cutoff_date)
            )
            return result.scalar()


class ChatService:
    """Chat database service"""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    async def get_or_create_chat(self, telegram_chat: TelegramChat) -> Chat:
        """Get or create chat from Telegram chat"""
        async with self.db_service.get_session() as session:
            # Try to get existing chat
            result = await session.execute(
                select(Chat).where(Chat.telegram_id == telegram_chat.id)
            )
            chat = result.scalar_one_or_none()

            if chat:
                # Update existing chat
                chat.type = telegram_chat.type.value
                chat.title = telegram_chat.title
                chat.username = telegram_chat.username
                chat.first_name = telegram_chat.first_name
                chat.last_name = telegram_chat.last_name
                chat.description = telegram_chat.description
                chat.updated_at = datetime.utcnow()
            else:
                # Create new chat
                chat = Chat(
                    telegram_id=telegram_chat.id,
                    type=telegram_chat.type.value,
                    title=telegram_chat.title,
                    username=telegram_chat.username,
                    first_name=telegram_chat.first_name,
                    last_name=telegram_chat.last_name,
                    description=telegram_chat.description,
                )
                session.add(chat)

            await session.commit()
            await session.refresh(chat)
            return chat

    async def get_chat_by_telegram_id(self, telegram_id: int) -> Optional[Chat]:
        """Get chat by Telegram ID"""
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(Chat).where(Chat.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()

    async def get_active_chats_count(self, days: int = 30) -> int:
        """Get count of active chats in last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(func.count(Chat.id))
                .join(Message)
                .where(Message.created_at >= cutoff_date)
                .distinct()
            )
            return result.scalar()


class MessageService:
    """Message database service"""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    async def save_message(
        self, telegram_message: TelegramMessage, user_id: int, chat_id: int
    ) -> Message:
        """Save message to database"""
        async with self.db_service.get_session() as session:
            message = Message(
                telegram_id=telegram_message.message_id,
                chat_id=chat_id,
                user_id=user_id,
                text=telegram_message.text,
                caption=telegram_message.caption,
                message_type=telegram_message.get_message_type().value,
                media_type=self._get_media_type(telegram_message),
                file_id=self._get_file_id(telegram_message),
                reply_to_message_id=(
                    telegram_message.reply_to_message.message_id
                    if telegram_message.reply_to_message
                    else None
                ),
                entities=(
                    self._serialize_entities(telegram_message.entities)
                    if telegram_message.entities
                    else None
                ),
                metadata=self._extract_metadata(telegram_message),
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message

    async def get_message_by_telegram_id(
        self, telegram_id: int, chat_id: int
    ) -> Optional[Message]:
        """Get message by Telegram ID and chat ID"""
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(Message).where(
                    and_(Message.telegram_id == telegram_id, Message.chat_id == chat_id)
                )
            )
            return result.scalar_one_or_none()

    async def get_chat_messages(
        self, chat_id: int, limit: int = 50, offset: int = 0
    ) -> List[Message]:
        """Get messages from chat with pagination"""
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(Message)
                .where(and_(Message.chat_id == chat_id, Message.is_deleted == False))
                .order_by(Message.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            return result.scalars().all()

    async def get_messages_count(self, chat_id: int, days: int = 30) -> int:
        """Get message count for chat in last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(func.count(Message.id)).where(
                    and_(Message.chat_id == chat_id, Message.created_at >= cutoff_date)
                )
            )
            return result.scalar()

    def _get_media_type(self, message: TelegramMessage) -> Optional[str]:
        """Extract media type from message"""
        if message.photo:
            return "photo"
        elif message.audio:
            return "audio"
        elif message.video:
            return "video"
        elif message.voice:
            return "voice"
        elif message.document:
            return "document"
        elif message.sticker:
            return "sticker"
        elif message.animation:
            return "animation"
        elif message.video_note:
            return "video_note"
        return None

    def _get_file_id(self, message: TelegramMessage) -> Optional[str]:
        """Extract file ID from message"""
        media = getattr(message, self._get_media_type(message), None)
        if media and hasattr(media, "file_id"):
            return media.file_id
        return None

    def _serialize_entities(self, entities: List) -> Optional[List[Dict]]:
        """Serialize message entities"""
        if not entities:
            return None
        return [
            {
                "type": entity.type,
                "offset": entity.offset,
                "length": entity.length,
                "url": getattr(entity, "url", None),
                "user": getattr(entity, "user", None),
            }
            for entity in entities
        ]

    def _extract_metadata(self, message: TelegramMessage) -> Dict[str, Any]:
        """Extract additional metadata from message"""
        metadata = {}

        if message.forward_from:
            metadata["forward_from"] = message.forward_from.to_dict()

        if message.reply_to_message:
            metadata["reply_to"] = {
                "message_id": message.reply_to_message.message_id,
                "text": message.reply_to_message.text,
            }

        if message.location:
            metadata["location"] = {
                "latitude": message.location.latitude,
                "longitude": message.location.longitude,
            }

        return metadata


class ChatMemberService:
    """Chat member database service"""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    async def update_chat_member(
        self, chat_id: int, user_id: int, status: str, **kwargs
    ) -> ChatMember:
        """Update or create chat member"""
        async with self.db_service.get_session() as session:
            # Try to get existing member
            result = await session.execute(
                select(ChatMember).where(
                    and_(ChatMember.chat_id == chat_id, ChatMember.user_id == user_id)
                )
            )
            member = result.scalar_one_or_none()

            if member:
                # Update existing member
                member.status = status
                member.custom_title = kwargs.get("custom_title")
                member.is_anonymous = kwargs.get("is_anonymous", False)
                member.can_manage_chat = kwargs.get("can_manage_chat", False)
                member.can_post_messages = kwargs.get("can_post_messages", False)
                member.can_edit_messages = kwargs.get("can_edit_messages", False)
                member.can_delete_messages = kwargs.get("can_delete_messages", False)
                member.can_restrict_members = kwargs.get("can_restrict_members", False)
                member.can_promote_members = kwargs.get("can_promote_members", False)
                member.can_change_info = kwargs.get("can_change_info", False)
                member.can_invite_users = kwargs.get("can_invite_users", False)
                member.can_pin_messages = kwargs.get("can_pin_messages", False)
                member.updated_at = datetime.utcnow()

                # Handle status changes
                if status == "left" and member.joined_at:
                    member.left_at = datetime.utcnow()
                elif (
                    status in ["member", "administrator", "creator"] and member.left_at
                ):
                    member.left_at = None
            else:
                # Create new member
                member = ChatMember(
                    chat_id=chat_id,
                    user_id=user_id,
                    status=status,
                    custom_title=kwargs.get("custom_title"),
                    is_anonymous=kwargs.get("is_anonymous", False),
                    can_manage_chat=kwargs.get("can_manage_chat", False),
                    can_post_messages=kwargs.get("can_post_messages", False),
                    can_edit_messages=kwargs.get("can_edit_messages", False),
                    can_delete_messages=kwargs.get("can_delete_messages", False),
                    can_restrict_members=kwargs.get("can_restrict_members", False),
                    can_promote_members=kwargs.get("can_promote_members", False),
                    can_change_info=kwargs.get("can_change_info", False),
                    can_invite_users=kwargs.get("can_invite_users", False),
                    can_pin_messages=kwargs.get("can_pin_messages", False),
                    joined_at=(
                        datetime.utcnow() if status not in ["left", "kicked"] else None
                    ),
                    left_at=datetime.utcnow() if status == "left" else None,
                )
                session.add(member)

            await session.commit()
            await session.refresh(member)
            return member

    async def get_chat_members(
        self, chat_id: int, status: Optional[str] = None
    ) -> List[ChatMember]:
        """Get chat members"""
        async with self.db_service.get_session() as session:
            query = select(ChatMember).where(ChatMember.chat_id == chat_id)
            if status:
                query = query.where(ChatMember.status == status)

            result = await session.execute(query)
            return result.scalars().all()

    async def get_chat_admins(self, chat_id: int) -> List[ChatMember]:
        """Get chat administrators"""
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(ChatMember).where(
                    and_(
                        ChatMember.chat_id == chat_id,
                        ChatMember.status.in_(["administrator", "creator"]),
                    )
                )
            )
            return result.scalars().all()


class BotLogService:
    """Bot logging service"""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    async def log(
        self,
        level: str,
        message: str,
        user_id: Optional[int] = None,
        chat_id: Optional[int] = None,
        update_type: Optional[str] = None,
        extra_data: Optional[Dict] = None,
    ):
        """Log bot activity"""
        async with self.db_service.get_session() as session:
            log_entry = BotLog(
                level=level,
                message=message,
                user_id=user_id,
                chat_id=chat_id,
                update_type=update_type,
                extra_data=extra_data,
            )
            session.add(log_entry)
            await session.commit()

    async def get_logs(
        self, level: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[BotLog]:
        """Get logs with filtering"""
        async with self.db_service.get_session() as session:
            query = select(BotLog)
            if level:
                query = query.where(BotLog.level == level)

            query = query.order_by(BotLog.created_at.desc()).limit(limit).offset(offset)

            result = await session.execute(query)
            return result.scalars().all()

    async def cleanup_old_logs(self, days: int = 30):
        """Clean up old logs"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        async with self.db_service.get_session() as session:
            await session.execute(delete(BotLog).where(BotLog.created_at < cutoff_date))
            await session.commit()


class BotStatsService:
    """Bot statistics service"""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    async def update_daily_stats(self, date: datetime = None):
        """Update daily statistics"""
        if date is None:
            date = datetime.utcnow().date()

        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = start_of_day + timedelta(days=1)

        async with self.db_service.get_session() as session:
            # Get existing stats for the day
            result = await session.execute(
                select(BotStats).where(BotStats.date == start_of_day)
            )
            stats = result.scalar_one_or_none()

            # Calculate statistics
            total_users = await session.execute(select(func.count(User.id)))
            active_users = await session.execute(
                select(func.count(User.id)).where(User.last_seen >= start_of_day)
            )

            total_chats = await session.execute(select(func.count(Chat.id)))
            active_chats = await session.execute(
                select(func.count(Chat.id))
                .join(Message)
                .where(Message.created_at >= start_of_day)
                .distinct()
            )

            messages_sent = await session.execute(
                select(func.count(Message.id)).where(
                    and_(
                        Message.created_at >= start_of_day,
                        Message.created_at < end_of_day,
                    )
                )
            )

            commands_used = await session.execute(
                select(func.count(BotLog.id)).where(
                    and_(
                        BotLog.created_at >= start_of_day,
                        BotLog.created_at < end_of_day,
                        BotLog.update_type == "command",
                    )
                )
            )

            errors_count = await session.execute(
                select(func.count(BotLog.id)).where(
                    and_(
                        BotLog.created_at >= start_of_day,
                        BotLog.created_at < end_of_day,
                        BotLog.level == "ERROR",
                    )
                )
            )

            if stats:
                # Update existing stats
                stats.total_users = total_users.scalar()
                stats.active_users = active_users.scalar()
                stats.total_chats = total_chats.scalar()
                stats.active_chats = active_chats.scalar()
                stats.messages_sent = messages_sent.scalar()
                stats.commands_used = commands_used.scalar()
                stats.errors_count = errors_count.scalar()
                stats.updated_at = datetime.utcnow()
            else:
                # Create new stats
                stats = BotStats(
                    date=start_of_day,
                    total_users=total_users.scalar(),
                    active_users=active_users.scalar(),
                    total_chats=total_chats.scalar(),
                    active_chats=active_chats.scalar(),
                    messages_sent=messages_sent.scalar(),
                    commands_used=commands_used.scalar(),
                    errors_count=errors_count.scalar(),
                )
                session.add(stats)

            await session.commit()

    async def get_stats(self, days: int = 30) -> List[BotStats]:
        """Get statistics for last N days"""
        start_date = datetime.utcnow().date() - timedelta(days=days)
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(BotStats)
                .where(BotStats.date >= start_date)
                .order_by(BotStats.date.desc())
            )
            return result.scalars().all()


# Service factory
class ServiceFactory:
    """Factory for creating database services"""

    def __init__(self, database_url: str = None):
        self.db_service = DatabaseService(database_url)
        self._services = {}

    async def initialize(self):
        """Initialize database and services"""
        await self.db_service.initialize()
        await self.db_service.create_tables()

        # Create services
        self._services["user"] = UserService(self.db_service)
        self._services["chat"] = ChatService(self.db_service)
        self._services["message"] = MessageService(self.db_service)
        self._services["chat_member"] = ChatMemberService(self.db_service)
        self._services["log"] = BotLogService(self.db_service)
        self._services["stats"] = BotStatsService(self.db_service)

    def get_service(self, service_name: str):
        """Get a service by name"""
        return self._services.get(service_name)

    async def close(self):
        """Close all services"""
        await self.db_service.close()
