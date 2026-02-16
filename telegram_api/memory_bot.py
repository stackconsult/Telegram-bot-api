"""
Enhanced bot core with memory integration
"""

import os
from telegram_api.core import TelegramBot as BaseTelegramBot, BotConfig
from telegram_api.services.memory_service import MemoryService
from telegram_api.handlers.memory_message_handler import MessageHandler
import structlog

logger = structlog.get_logger(__name__)

class TelegramBot(BaseTelegramBot):
    """Enhanced Telegram bot with memory integration"""
    
    def __init__(self, config: BotConfig):
        super().__init__(config)
        self.memory_service = None
        self._initialize_memory_service()
    
    def _initialize_memory_service(self):
        """Initialize Mem0 memory service"""
        try:
            mem0_api_key = os.getenv("MEM0_API_KEY")
            if mem0_api_key:
                self.memory_service = MemoryService(api_key=mem0_api_key)
                
                # Replace message handler with memory-enabled version
                self.message_handler = MessageHandler(
                    self, 
                    self.api_service, 
                    self.memory_service
                )
                
                logger.info("Memory service initialized successfully")
            else:
                logger.warning("MEM0_API_KEY not found, memory features disabled")
        except Exception as e:
            logger.error("Failed to initialize memory service", error=str(e))
    
    async def get_user_context(self, user_id: str, query: str = None) -> str:
        """Get conversation context for a user"""
        if not self.memory_service:
            return "Memory service not available."
        
        try:
            return await self.memory_service.get_context_for_user(user_id, query)
        except Exception as e:
            logger.error("Failed to get user context", user_id=user_id, error=str(e))
            return "Error retrieving context."
    
    async def remember_conversation(self, user_id: str, messages: list):
        """Store a conversation in memory"""
        if not self.memory_service:
            return False
        
        try:
            await self.memory_service.add_conversation_memory(messages, user_id)
            logger.info("Conversation stored in memory", user_id=user_id)
            return True
        except Exception as e:
            logger.error("Failed to store conversation", user_id=user_id, error=str(e))
            return False
