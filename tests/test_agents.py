"""
Test suite
"""

import pytest
import asyncio
from datetime import datetime

from agents.base import AgentMessage, SimpleAgent
from agents.manager import AgentManager

class TestAgent:
    """Test agent functionality"""
    
    @pytest.mark.asyncio
    async def test_simple_agent(self):
        """Test simple agent"""
        agent = SimpleAgent("test")
        await agent.start()
        
        message = AgentMessage("user", "Hello", datetime.now())
        response = await agent.process_message(message)
        
        assert "Hello" in response
        assert "test" in response
        
        await agent.stop()

class TestAgentManager:
    """Test agent manager"""
    
    @pytest.mark.asyncio
    async def test_agent_manager(self):
        """Test agent manager"""
        manager = AgentManager()
        await manager.initialize()
        
        message = AgentMessage("user", "Test message", datetime.now())
        responses = await manager.route_message(message)
        
        assert len(responses) > 0
        
        await manager.shutdown()

if __name__ == "__main__":
    pytest.main([__file__])
