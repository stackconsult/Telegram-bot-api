"""
Agent Manager
"""

import logging
from typing import Dict, List
from agents.base import BaseAgent, AgentMessage, SimpleAgent

logger = logging.getLogger(__name__)

class AgentManager:
    """Manages all agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
    
    async def initialize(self):
        """Initialize agent manager"""
        # Register default agents
        await self.register_agent(SimpleAgent("default"))
        await self.register_agent(SimpleAgent("echo"))
    
    async def register_agent(self, agent: BaseAgent) -> bool:
        """Register an agent"""
        try:
            await agent.start()
            self.agents[agent.name] = agent
            logger.info(f"Agent {agent.name} registered")
            return True
        except Exception as e:
            logger.error(f"Failed to register agent {agent.name}: {e}")
            return False
    
    async def route_message(self, message: AgentMessage) -> List[str]:
        """Route message to all agents"""
        responses = []
        for agent in self.agents.values():
            if agent.is_active:
                try:
                    response = await agent.process_message(message)
                    responses.append(response)
                except Exception as e:
                    logger.error(f"Error in agent {agent.name}: {e}")
        return responses
    
    async def shutdown(self):
        """Shutdown all agents"""
        for agent in self.agents.values():
            await agent.stop()
