"""
Enhanced message handler with memory integration
"""

import structlog
from telegram_api.handlers.message_handler import MessageHandler as BaseMessageHandler
from telegram_api.services.memory_service import MemoryService, ConversationMemory
from telegram_api.models.telegram_models import TelegramUpdate, TelegramMessage

logger = structlog.get_logger(__name__)

class MessageHandler(BaseMessageHandler):
    """Enhanced message handler with memory integration"""
    
    def __init__(self, bot, api_service, memory_service: MemoryService = None):
        super().__init__(bot, api_service)
        self.memory_service = memory_service
        self.conversation_memory = ConversationMemory(memory_service) if memory_service else None
    
    async def handle(self, update: TelegramUpdate, context):
        """Handle message with memory integration"""
        if not update.message:
            return False
        
        # Store message in memory if service is available
        if self.memory_service and update.message.from_user:
            try:
                user_id = str(update.message.from_user.id)
                await self.conversation_memory.add_message(user_id, update.message)
                logger.info("Message stored in memory", user_id=user_id)
            except Exception as e:
                logger.error("Failed to store message in memory", error=str(e))
        
        # Handle the message normally
        return await super().handle(update, context)
    
    async def get_context_for_user(self, user_id: str, query: str = None) -> str:
        """Get conversation context for user"""
        if not self.conversation_memory:
            return "Memory service not available."
        
        try:
            return await self.conversation_memory.get_context(user_id, query)
        except Exception as e:
            logger.error("Failed to get context", user_id=user_id, error=str(e))
            return "Error retrieving context."
