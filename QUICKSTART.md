# Quick Start Guide

Get started with OR1ON - Live-Evolving AI Kernel Stack in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/Alvoradozerouno/Focus-Real-Time-Evolution-Audit.git
cd Focus-Real-Time-Evolution-Audit

# No additional dependencies needed - uses Python standard library!
```

## First Steps

### 1. Initialize the Kernel

```bash
python core/kernel/init.py
```

You should see:
```
============================================================
OR1ON - Live-Evolving AI Kernel Stack
Genesis-Level Auditability for Ethical AI Agents
============================================================

[OR1ON] Evolution tracker initialized
[OR1ON] Audit logger initialized with Genesis mode
[OR1ON] Safety monitor initialized
[OR1ON] Kernel initialized successfully

Kernel Components:
  - Evolution Tracker: ✓
  - Audit Logger: ✓
  - Safety Monitor: ✓

Kernel ready for operation.
```

### 2. Run the Basic Example

```bash
python examples/basic_usage.py
```

This demonstrates:
- Kernel initialization
- EIRA agent creation
- Ethical reasoning
- Evolution tracking
- Audit logging
- Data export

### 3. Explore Advanced Features

```bash
python examples/advanced_features.py
```

This shows:
- Safety monitoring and constraints
- Ethical constraint enforcement
- Evolution rollback capabilities
- Genesis-level audit tracking
- Complete workflow integration

## Basic Usage in Your Code

### Simple Example

```python
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.kernel import initialize_kernel, KernelConfig
from agents.eira import EIRAAgent

# Initialize OR1ON
components = initialize_kernel(KernelConfig(verbose=True))

# Create an ethical agent
agent = EIRAAgent(ethical_constraints=True)

# Perform ethical reasoning
result = agent.reason(
    "How can AI benefit humanity?",
    context={'domain': 'ethics'}
)

print(f"Result: {result['result']}")
print(f"Ethical compliance: {result['ethical_verification']['compliant']}")
```

### With Full Audit Trail

```python
from core.kernel import initialize_kernel
from core.evolution import EvolutionTracker
from core.audit import AuditLogger
from agents.eira import EIRAAgent

# Initialize components
components = initialize_kernel()
tracker = components['evolution_tracker']
auditor = components['audit_logger']

# Create agent
agent = EIRAAgent(ethical_constraints=True)

# Execute with full tracking
with auditor.track():
    # Capture initial state
    initial = tracker.capture_snapshot(agent.get_state())
    
    # Perform reasoning
    result = agent.reason("Ethical decision")
    
    # Log the operation
    auditor.log(
        'REASONING',
        agent.name,
        {'result': result['status']},
        severity='INFO'
    )
    
    # Evolve agent
    agent.evolve(tracker)

# Verify integrity
print(f"Audit integrity: {auditor.verify_integrity()}")
```

## Key Concepts

### Evolution Tracking

Track all system changes:
```python
from core.evolution import EvolutionTracker

tracker = EvolutionTracker()

# Capture snapshots
snapshot = tracker.capture_snapshot(current_state)

# Log evolution events
tracker.log_evolution('EVENT_TYPE', 'Description', data)

# Rollback if needed
tracker.rollback_to_snapshot(snapshot_id)
```

### Audit Logging

Maintain immutable audit trail:
```python
from core.audit import AuditLogger

auditor = AuditLogger(genesis_mode=True)

# Log actions
auditor.log('ACTION', 'ACTOR', details, severity='INFO')

# Verify integrity
is_valid = auditor.verify_integrity()

# Export report
report = auditor.export_audit_report()
```

### Safety Monitoring

Enforce safety constraints:
```python
from core.kernel import SafetyMonitor

monitor = SafetyMonitor()

# Add constraints
monitor.add_constraint(
    'SAFETY_RULE',
    'Description',
    lambda state: check_function(state)
)

# Verify constraints
is_safe = monitor.verify_constraints(current_state)
```

### Ethical Constraints

Ensure ethical behavior:
```python
from agents.framework import EthicalConstraints

ethics = EthicalConstraints()

# Verify decision
result = ethics.verify_decision(decision)

if result['compliant']:
    # Proceed
    pass
else:
    # Handle violations
    print(result['violations'])
```

## Configuration

Customize behavior using YAML configs:

```bash
# Copy templates
cp config/evolution.yaml config/evolution.local.yaml
cp config/audit.yaml config/audit.local.yaml
cp config/agents.yaml config/agents.local.yaml
cp config/security.yaml config/security.local.yaml

# Edit configurations
nano config/*.local.yaml
```

## Next Steps

1. **Read the Documentation**
   - [README.md](README.md) - Full overview
   - [docs/conscious-ai/advancement-tracking.md](docs/conscious-ai/advancement-tracking.md) - Consciousness research
   - [docs/future-aligned/design-principles.md](docs/future-aligned/design-principles.md) - Design patterns
   - [docs/deployment/production-guide.md](docs/deployment/production-guide.md) - Production deployment

2. **Experiment with Examples**
   - Modify `examples/basic_usage.py`
   - Try different scenarios in `examples/advanced_features.py`
   - Create your own examples

3. **Build Your Agent**
   - Extend `BaseAgent` for custom behavior
   - Add custom ethical constraints
   - Implement domain-specific reasoning

4. **Contribute**
   - Read [CONTRIBUTING.md](CONTRIBUTING.md)
   - Open issues for bugs or features
   - Submit pull requests

## Common Use Cases

### Research & Development
- Test consciousness metrics
- Develop new alignment techniques
- Study ethical AI behavior
- Track evolution patterns

### Production Deployment
- Deploy ethical AI agents
- Maintain audit compliance
- Monitor system safety
- Handle real-world scenarios

### Education & Training
- Learn about ethical AI
- Understand alignment challenges
- Practice safe AI development
- Study consciousness research

## Getting Help

- **Documentation**: Check docs/ directory
- **Examples**: Review examples/ directory
- **Issues**: Open a GitHub issue
- **Contributing**: See CONTRIBUTING.md

## Summary

You now know how to:
- ✓ Initialize the OR1ON kernel
- ✓ Create ethical agents
- ✓ Track evolution with snapshots
- ✓ Maintain audit trails
- ✓ Enforce safety constraints
- ✓ Verify ethical compliance

Start building ethical, conscious, and future-aligned AI systems with OR1ON!

---

**Welcome to the future of ethical AI development!**
