"""
Telegram API Services

Production-ready services for Telegram bot operations.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json

from telegram import Bot, Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.request import BaseRequest
import httpx

from ..models.telegram_models import (
    TelegramUser,
    TelegramChat,
    TelegramMessage,
    TelegramUpdate,
)
from ..config.settings import settings

logger = logging.getLogger(__name__)


class TelegramAPIService:
    """Service for Telegram API operations"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.TelegramAPIService")
        self._rate_limit_delay = 0.1  # 100ms between requests

    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a message"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send message to {chat_id}: {e}")
            return None

    async def edit_message_text(
        self,
        chat_id: Union[int, str],
        message_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Edit message text"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to edit message {message_id} in {chat_id}: {e}")
            return None

    async def delete_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Delete a message"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
            return True

        except Exception as e:
            self.logger.error(
                f"Failed to delete message {message_id} in {chat_id}: {e}"
            )
            return False

    async def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        disable_notification: Optional[bool] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Forward a message"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.forward_message(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                disable_notification=disable_notification,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to forward message {message_id}: {e}")
            return None

    async def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Copy a message"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to copy message {message_id}: {e}")
            return None

    async def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[str, bytes],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a photo"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send photo to {chat_id}: {e}")
            return None

    async def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[str, bytes],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Optional[Union[str, bytes]] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send an audio file"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_audio(
                chat_id=chat_id,
                audio=audio,
                caption=caption,
                parse_mode=parse_mode,
                duration=duration,
                performer=performer,
                title=title,
                thumb=thumb,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send audio to {chat_id}: {e}")
            return None

    async def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[str, bytes],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a document"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_document(
                chat_id=chat_id,
                document=document,
                caption=caption,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send document to {chat_id}: {e}")
            return None

    async def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[str, bytes],
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[str, bytes]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a video"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_video(
                chat_id=chat_id,
                video=video,
                duration=duration,
                width=width,
                height=height,
                thumb=thumb,
                caption=caption,
                parse_mode=parse_mode,
                supports_streaming=supports_streaming,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send video to {chat_id}: {e}")
            return None

    async def send_voice(
        self,
        chat_id: Union[int, str],
        voice: Union[str, bytes],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a voice message"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_voice(
                chat_id=chat_id,
                voice=voice,
                caption=caption,
                parse_mode=parse_mode,
                duration=duration,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send voice to {chat_id}: {e}")
            return None

    async def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a location"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_location(
                chat_id=chat_id,
                latitude=latitude,
                longitude=longitude,
                horizontal_accuracy=horizontal_accuracy,
                live_period=live_period,
                heading=heading,
                proximity_alert_radius=proximity_alert_radius,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send location to {chat_id}: {e}")
            return None

    async def send_venue(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a venue"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_venue(
                chat_id=chat_id,
                latitude=latitude,
                longitude=longitude,
                title=title,
                address=address,
                foursquare_id=foursquare_id,
                foursquare_type=foursquare_type,
                google_place_id=google_place_id,
                google_place_type=google_place_type,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send venue to {chat_id}: {e}")
            return None

    async def send_contact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a contact"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_contact(
                chat_id=chat_id,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                vcard=vcard,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send contact to {chat_id}: {e}")
            return None

    async def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        open_period: Optional[int] = None,
        close_date: Optional[Union[int, datetime]] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a poll"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                is_anonymous=is_anonymous,
                type=type,
                allows_multiple_answers=allows_multiple_answers,
                correct_option_id=correct_option_id,
                explanation=explanation,
                explanation_parse_mode=explanation_parse_mode,
                open_period=open_period,
                close_date=close_date,
                is_closed=is_closed,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send poll to {chat_id}: {e}")
            return None

    async def send_dice(
        self,
        chat_id: Union[int, str],
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        **kwargs,
    ) -> Optional[TelegramMessage]:
        """Send a dice"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            message = await self.bot.send_dice(
                chat_id=chat_id,
                emoji=emoji,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                **kwargs,
            )

            return TelegramMessage.from_telegram_message(message)

        except Exception as e:
            self.logger.error(f"Failed to send dice to {chat_id}: {e}")
            return None

    async def send_chat_action(self, chat_id: Union[int, str], action: str) -> bool:
        """Send a chat action"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.send_chat_action(chat_id=chat_id, action=action)
            return True

        except Exception as e:
            self.logger.error(f"Failed to send chat action {action} to {chat_id}: {e}")
            return False

    async def get_user_profile_photos(
        self, user_id: int, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Get user's profile photos"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            photos = await self.bot.get_user_profile_photos(
                user_id=user_id, offset=offset, limit=limit
            )

            return {"total_count": photos.total_count, "photos": photos.photos}

        except Exception as e:
            self.logger.error(f"Failed to get profile photos for user {user_id}: {e}")
            return None

    async def get_chat(self, chat_id: Union[int, str]) -> Optional[TelegramChat]:
        """Get chat information"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            chat = await self.bot.get_chat(chat_id=chat_id)
            return TelegramChat.from_telegram_chat(chat)

        except Exception as e:
            self.logger.error(f"Failed to get chat {chat_id}: {e}")
            return None

    async def get_chat_member(
        self, chat_id: Union[int, str], user_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get chat member information"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_id)

            return {
                "user": TelegramUser.from_telegram_user(member.user).to_dict(),
                "status": member.status,
                "custom_title": getattr(member, "custom_title", None),
                "is_anonymous": getattr(member, "is_anonymous", None),
                "can_be_edited": getattr(member, "can_be_edited", None),
                "can_manage_chat": getattr(member, "can_manage_chat", None),
                "can_post_messages": getattr(member, "can_post_messages", None),
                "can_edit_messages": getattr(member, "can_edit_messages", None),
                "can_delete_messages": getattr(member, "can_delete_messages", None),
                "can_manage_video_chats": getattr(
                    member, "can_manage_video_chats", None
                ),
                "can_restrict_members": getattr(member, "can_restrict_members", None),
                "can_promote_members": getattr(member, "can_promote_members", None),
                "can_change_info": getattr(member, "can_change_info", None),
                "can_invite_users": getattr(member, "can_invite_users", None),
                "can_pin_messages": getattr(member, "can_pin_messages", None),
                "can_manage_topics": getattr(member, "can_manage_topics", None),
            }

        except Exception as e:
            self.logger.error(
                f"Failed to get chat member {user_id} from {chat_id}: {e}"
            )
            return None

    async def get_chat_administrators(
        self, chat_id: Union[int, str]
    ) -> Optional[List[Dict[str, Any]]]:
        """Get chat administrators"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            administrators = await self.bot.get_chat_administrators(chat_id=chat_id)

            result = []
            for admin in administrators:
                result.append(
                    {
                        "user": TelegramUser.from_telegram_user(admin.user).to_dict(),
                        "status": admin.status,
                        "custom_title": getattr(admin, "custom_title", None),
                        "is_anonymous": getattr(admin, "is_anonymous", None),
                        "can_be_edited": getattr(admin, "can_be_edited", None),
                        "can_manage_chat": getattr(admin, "can_manage_chat", None),
                        "can_post_messages": getattr(admin, "can_post_messages", None),
                        "can_edit_messages": getattr(admin, "can_edit_messages", None),
                        "can_delete_messages": getattr(
                            admin, "can_delete_messages", None
                        ),
                        "can_manage_video_chats": getattr(
                            admin, "can_manage_video_chats", None
                        ),
                        "can_restrict_members": getattr(
                            admin, "can_restrict_members", None
                        ),
                        "can_promote_members": getattr(
                            admin, "can_promote_members", None
                        ),
                        "can_change_info": getattr(admin, "can_change_info", None),
                        "can_invite_users": getattr(admin, "can_invite_users", None),
                        "can_pin_messages": getattr(admin, "can_pin_messages", None),
                        "can_manage_topics": getattr(admin, "can_manage_topics", None),
                    }
                )

            return result

        except Exception as e:
            self.logger.error(f"Failed to get chat administrators from {chat_id}: {e}")
            return None

    async def get_chat_member_count(self, chat_id: Union[int, str]) -> Optional[int]:
        """Get chat member count"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            count = await self.bot.get_chat_member_count(chat_id=chat_id)
            return count

        except Exception as e:
            self.logger.error(f"Failed to get chat member count from {chat_id}: {e}")
            return None

    async def leave_chat(self, chat_id: Union[int, str]) -> bool:
        """Leave a chat"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.leave_chat(chat_id=chat_id)
            return True

        except Exception as e:
            self.logger.error(f"Failed to leave chat {chat_id}: {e}")
            return False

    async def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        until_date: Optional[Union[int, datetime]] = None,
        revoke_messages: Optional[bool] = None,
    ) -> bool:
        """Ban a chat member"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                until_date=until_date,
                revoke_messages=revoke_messages,
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to ban user {user_id} from {chat_id}: {e}")
            return False

    async def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        only_if_banned: Optional[bool] = None,
    ) -> bool:
        """Unban a chat member"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.unban_chat_member(
                chat_id=chat_id, user_id=user_id, only_if_banned=only_if_banned
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to unban user {user_id} from {chat_id}: {e}")
            return False

    async def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        permissions: Dict[str, Any],
        until_date: Optional[Union[int, datetime]] = None,
    ) -> bool:
        """Restrict a chat member"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=permissions,
                until_date=until_date,
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to restrict user {user_id} in {chat_id}: {e}")
            return False

    async def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        can_change_info: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None,
    ) -> bool:
        """Promote a chat member"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.promote_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                can_change_info=can_change_info,
                can_post_messages=can_post_messages,
                can_edit_messages=can_edit_messages,
                can_delete_messages=can_delete_messages,
                can_invite_users=can_invite_users,
                can_restrict_members=can_restrict_members,
                can_pin_messages=can_pin_messages,
                can_promote_members=can_promote_members,
                can_manage_video_chats=can_manage_video_chats,
                can_manage_topics=can_manage_topics,
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to promote user {user_id} in {chat_id}: {e}")
            return False

    async def set_chat_photo(
        self, chat_id: Union[int, str], photo: Union[str, bytes]
    ) -> bool:
        """Set chat photo"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.set_chat_photo(chat_id=chat_id, photo=photo)
            return True

        except Exception as e:
            self.logger.error(f"Failed to set chat photo for {chat_id}: {e}")
            return False

    async def delete_chat_photo(self, chat_id: Union[int, str]) -> bool:
        """Delete chat photo"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.delete_chat_photo(chat_id=chat_id)
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete chat photo for {chat_id}: {e}")
            return False

    async def set_chat_title(self, chat_id: Union[int, str], title: str) -> bool:
        """Set chat title"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.set_chat_title(chat_id=chat_id, title=title)
            return True

        except Exception as e:
            self.logger.error(f"Failed to set chat title for {chat_id}: {e}")
            return False

    async def set_chat_description(
        self, chat_id: Union[int, str], description: str
    ) -> bool:
        """Set chat description"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.set_chat_description(
                chat_id=chat_id, description=description
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to set chat description for {chat_id}: {e}")
            return False

    async def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        disable_notification: Optional[bool] = None,
    ) -> bool:
        """Pin a message in chat"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.pin_chat_message(
                chat_id=chat_id,
                message_id=message_id,
                disable_notification=disable_notification,
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to pin message {message_id} in {chat_id}: {e}")
            return False

    async def unpin_chat_message(
        self, chat_id: Union[int, str], message_id: Optional[int] = None
    ) -> bool:
        """Unpin a message in chat"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
            return True

        except Exception as e:
            self.logger.error(f"Failed to unpin message {message_id} in {chat_id}: {e}")
            return None

    async def unpin_all_chat_messages(self, chat_id: Union[int, str]) -> bool:
        """Unpin all messages in chat"""
        try:
            await asyncio.sleep(self._rate_limit_delay)

            await self.bot.unpin_all_chat_messages(chat_id=chat_id)
            return True

        except Exception as e:
            self.logger.error(f"Failed to unpin all messages in {chat_id}: {e}")
            return False
