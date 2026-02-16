"""
Base Agent System
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentMessage:
    """Agent message structure"""
    sender: str
    content: str
    timestamp: datetime

class BaseAgent(ABC):
    """Base agent class"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_active = False
    
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> str:
        """Process incoming message"""
        pass
    
    async def start(self):
        """Start agent"""
        self.is_active = True
    
    async def stop(self):
        """Stop agent"""
        self.is_active = False

class SimpleAgent(BaseAgent):
    """Simple implementation"""
    
    def __init__(self, name: str):
        super().__init__(name)
    
    async def process_message(self, message: AgentMessage) -> str:
        """Process message with echo response"""
        return f"Agent {self.name} received: {message.content}"
