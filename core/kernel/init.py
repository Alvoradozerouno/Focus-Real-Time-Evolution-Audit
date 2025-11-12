"""
OR1ON Kernel Initialization

Initialize and configure the OR1ON kernel with all components.
"""

import sys
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

# Add parent directory to path for imports when run as script
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@dataclass
class KernelConfig:
    """Configuration for OR1ON kernel."""
    enable_evolution_tracking: bool = True
    enable_audit_logging: bool = True
    genesis_mode: bool = True
    enable_safety_monitor: bool = True
    verbose: bool = False


def initialize_kernel(config: Optional[KernelConfig] = None) -> Dict[str, Any]:
    """
    Initialize the OR1ON kernel with specified configuration.
    
    Args:
        config: Kernel configuration (uses defaults if None)
        
    Returns:
        Dictionary containing initialized components
    """
    if config is None:
        config = KernelConfig()
        
    components = {
        'config': config,
        'initialized_at': datetime.now(datetime.UTC if hasattr(datetime, 'UTC') else None).replace(tzinfo=None).isoformat(),
        'kernel_version': '0.1.0'
    }
    
    # Initialize evolution tracker
    if config.enable_evolution_tracking:
        from core.evolution import EvolutionTracker
        components['evolution_tracker'] = EvolutionTracker(enable_realtime=True)
        if config.verbose:
            print("[OR1ON] Evolution tracker initialized")
    
    # Initialize audit logger
    if config.enable_audit_logging:
        from core.audit import AuditLogger
        components['audit_logger'] = AuditLogger(
            genesis_mode=config.genesis_mode,
            verification_enabled=True
        )
        components['audit_logger'].log(
            'KERNEL_INIT',
            'SYSTEM',
            {'version': components['kernel_version']},
            severity='INFO'
        )
        if config.verbose:
            print("[OR1ON] Audit logger initialized with Genesis mode")
    
    # Initialize safety monitor
    if config.enable_safety_monitor:
        from core.kernel.monitor import SafetyMonitor
        components['safety_monitor'] = SafetyMonitor()
        if config.verbose:
            print("[OR1ON] Safety monitor initialized")
    
    if config.verbose:
        print(f"[OR1ON] Kernel initialized successfully at {components['initialized_at']}")
        
    return components


if __name__ == '__main__':
    """CLI entry point for kernel initialization."""
    print("=" * 60)
    print("OR1ON - Live-Evolving AI Kernel Stack")
    print("Genesis-Level Auditability for Ethical AI Agents")
    print("=" * 60)
    print()
    
    config = KernelConfig(verbose=True)
    components = initialize_kernel(config)
    
    print()
    print("Kernel Components:")
    print(f"  - Evolution Tracker: {'✓' if 'evolution_tracker' in components else '✗'}")
    print(f"  - Audit Logger: {'✓' if 'audit_logger' in components else '✗'}")
    print(f"  - Safety Monitor: {'✓' if 'safety_monitor' in components else '✗'}")
    print()
    print("Kernel ready for operation.")
