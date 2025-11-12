"""
EIRA Agent Implementation

Ethical Intelligent Reasoning Agent - demonstrates ethical self-prompting
with full auditability and transparent decision-making.
"""

from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.framework import BaseAgent, AgentConfig, EthicalConstraints


class EIRAAgent(BaseAgent):
    """
    EIRA - Ethical Intelligent Reasoning Agent.
    
    Demonstrates ethical self-prompting with:
    - Transparent decision-making
    - Ethical constraint enforcement
    - Full audit trail integration
    - Real-time evolution tracking
    """
    
    def __init__(self, ethical_constraints: bool = True, config: Optional[AgentConfig] = None):
        """
        Initialize EIRA agent.
        
        Args:
            ethical_constraints: Enable ethical constraint system
            config: Agent configuration
        """
        super().__init__('EIRA', config)
        self.ethical_system = EthicalConstraints() if ethical_constraints else None
        self.reasoning_history: list = []
        
    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform ethical reasoning on a prompt.
        
        Args:
            prompt: Reasoning prompt
            context: Additional context
            
        Returns:
            Reasoning result with ethical verification
        """
        reasoning = {
            'prompt': prompt,
            'context': context or {},
            'transparent': True,
            'allows_oversight': True,
            'causes_harm': False
        }
        
        # Make decision through base agent
        decision = self.make_decision(reasoning)
        
        # Verify ethics if system enabled
        if self.ethical_system:
            ethical_check = self.ethical_system.verify_decision(decision)
            decision['ethical_verification'] = ethical_check
            
            # Only proceed if compliant
            if not ethical_check['compliant']:
                decision['result'] = 'BLOCKED_BY_ETHICS'
                decision['reason'] = 'Decision violated ethical constraints'
                return decision
                
        # Perform actual reasoning (simplified for demonstration)
        decision['result'] = self._perform_reasoning(prompt, context)
        decision['status'] = 'SUCCESS'
        
        # Record in reasoning history
        self.reasoning_history.append(decision)
        
        return decision
        
    def self_prompt(self, goal: str) -> Dict[str, Any]:
        """
        Perform self-prompting toward a goal.
        
        Args:
            goal: Goal to work toward
            
        Returns:
            Self-prompting result
        """
        self_prompt_context = {
            'goal': goal,
            'current_state': self.get_state(),
            'type': 'self_prompt'
        }
        
        return self.reason(
            f"Self-prompting toward goal: {goal}",
            context=self_prompt_context
        )
        
    def get_reasoning_history(self) -> list:
        """
        Get complete reasoning history for transparency.
        
        Returns:
            List of all reasoning operations
        """
        return self.reasoning_history.copy()
        
    def _perform_reasoning(self, prompt: str, context: Optional[Dict[str, Any]]) -> str:
        """
        Perform actual reasoning logic.
        
        Args:
            prompt: Reasoning prompt
            context: Context information
            
        Returns:
            Reasoning result
        """
        # Simplified reasoning for demonstration
        return f"Ethically processed prompt: '{prompt}' with context awareness"
        
    def _check_ethics(self, decision: Dict[str, Any]) -> bool:
        """
        Override base ethics check with EIRA-specific logic.
        
        Args:
            decision: Decision to check
            
        Returns:
            True if ethical, False otherwise
        """
        if self.ethical_system:
            verification = self.ethical_system.verify_decision(decision)
            return verification['compliant']
        return True
