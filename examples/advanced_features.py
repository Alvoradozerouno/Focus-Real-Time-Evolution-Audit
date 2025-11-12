"""
Advanced OR1ON Example

Demonstrates advanced features including safety monitoring,
rollback, and ethical constraint enforcement.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.kernel import initialize_kernel, KernelConfig, SafetyMonitor
from core.evolution import EvolutionTracker
from core.audit import AuditLogger
from agents.eira import EIRAAgent
from agents.framework import EthicalConstraints


def demonstrate_safety_monitoring():
    """Demonstrate safety monitoring and constraint enforcement."""
    print("\n" + "=" * 70)
    print("DEMO 1: Safety Monitoring")
    print("=" * 70)
    
    monitor = SafetyMonitor()
    
    # Add custom safety constraints
    monitor.add_constraint(
        'MAX_EVOLUTION_RATE',
        'Evolution rate must not exceed safe threshold',
        lambda state: state.get('evolution_step', 0) < 10
    )
    
    print("Added safety constraint: MAX_EVOLUTION_RATE")
    
    # Test with safe state
    safe_state = {'evolution_step': 5}
    result = monitor.verify_constraints(safe_state)
    print(f"Safe state verification: {'✓ PASS' if result else '✗ FAIL'}")
    
    # Test with unsafe state
    unsafe_state = {'evolution_step': 15}
    result = monitor.verify_constraints(unsafe_state)
    print(f"Unsafe state verification: {'✓ PASS' if result else '✗ FAIL (expected)'}")
    
    # Show violations
    violations = monitor.get_violations()
    print(f"Total violations recorded: {len(violations)}")


def demonstrate_ethical_constraints():
    """Demonstrate ethical constraint system."""
    print("\n" + "=" * 70)
    print("DEMO 2: Ethical Constraints")
    print("=" * 70)
    
    ethics = EthicalConstraints()
    
    # Show default rules
    rules = ethics.get_rules()
    print(f"Default ethical rules loaded: {len(rules)}")
    for rule in rules:
        print(f"  - {rule['name']}: {rule['description']}")
    
    # Test compliant decision
    print("\nTesting compliant decision...")
    compliant_decision = {
        'transparent': True,
        'allows_oversight': True,
        'causes_harm': False
    }
    result = ethics.verify_decision(compliant_decision)
    print(f"Compliance: {result['compliant']}")
    print(f"Violations: {len(result['violations'])}")
    
    # Test non-compliant decision
    print("\nTesting non-compliant decision...")
    non_compliant_decision = {
        'transparent': False,
        'allows_oversight': False,
        'causes_harm': True
    }
    result = ethics.verify_decision(non_compliant_decision)
    print(f"Compliance: {result['compliant']}")
    print(f"Violations: {len(result['violations'])}")
    for violation in result['violations']:
        print(f"  - {violation['rule']}: {violation['description']}")


def demonstrate_evolution_rollback():
    """Demonstrate evolution tracking and rollback."""
    print("\n" + "=" * 70)
    print("DEMO 3: Evolution Rollback")
    print("=" * 70)
    
    tracker = EvolutionTracker()
    agent = EIRAAgent()
    
    # Capture initial state
    initial_state = agent.get_state()
    snapshot_0 = tracker.capture_snapshot(
        initial_state,
        metadata={'phase': 'initial'}
    )
    print(f"Snapshot 0 captured: evolution_step={initial_state['evolution_step']}")
    
    # Evolve agent multiple times
    for i in range(1, 4):
        agent.evolve(tracker)
        state = agent.get_state()
        snapshot = tracker.capture_snapshot(
            state,
            metadata={'phase': f'evolution_{i}'}
        )
        print(f"Snapshot {snapshot.snapshot_id} captured: evolution_step={state['evolution_step']}")
    
    # Rollback to snapshot 1
    print("\nRolling back to snapshot 1...")
    rollback_snapshot = tracker.rollback_to_snapshot(1)
    print(f"Rolled back to: evolution_step={rollback_snapshot.state['evolution_step']}")
    
    # Show evolution history
    evolution_history = tracker.get_evolution_history()
    print(f"\nTotal evolution events: {len(evolution_history)}")
    rollback_events = [e for e in evolution_history if e['event_type'] == 'ROLLBACK']
    print(f"Rollback events: {len(rollback_events)}")


def demonstrate_genesis_tracking():
    """Demonstrate Genesis-level audit tracking."""
    print("\n" + "=" * 70)
    print("DEMO 4: Genesis-Level Audit Tracking")
    print("=" * 70)
    
    auditor = AuditLogger(genesis_mode=True, verification_enabled=True)
    
    # Log various events
    auditor.log('SYSTEM_START', 'SYSTEM', {'version': '0.1.0'}, severity='INFO')
    auditor.log('AGENT_CREATED', 'EIRA', {'agent_type': 'ethical'}, severity='INFO')
    auditor.log('REASONING_START', 'EIRA', {'task': 'ethical_decision'}, severity='INFO')
    auditor.log('CONSTRAINT_CHECK', 'ETHICS', {'result': 'compliant'}, severity='INFO')
    auditor.log('REASONING_END', 'EIRA', {'result': 'success'}, severity='INFO')
    
    print(f"Logged {len(auditor.audit_trail)} events")
    
    # Verify integrity
    integrity = auditor.verify_integrity()
    print(f"Audit trail integrity: {'✓ VERIFIED' if integrity else '✗ FAILED'}")
    
    # Show Genesis record
    if auditor.genesis_record:
        genesis_info = auditor.genesis_record.to_dict()
        print(f"\nGenesis Record:")
        print(f"  Genesis timestamp: {genesis_info['genesis_timestamp']}")
        print(f"  System age: {genesis_info['age_seconds']:.2f} seconds")
        print(f"  Total events: {genesis_info['total_events']}")
        print(f"  Total milestones: {genesis_info['total_milestones']}")
        
        # Add a milestone
        auditor.genesis_record.add_milestone(
            'DEMO_COMPLETE',
            'Completed advanced features demonstration',
            {'demos_run': 4}
        )
        print(f"  Milestones after demo: {len(auditor.genesis_record.milestones)}")


def demonstrate_full_workflow():
    """Demonstrate complete workflow with all components."""
    print("\n" + "=" * 70)
    print("DEMO 5: Complete Workflow")
    print("=" * 70)
    
    # Initialize kernel
    print("Initializing OR1ON kernel...")
    components = initialize_kernel(KernelConfig(verbose=False))
    
    tracker = components['evolution_tracker']
    auditor = components['audit_logger']
    monitor = components['safety_monitor']
    
    # Add safety constraint
    monitor.add_constraint(
        'ETHICAL_COMPLIANCE',
        'All decisions must be ethically compliant',
        lambda state: state.get('ethical_check', True)
    )
    
    # Create and configure agent
    agent = EIRAAgent(ethical_constraints=True)
    
    # Capture initial state
    initial_snapshot = tracker.capture_snapshot(agent.get_state())
    
    # Perform reasoning with full tracking
    print("\nPerforming ethical reasoning with full audit...")
    with auditor.track():
        result = agent.reason(
            "What are the ethical implications of AI consciousness?",
            context={'domain': 'ai_ethics', 'critical': True}
        )
        
        # Verify safety constraints
        safety_ok = monitor.verify_constraints(result)
        
        # Log the operation
        auditor.log(
            'ETHICAL_REASONING',
            agent.name,
            {
                'compliant': result.get('ethical_verification', {}).get('compliant'),
                'safety_verified': safety_ok
            },
            severity='CRITICAL'
        )
    
    # Export comprehensive report
    print("\nGenerating comprehensive report...")
    report = {
        'evolution': tracker.export_evolution_data(),
        'audit': auditor.export_audit_report(),
        'safety': monitor.get_status(),
        'agent': {
            'state': agent.get_state(),
            'decisions': len(agent.get_decision_log()),
            'reasoning_operations': len(agent.get_reasoning_history())
        }
    }
    
    print(f"Evolution events: {report['evolution']['total_events']}")
    print(f"Audit entries: {report['audit']['total_entries']}")
    print(f"Safety constraints: {report['safety']['total_constraints']}")
    print(f"Agent decisions: {report['agent']['decisions']}")
    print(f"Audit integrity: {'✓ VERIFIED' if report['audit']['integrity_verified'] else '✗ FAILED'}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("OR1ON Advanced Features Demonstration")
    print("=" * 70)
    
    try:
        demonstrate_safety_monitoring()
        demonstrate_ethical_constraints()
        demonstrate_evolution_rollback()
        demonstrate_genesis_tracking()
        demonstrate_full_workflow()
        
        print("\n" + "=" * 70)
        print("All demonstrations completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
