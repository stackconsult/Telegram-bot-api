"""
Simple test for Mem0 integration
"""

import os
import asyncio
from mem0 import MemoryClient

async def test_mem0_basic():
    """Test basic Mem0 functionality"""
    
    print("🧠 Testing Mem0 Basic Integration")
    print("=" * 50)
    
    # Initialize Mem0 client
    api_key = os.getenv("MEM0_API_KEY", "m0-QMXKBd6VYUyesXJeGO9HENwV5eaoRRYzayDkV56u")
    client = MemoryClient(api_key=api_key)
    
    try:
        # Test adding memories
        messages = [
            {"role": "user", "content": "Hi, I'm Alex. I'm a vegetarian and I'm allergic to nuts."},
            {"role": "assistant", "content": "Hello Alex! I see that you're a vegetarian with a nut allergy."}
        ]
        
        result = client.add(messages, user_id="alex")
        print(f"✅ Added memory for Alex: {result}")
        
        # Test searching memories
        query = "food"
        filters = {"OR": [{"user_id": "alex"}]}
        
        search_results = client.search(query, version="v2", filters=filters)
        print(f"✅ Search results for '{query}':")
        for i, result in enumerate(search_results):
            print(f"   {i+1}. {result}")
        
        # Test with another user
        messages2 = [
            {"role": "user", "content": "I'm Sam and I love spicy food."},
            {"role": "assistant", "content": "Hi Sam! I'll remember you enjoy spicy cuisine."}
        ]
        
        client.add(messages2, user_id="sam")
        print("✅ Added memory for Sam")
        
        # Search all memories with a query
        all_results = client.search("preferences", version="v2", filters={"OR": [{"user_id": "alex"}, {"user_id": "sam"}]})
        print(f"✅ Found {len(all_results)} memories for 'preferences':")
        
        print("=" * 50)
        print("🎉 Mem0 integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Mem0 Integration Test")
    print("=" * 50)
    
    # Run the test
    success = asyncio.run(test_mem0_basic())
    
    if success:
        print("\n✅ Mem0 is working correctly!")
        print("📝 Ready for integration with Telegram bot")
    else:
        print("\n❌ Mem0 integration failed")
        print("🔧 Check API key and connection")
