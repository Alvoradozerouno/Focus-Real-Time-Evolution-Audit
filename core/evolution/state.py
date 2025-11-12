"""
State Snapshot Management

Captures and manages system state snapshots for evolution tracking.
"""

from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class StateSnapshot:
    """
    Represents a point-in-time snapshot of system state.
    """
    timestamp: str
    state: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    snapshot_id: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert snapshot to dictionary format.
        
        Returns:
            Dictionary representation of snapshot
        """
        return {
            'timestamp': self.timestamp,
            'state': self.state,
            'metadata': self.metadata,
            'snapshot_id': self.snapshot_id
        }
        
    def get_state_value(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a specific state value.
        
        Args:
            key: State key to retrieve
            default: Default value if key not found
            
        Returns:
            State value or default
        """
        return self.state.get(key, default)
