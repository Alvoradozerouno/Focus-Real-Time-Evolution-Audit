"""
Base Agent Implementation

Foundation for all ethical self-prompting agents.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class AgentConfig:
    """Configuration for agent behavior."""
    enable_ethical_constraints: bool = True
    enable_audit_logging: bool = True
    enable_transparency: bool = True
    max_evolution_steps: int = 1000


class BaseAgent:
    """
    Base class for ethical self-prompting agents.
    
    Provides framework for autonomous operation with ethical constraints,
    transparency, and full auditability.
    """
    
    def __init__(self, name: str, config: Optional[AgentConfig] = None):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            config: Agent configuration
        """
        self.name = name
        self.config = config or AgentConfig()
        self.state: Dict[str, Any] = {
            'initialized_at': datetime.utcnow().isoformat(),
            'evolution_step': 0,
            'status': 'initialized'
        }
        self.decision_log: List[Dict[str, Any]] = []
        
    def make_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a decision based on context.
        
        Args:
            context: Decision context
            
        Returns:
            Decision details
        """
        decision = {
            'timestamp': datetime.utcnow().isoformat(),
            'context': context,
            'agent': self.name,
            'step': self.state['evolution_step']
        }
        
        # Apply ethical constraints if enabled
        if self.config.enable_ethical_constraints:
            decision['ethical_check'] = self._check_ethics(decision)
            
        # Log decision if transparency enabled
        if self.config.enable_transparency:
            self.decision_log.append(decision)
            
        return decision
        
    def evolve(self, evolution_tracker: Optional[Any] = None):
        """
        Evolve agent based on experience and learning.
        
        Args:
            evolution_tracker: Optional evolution tracker for logging
        """
        if self.state['evolution_step'] >= self.config.max_evolution_steps:
            return
            
        self.state['evolution_step'] += 1
        
        if evolution_tracker:
            evolution_tracker.log_evolution(
                'AGENT_EVOLUTION',
                f'{self.name} evolved to step {self.state["evolution_step"]}',
                {'agent': self.name, 'step': self.state['evolution_step']}
            )
            
    def get_state(self) -> Dict[str, Any]:
        """
        Get current agent state.
        
        Returns:
            Current state dictionary
        """
        return self.state.copy()
        
    def get_decision_log(self) -> List[Dict[str, Any]]:
        """
        Get transparent decision log.
        
        Returns:
            List of all decisions made
        """
        return self.decision_log.copy()
        
    def _check_ethics(self, decision: Dict[str, Any]) -> bool:
        """
        Check if decision satisfies ethical constraints.
        
        Args:
            decision: Decision to check
            
        Returns:
            True if ethical, False otherwise
        """
        # Base implementation - override in subclasses
        return True
