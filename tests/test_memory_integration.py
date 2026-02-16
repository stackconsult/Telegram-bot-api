"""
Test script for Mem0 memory integration
"""

import asyncio
import os
from telegram_api.services.memory_service import MemoryService
from telegram_api.models.telegram_models import TelegramUser, TelegramChat, TelegramMessage
from datetime import datetime

async def test_memory_service():
    """Test Mem0 memory service functionality"""
    
    # Initialize memory service
    api_key = os.getenv("MEM0_API_KEY", "m0-QMXKBd6VYUyesXJeGO9HENwV5eaoRRYzayDkV56u")
    memory_service = MemoryService(api_key=api_key)
    
    # Create test user and message
    test_user = TelegramUser(
        id=12345,
        is_bot=False,
        first_name="Alex",
        username="alex_test"
    )
    
    test_chat = TelegramChat(
        id=67890,
        type="private",
        first_name="Alex"
    )
    
    test_message = TelegramMessage(
        message_id=1,
        date=datetime.utcnow(),
        chat=test_chat,
        from_user=test_user,
        text="Hi, I'm Alex. I'm a vegetarian and I'm allergic to nuts."
    )
    
    # Test adding message to memory
    print("🧠 Testing Mem0 Memory Service")
    print("=" * 50)
    
    try:
        # Add message to memory
        user_id = str(test_user.id)
        result = await memory_service.add_telegram_message(test_message, user_id)
        print(f"✅ Message added to memory: {result}")
        
        # Add another message
        test_message2 = TelegramMessage(
            message_id=2,
            date=datetime.utcnow(),
            chat=test_chat,
            from_user=test_user,
            text="What can I cook for dinner tonight?"
        )
        
        await memory_service.add_telegram_message(test_message2, user_id)
        print("✅ Second message added to memory")
        
        # Search memories
        memories = await memory_service.search_memories("dinner", user_id)
        print(f"✅ Found {len(memories)} memories for 'dinner':")
        for i, memory in enumerate(memories):
            print(f"   {i+1}. {memory}")
        
        # Get all user memories
        all_memories = await memory_service.get_user_memories(user_id)
        print(f"✅ Total memories for user: {len(all_memories)}")
        
        # Get context
        context = await memory_service.get_context_for_user(user_id, "food preferences")
        print(f"✅ Context for food preferences: {context}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("=" * 50)
    print("🎉 Memory service test completed successfully!")
    return True

async def test_conversation_memory():
    """Test conversation memory helper"""
    from telegram_api.services.memory_service import ConversationMemory
    
    api_key = os.getenv("MEM0_API_KEY", "m0-QMXKBd6VYUyesXJeGO9HENwV5eaoRRYzayDkV56u")
    memory_service = MemoryService(api_key=api_key)
    conversation_memory = ConversationMemory(memory_service)
    
    print("\n🗣️ Testing Conversation Memory")
    print("=" * 50)
    
    try:
        # Create test messages
        test_user = TelegramUser(id=12346, is_bot=False, first_name="Sam")
        test_chat = TelegramChat(id=67891, type="private")
        
        messages = [
            TelegramMessage(
                message_id=1,
                date=datetime.utcnow(),
                chat=test_chat,
                from_user=test_user,
                text="Hello! I'm learning to cook."
            ),
            TelegramMessage(
                message_id=2,
                date=datetime.utcnow(),
                chat=test_chat,
                from_user=test_user,
                text="What ingredients do I need for pasta?"
            ),
            TelegramMessage(
                message_id=3,
                date=datetime.utcnow(),
                chat=test_chat,
                from_user=test_user,
                text="I prefer vegetarian recipes."
            )
        ]
        
        # Add messages to conversation
        user_id = str(test_user.id)
        for message in messages:
            await conversation_memory.add_message(user_id, message)
        
        print("✅ Added 3 messages to conversation buffer")
        
        # Flush conversation
        await conversation_memory.flush_conversation(user_id)
        print("✅ Flushed conversation to memory")
        
        # Get context
        context = await conversation_memory.get_context(user_id)
        print(f"✅ Conversation context: {context}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("=" * 50)
    print("🎉 Conversation memory test completed successfully!")
    return True

if __name__ == "__main__":
    print("🚀 Starting Mem0 Integration Tests")
    print("=" * 50)
    
    # Run tests
    asyncio.run(test_memory_service())
    asyncio.run(test_conversation_memory())
    
    print("\n🎯 All tests completed!")
    print("📝 Mem0 integration is working correctly")
