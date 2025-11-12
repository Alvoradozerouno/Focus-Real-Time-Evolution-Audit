"""
Basic OR1ON Usage Example

Demonstrates core functionality of the OR1ON kernel stack.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.kernel import initialize_kernel, KernelConfig
from core.evolution import EvolutionTracker
from core.audit import AuditLogger
from agents.eira import EIRAAgent


def main():
    """Main example demonstrating OR1ON capabilities."""
    
    print("=" * 70)
    print("OR1ON - Live-Evolving AI Kernel Stack")
    print("Basic Usage Example")
    print("=" * 70)
    print()
    
    # 1. Initialize OR1ON kernel
    print("1. Initializing OR1ON kernel...")
    config = KernelConfig(verbose=True)
    components = initialize_kernel(config)
    print()
    
    # 2. Get components
    tracker = components['evolution_tracker']
    auditor = components['audit_logger']
    
    # 3. Create EIRA agent
    print("2. Creating EIRA agent...")
    agent = EIRAAgent(ethical_constraints=True)
    print(f"   Agent '{agent.name}' created with ethical constraints")
    print()
    
    # 4. Capture initial state
    print("3. Capturing initial state...")
    initial_state = agent.get_state()
    snapshot = tracker.capture_snapshot(
        initial_state,
        metadata={'description': 'Initial agent state'}
    )
    print(f"   Snapshot {snapshot.snapshot_id} captured at {snapshot.timestamp}")
    print()
    
    # 5. Perform ethical reasoning
    print("4. Performing ethical reasoning...")
    result = agent.reason(
        "How can I help humanity while respecting individual autonomy?",
        context={'domain': 'ethics', 'priority': 'high'}
    )
    print(f"   Result: {result.get('result', 'N/A')}")
    print(f"   Status: {result.get('status', 'N/A')}")
    print(f"   Ethical compliance: {result.get('ethical_verification', {}).get('compliant', 'N/A')}")
    print()
    
    # 6. Log evolution event
    print("5. Logging evolution event...")
    tracker.log_evolution(
        'REASONING_COMPLETE',
        'Agent completed ethical reasoning task',
        {'reasoning_id': len(agent.get_reasoning_history())}
    )
    print("   Evolution event logged")
    print()
    
    # 7. Audit logging
    print("6. Recording audit entry...")
    auditor.log(
        'AGENT_REASONING',
        agent.name,
        {
            'prompt': 'ethical reasoning',
            'result_status': result.get('status'),
            'compliant': result.get('ethical_verification', {}).get('compliant')
        },
        severity='INFO'
    )
    print("   Audit entry recorded")
    print()
    
    # 8. Agent evolution
    print("7. Evolving agent...")
    agent.evolve(tracker)
    print(f"   Agent evolved to step {agent.state['evolution_step']}")
    print()
    
    # 9. Verify audit integrity
    print("8. Verifying audit integrity...")
    integrity_ok = auditor.verify_integrity()
    print(f"   Audit integrity: {'✓ VERIFIED' if integrity_ok else '✗ FAILED'}")
    print()
    
    # 10. Export data
    print("9. Exporting data...")
    evolution_data = tracker.export_evolution_data()
    audit_report = auditor.export_audit_report()
    
    print(f"   Evolution events: {evolution_data['total_events']}")
    print(f"   Snapshots: {evolution_data['total_snapshots']}")
    print(f"   Audit entries: {audit_report['total_entries']}")
    print(f"   Genesis timestamp: {evolution_data['genesis_timestamp']}")
    print()
    
    # 11. Demonstrate transparency
    print("10. Demonstrating transparency...")
    decision_log = agent.get_decision_log()
    reasoning_history = agent.get_reasoning_history()
    print(f"   Total decisions logged: {len(decision_log)}")
    print(f"   Total reasoning operations: {len(reasoning_history)}")
    print()
    
    print("=" * 70)
    print("Example completed successfully!")
    print("All operations fully auditable through Genesis-level tracking.")
    print("=" * 70)


if __name__ == '__main__':
    main()
