"""
Agent Framework

Base framework for ethical self-prompting agents.
"""

from .base import BaseAgent, AgentConfig
from .ethics import EthicalConstraints

__all__ = ['BaseAgent', 'AgentConfig', 'EthicalConstraints']
