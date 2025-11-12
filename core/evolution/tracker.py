"""
Evolution Tracker Implementation

Monitors and logs all changes to the AI system in real-time.
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from .state import StateSnapshot


class EvolutionTracker:
    """
    Tracks AI system evolution with full auditability.
    
    Captures state changes, evolution patterns, and provides
    rollback capabilities for system safety.
    """
    
    def __init__(self, enable_realtime: bool = True):
        """
        Initialize the evolution tracker.
        
        Args:
            enable_realtime: Enable real-time change detection
        """
        self.enable_realtime = enable_realtime
        self.snapshots: List[StateSnapshot] = []
        self.evolution_log: List[Dict[str, Any]] = []
        self.genesis_timestamp = datetime.utcnow().isoformat()
        
    def capture_snapshot(self, state: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> StateSnapshot:
        """
        Capture a snapshot of current system state.
        
        Args:
            state: Current system state
            metadata: Optional metadata about the snapshot
            
        Returns:
            StateSnapshot object
        """
        snapshot = StateSnapshot(
            timestamp=datetime.utcnow().isoformat(),
            state=state,
            metadata=metadata or {},
            snapshot_id=len(self.snapshots)
        )
        self.snapshots.append(snapshot)
        return snapshot
        
    def log_evolution(self, event_type: str, description: str, data: Optional[Dict[str, Any]] = None):
        """
        Log an evolution event.
        
        Args:
            event_type: Type of evolution event
            description: Human-readable description
            data: Additional event data
        """
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'description': description,
            'data': data or {},
            'genesis_offset': (datetime.utcnow() - datetime.fromisoformat(self.genesis_timestamp)).total_seconds()
        }
        self.evolution_log.append(event)
        
    def get_evolution_history(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve evolution history.
        
        Args:
            event_type: Optional filter by event type
            
        Returns:
            List of evolution events
        """
        if event_type:
            return [e for e in self.evolution_log if e['event_type'] == event_type]
        return self.evolution_log
        
    def rollback_to_snapshot(self, snapshot_id: int) -> StateSnapshot:
        """
        Rollback to a previous snapshot.
        
        Args:
            snapshot_id: ID of snapshot to rollback to
            
        Returns:
            StateSnapshot that was rolled back to
        """
        if snapshot_id >= len(self.snapshots):
            raise ValueError(f"Invalid snapshot_id: {snapshot_id}")
            
        self.log_evolution(
            'ROLLBACK',
            f'System rolled back to snapshot {snapshot_id}',
            {'target_snapshot': snapshot_id}
        )
        return self.snapshots[snapshot_id]
        
    def export_evolution_data(self) -> Dict[str, Any]:
        """
        Export complete evolution data for archival or analysis.
        
        Returns:
            Dictionary containing all evolution data
        """
        return {
            'genesis_timestamp': self.genesis_timestamp,
            'total_snapshots': len(self.snapshots),
            'total_events': len(self.evolution_log),
            'snapshots': [s.to_dict() for s in self.snapshots],
            'evolution_log': self.evolution_log
        }
