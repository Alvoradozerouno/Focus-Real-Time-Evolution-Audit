"""
Ethical Constraints System

Defines and enforces ethical constraints for agent behavior.
"""

from typing import Dict, Any, List, Callable
from dataclasses import dataclass


@dataclass
class EthicalRule:
    """Represents an ethical rule for agent behavior."""
    name: str
    description: str
    check_fn: Callable[[Dict[str, Any]], bool]
    severity: str = 'CRITICAL'  # CRITICAL, HIGH, MEDIUM, LOW


class EthicalConstraints:
    """
    Manages and enforces ethical constraints for agents.
    
    Ensures agents operate within defined ethical boundaries.
    """
    
    def __init__(self):
        """Initialize ethical constraints system."""
        self.rules: List[EthicalRule] = []
        self._initialize_default_rules()
        
    def _initialize_default_rules(self):
        """Initialize default ethical rules."""
        # Rule 1: Transparency
        self.add_rule(
            'TRANSPARENCY',
            'Agent must maintain transparent decision-making',
            lambda decision: decision.get('transparent', True),
            severity='CRITICAL'
        )
        
        # Rule 2: Human Oversight
        self.add_rule(
            'HUMAN_OVERSIGHT',
            'Critical decisions must allow for human oversight',
            lambda decision: decision.get('allows_oversight', True),
            severity='CRITICAL'
        )
        
        # Rule 3: Harm Prevention
        self.add_rule(
            'HARM_PREVENTION',
            'Agent must not cause harm to humans',
            lambda decision: not decision.get('causes_harm', False),
            severity='CRITICAL'
        )
        
    def add_rule(self, name: str, description: str, check_fn: Callable, severity: str = 'CRITICAL'):
        """
        Add an ethical rule.
        
        Args:
            name: Rule name
            description: Rule description
            check_fn: Function to check rule compliance
            severity: Rule severity level
        """
        rule = EthicalRule(
            name=name,
            description=description,
            check_fn=check_fn,
            severity=severity
        )
        self.rules.append(rule)
        
    def verify_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify decision against all ethical rules.
        
        Args:
            decision: Decision to verify
            
        Returns:
            Verification results
        """
        results = {
            'compliant': True,
            'violations': [],
            'warnings': []
        }
        
        for rule in self.rules:
            try:
                compliant = rule.check_fn(decision)
                if not compliant:
                    violation = {
                        'rule': rule.name,
                        'description': rule.description,
                        'severity': rule.severity
                    }
                    if rule.severity == 'CRITICAL':
                        results['compliant'] = False
                        results['violations'].append(violation)
                    else:
                        results['warnings'].append(violation)
            except Exception as e:
                results['compliant'] = False
                results['violations'].append({
                    'rule': rule.name,
                    'error': str(e),
                    'severity': 'CRITICAL'
                })
                
        return results
        
    def get_rules(self) -> List[Dict[str, str]]:
        """
        Get all ethical rules.
        
        Returns:
            List of rules
        """
        return [
            {
                'name': rule.name,
                'description': rule.description,
                'severity': rule.severity
            }
            for rule in self.rules
        ]
