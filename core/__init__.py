"""
OR1ON Core Kernel Module

Provides the foundation for live-evolving AI with full Genesis-level auditability.
"""

__version__ = "0.1.0"
__author__ = "OR1ON Project"

from .evolution import EvolutionTracker
from .audit import AuditLogger

__all__ = ['EvolutionTracker', 'AuditLogger']
