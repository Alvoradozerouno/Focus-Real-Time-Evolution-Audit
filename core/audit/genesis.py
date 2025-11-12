"""
Genesis Record Management

Tracks system history from inception (Genesis).
"""

from datetime import datetime
from typing import Dict, List, Any, Optional


class GenesisRecord:
    """
    Maintains record of system from Genesis (inception).
    
    Provides complete historical tracking and reconstruction capabilities.
    """
    
    def __init__(self):
        """Initialize Genesis record."""
        self.genesis_timestamp = datetime.utcnow().isoformat()
        self.events: List[Dict[str, Any]] = []
        self.milestones: List[Dict[str, Any]] = []
        
    def record_event(self, event: Dict[str, Any]):
        """
        Record a Genesis-level event.
        
        Args:
            event: Event data to record
        """
        self.events.append({
            'genesis_offset': (datetime.utcnow() - datetime.fromisoformat(self.genesis_timestamp)).total_seconds(),
            'event': event
        })
        
    def add_milestone(self, name: str, description: str, data: Optional[Dict[str, Any]] = None):
        """
        Add a significant milestone to Genesis record.
        
        Args:
            name: Milestone name
            description: Milestone description
            data: Additional milestone data
        """
        milestone = {
            'timestamp': datetime.utcnow().isoformat(),
            'genesis_offset': (datetime.utcnow() - datetime.fromisoformat(self.genesis_timestamp)).total_seconds(),
            'name': name,
            'description': description,
            'data': data or {}
        }
        self.milestones.append(milestone)
        
    def reconstruct_state(self, target_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Reconstruct system state at a specific point in time.
        
        Args:
            target_time: ISO timestamp to reconstruct to (None = current)
            
        Returns:
            Reconstructed state information
        """
        if target_time is None:
            relevant_events = self.events
        else:
            target_dt = datetime.fromisoformat(target_time)
            relevant_events = [
                e for e in self.events 
                if datetime.fromisoformat(e['event']['timestamp']) <= target_dt
            ]
            
        return {
            'genesis_timestamp': self.genesis_timestamp,
            'reconstruction_time': target_time or datetime.utcnow().isoformat(),
            'event_count': len(relevant_events),
            'milestones': [m for m in self.milestones if target_time is None or m['timestamp'] <= target_time],
            'events': relevant_events
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Export Genesis record to dictionary.
        
        Returns:
            Dictionary representation of Genesis record
        """
        return {
            'genesis_timestamp': self.genesis_timestamp,
            'total_events': len(self.events),
            'total_milestones': len(self.milestones),
            'milestones': self.milestones,
            'age_seconds': (datetime.utcnow() - datetime.fromisoformat(self.genesis_timestamp)).total_seconds()
        }
