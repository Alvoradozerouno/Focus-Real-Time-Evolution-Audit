"""
Audit Logger Implementation

Maintains immutable audit logs with cryptographic verification.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from .genesis import GenesisRecord


class AuditLogger:
    """
    Genesis-level audit logger with cryptographic verification.
    
    Maintains complete, immutable audit trail from system inception.
    """
    
    def __init__(self, genesis_mode: bool = True, verification_enabled: bool = True):
        """
        Initialize audit logger.
        
        Args:
            genesis_mode: Enable Genesis-level tracking from inception
            verification_enabled: Enable cryptographic verification
        """
        self.genesis_mode = genesis_mode
        self.verification_enabled = verification_enabled
        self.audit_trail: List[Dict[str, Any]] = []
        self.genesis_record = GenesisRecord() if genesis_mode else None
        
    def log(self, 
            action: str, 
            actor: str, 
            details: Optional[Dict[str, Any]] = None,
            severity: str = 'INFO'):
        """
        Log an auditable action.
        
        Args:
            action: Action being performed
            actor: Entity performing the action
            details: Additional details about the action
            severity: Severity level (INFO, WARNING, CRITICAL)
        """
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'actor': actor,
            'details': details or {},
            'severity': severity,
            'sequence': len(self.audit_trail)
        }
        
        # Add cryptographic hash if verification enabled
        if self.verification_enabled:
            entry['hash'] = self._compute_hash(entry)
            if self.audit_trail:
                entry['prev_hash'] = self.audit_trail[-1].get('hash', '')
        
        self.audit_trail.append(entry)
        
        # Update genesis record if in genesis mode
        if self.genesis_record:
            self.genesis_record.record_event(entry)
            
    def verify_integrity(self) -> bool:
        """
        Verify the integrity of the audit trail.
        
        Returns:
            True if audit trail is intact, False otherwise
        """
        if not self.verification_enabled:
            return True
            
        for i, entry in enumerate(self.audit_trail):
            # Verify hash
            expected_hash = self._compute_hash(entry)
            if entry.get('hash') != expected_hash:
                return False
                
            # Verify chain
            if i > 0:
                prev_hash = self.audit_trail[i-1].get('hash', '')
                if entry.get('prev_hash') != prev_hash:
                    return False
                    
        return True
        
    def get_audit_trail(self, 
                       actor: Optional[str] = None,
                       action: Optional[str] = None,
                       severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve audit trail with optional filtering.
        
        Args:
            actor: Filter by actor
            action: Filter by action
            severity: Filter by severity level
            
        Returns:
            Filtered audit trail
        """
        results = self.audit_trail
        
        if actor:
            results = [e for e in results if e['actor'] == actor]
        if action:
            results = [e for e in results if e['action'] == action]
        if severity:
            results = [e for e in results if e['severity'] == severity]
            
        return results
        
    def export_audit_report(self) -> Dict[str, Any]:
        """
        Export complete audit report.
        
        Returns:
            Comprehensive audit report
        """
        report = {
            'genesis_mode': self.genesis_mode,
            'verification_enabled': self.verification_enabled,
            'total_entries': len(self.audit_trail),
            'integrity_verified': self.verify_integrity(),
            'audit_trail': self.audit_trail
        }
        
        if self.genesis_record:
            report['genesis_record'] = self.genesis_record.to_dict()
            
        return report
        
    @contextmanager
    def track(self):
        """
        Context manager for tracking operations.
        
        Usage:
            with auditor.track():
                # perform operations
        """
        self.log('TRACKING_START', 'SYSTEM', {'context': 'track'})
        try:
            yield self
        finally:
            self.log('TRACKING_END', 'SYSTEM', {'context': 'track'})
            
    def _compute_hash(self, entry: Dict[str, Any]) -> str:
        """
        Compute cryptographic hash for an entry.
        
        Args:
            entry: Audit entry to hash
            
        Returns:
            SHA-256 hash of entry
        """
        # Create a copy without the hash field
        entry_copy = {k: v for k, v in entry.items() if k not in ['hash', 'prev_hash']}
        entry_json = json.dumps(entry_copy, sort_keys=True)
        return hashlib.sha256(entry_json.encode()).hexdigest()
