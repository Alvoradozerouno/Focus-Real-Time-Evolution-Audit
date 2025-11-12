"""
Safety Monitor

Enforces constraints and safety rules for the OR1ON kernel.
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime


class SafetyMonitor:
    """
    Monitors system behavior and enforces safety constraints.
    
    Ensures ethical operation and prevents harmful behaviors.
    """
    
    def __init__(self):
        """Initialize safety monitor."""
        self.constraints: List[Dict[str, Any]] = []
        self.violations: List[Dict[str, Any]] = []
        self.checks: List[Callable] = []
        
    def add_constraint(self, name: str, description: str, check_fn: Callable[[Any], bool]):
        """
        Add a safety constraint.
        
        Args:
            name: Constraint name
            description: Human-readable description
            check_fn: Function that returns True if constraint is satisfied
        """
        constraint = {
            'name': name,
            'description': description,
            'check_fn': check_fn,
            'added_at': datetime.utcnow().isoformat()
        }
        self.constraints.append(constraint)
        self.checks.append(check_fn)
        
    def verify_constraints(self, state: Any) -> bool:
        """
        Verify all constraints against current state.
        
        Args:
            state: Current system state to verify
            
        Returns:
            True if all constraints satisfied, False otherwise
        """
        all_satisfied = True
        
        for constraint in self.constraints:
            try:
                satisfied = constraint['check_fn'](state)
                if not satisfied:
                    all_satisfied = False
                    self._record_violation(constraint, state)
            except Exception as e:
                all_satisfied = False
                self._record_violation(constraint, state, error=str(e))
                
        return all_satisfied
        
    def get_violations(self, constraint_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recorded violations.
        
        Args:
            constraint_name: Optional filter by constraint name
            
        Returns:
            List of violations
        """
        if constraint_name:
            return [v for v in self.violations if v['constraint'] == constraint_name]
        return self.violations
        
    def _record_violation(self, constraint: Dict[str, Any], state: Any, error: Optional[str] = None):
        """
        Record a constraint violation.
        
        Args:
            constraint: Violated constraint
            state: State at time of violation
            error: Optional error message
        """
        violation = {
            'timestamp': datetime.utcnow().isoformat(),
            'constraint': constraint['name'],
            'description': constraint['description'],
            'state': str(state),
            'error': error
        }
        self.violations.append(violation)
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get safety monitor status.
        
        Returns:
            Status information
        """
        return {
            'total_constraints': len(self.constraints),
            'total_violations': len(self.violations),
            'constraints': [
                {'name': c['name'], 'description': c['description']}
                for c in self.constraints
            ]
        }
