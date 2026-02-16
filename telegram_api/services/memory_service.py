"""
Memory integration service using Mem0 AI
Provides persistent memory for Telegram bot conversations
"""

import os
from typing import List, Dict, Any, Optional
from mem0 import MemoryClient
from telegram_api.models.telegram_models import TelegramUser, TelegramMessage
import structlog

logger = structlog.get_logger(__name__)

class MemoryService:
    """Service for managing bot memory using Mem0 AI"""
    
    def __init__(self, api_key: str = None):
        """Initialize memory service with Mem0 API key"""
        self.api_key = api_key or os.getenv("MEM0_API_KEY")
        if not self.api_key:
            raise ValueError("MEM0_API_KEY environment variable is required")
        
        self.client = MemoryClient(api_key=self.api_key)
        logger.info("Memory service initialized", service="mem0")
    
    async def add_conversation_memory(
        self, 
        messages: List[Dict[str, str]], 
        user_id: str
    ) -> Dict[str, Any]:
        """Add conversation to memory"""
        try:
            result = self.client.add(messages, user_id=user_id)
            logger.info("Added conversation memory", user_id=user_id, result=result)
            return result
        except Exception as e:
            logger.error("Failed to add conversation memory", user_id=user_id, error=str(e))
            raise
    
    async def search_memories(
        self, 
        query: str, 
        user_id: str = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search through stored memories"""
        try:
            filters = {}
            if user_id:
                filters = {"OR": [{"user_id": user_id}]}
            
            results = self.client.search(query, version="v2", filters=filters)
            
            # Limit results
            if limit and len(results) > limit:
                results = results[:limit]
            
            logger.info("Searched memories", query=query, user_id=user_id, results_count=len(results))
            return results
        except Exception as e:
            logger.error("Failed to search memories", query=query, user_id=user_id, error=str(e))
            raise
    
    async def get_user_memories(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get all memories for a specific user"""
        try:
            # Search with user filter to get all memories
            results = self.client.search("", version="v2", filters={"OR": [{"user_id": user_id}]})
            
            if limit and len(results) > limit:
                results = results[:limit]
            
            logger.info("Retrieved user memories", user_id=user_id, count=len(results))
            return results
        except Exception as e:
            logger.error("Failed to get user memories", user_id=user_id, error=str(e))
            raise
    
    async def delete_user_memories(self, user_id: str) -> bool:
        """Delete all memories for a specific user"""
        try:
            # Note: Mem0 doesn't have a direct delete method in the basic client
            # This would need to be implemented via API call
            logger.warning("Delete user memories not implemented in Mem0 client", user_id=user_id)
            return False
        except Exception as e:
            logger.error("Failed to delete user memories", user_id=user_id, error=str(e))
            raise
    
    def telegram_message_to_mem0_format(self, message: TelegramMessage) -> Dict[str, str]:
        """Convert Telegram message to Mem0 format"""
        role = "user" if message.from_user and not message.from_user.is_bot else "assistant"
        content = message.text or message.caption or ""
        
        return {
            "role": role,
            "content": content,
            "timestamp": str(message.date) if message.date else None
        }
    
    async def add_telegram_message(
        self, 
        message: TelegramMessage, 
        user_id: str
    ) -> Dict[str, Any]:
        """Add a Telegram message to memory"""
        mem0_message = self.telegram_message_to_mem0_format(message)
        return await self.add_conversation_memory([mem0_message], user_id)
    
    async def add_telegram_conversation(
        self, 
        messages: List[TelegramMessage], 
        user_id: str
    ) -> Dict[str, Any]:
        """Add a conversation of Telegram messages to memory"""
        mem0_messages = [
            self.telegram_message_to_mem0_format(msg) 
            for msg in messages
        ]
        return await self.add_conversation_memory(mem0_messages, user_id)
    
    async def get_context_for_user(self, user_id: str, query: str = None) -> str:
        """Get contextual information for a user"""
        try:
            if query:
                memories = await self.search_memories(query, user_id, limit=3)
            else:
                memories = await self.get_user_memories(user_id, limit=5)
            
            if not memories:
                return "No previous context found."
            
            context_parts = []
            for memory in memories:
                if isinstance(memory, dict) and "memory" in memory:
                    context_parts.append(memory["memory"])
                elif isinstance(memory, str):
                    context_parts.append(memory)
            
            return "\n\n".join(context_parts)
        except Exception as e:
            logger.error("Failed to get context for user", user_id=user_id, error=str(e))
            return "Error retrieving context."

class ConversationMemory:
    """Helper class for managing conversation memory"""
    
    def __init__(self, memory_service: MemoryService):
        self.memory_service = memory_service
        self.conversation_buffer = {}
    
    async def add_message(self, user_id: str, message: TelegramMessage):
        """Add message to conversation buffer"""
        if user_id not in self.conversation_buffer:
            self.conversation_buffer[user_id] = []
        
        self.conversation_buffer[user_id].append(message)
        
        # Add to memory every 5 messages or when conversation ends
        if len(self.conversation_buffer[user_id]) >= 5:
            await self.flush_conversation(user_id)
    
    async def flush_conversation(self, user_id: str):
        """Flush conversation buffer to memory"""
        if user_id in self.conversation_buffer and self.conversation_buffer[user_id]:
            await self.memory_service.add_telegram_conversation(
                self.conversation_buffer[user_id], 
                user_id
            )
            self.conversation_buffer[user_id] = []
    
    async def get_context(self, user_id: str, query: str = None) -> str:
        """Get conversation context for user"""
        return await self.memory_service.get_context_for_user(user_id, query)
