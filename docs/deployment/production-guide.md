# Deployment Guide

## Secure Real-World Deployment of OR1ON

This guide covers deploying OR1ON AI kernel stack in production environments with full security and monitoring.

## Pre-Deployment Checklist

### Security Review
- [ ] All dependencies scanned for vulnerabilities
- [ ] Security configuration reviewed
- [ ] Authentication and authorization configured
- [ ] Encryption enabled (at rest and in transit)
- [ ] Network security rules defined
- [ ] Rate limiting configured
- [ ] Firewall rules established

### Operational Readiness
- [ ] Monitoring configured
- [ ] Alerting rules defined
- [ ] Backup system tested
- [ ] Disaster recovery plan documented
- [ ] Health checks implemented
- [ ] Logging infrastructure ready
- [ ] Incident response procedures documented

### Compliance
- [ ] Audit logging enabled
- [ ] Genesis-level tracking verified
- [ ] Data retention policies configured
- [ ] Privacy controls implemented
- [ ] Compliance reporting tested

## Installation

### System Requirements

**Minimum**:
- CPU: 4 cores
- RAM: 8 GB
- Storage: 50 GB SSD
- Network: 1 Gbps
- OS: Ubuntu 20.04 LTS or newer

**Recommended**:
- CPU: 8+ cores
- RAM: 16+ GB
- Storage: 200+ GB SSD
- Network: 10 Gbps
- OS: Ubuntu 22.04 LTS

### Installation Steps

1. **Clone Repository**:
```bash
git clone https://github.com/Alvoradozerouno/Focus-Real-Time-Evolution-Audit.git
cd Focus-Real-Time-Evolution-Audit
```

2. **Install Dependencies**:
```bash
# Python dependencies (create requirements.txt as needed)
pip install -r requirements.txt
```

3. **Configure System**:
```bash
# Copy configuration templates
cp config/security.yaml config/security.local.yaml
cp config/audit.yaml config/audit.local.yaml
cp config/evolution.yaml config/evolution.local.yaml
cp config/agents.yaml config/agents.local.yaml

# Edit configurations for your environment
nano config/security.local.yaml
# Update: authentication tokens, allowed IPs, etc.
```

4. **Initialize OR1ON Kernel**:
```bash
python core/kernel/init.py
```

5. **Verify Installation**:
```bash
# Run verification script
python -c "
from core.kernel import initialize_kernel
from core.evolution import EvolutionTracker
from core.audit import AuditLogger
from agents.eira import EIRAAgent

components = initialize_kernel()
print('OR1ON kernel initialized successfully')
print(f'Components: {list(components.keys())}')
"
```

## Configuration

### Security Configuration

Edit `config/security.local.yaml`:

```yaml
security:
  authentication:
    enabled: true
    method: token
    token_expiration: 3600
  
  authorization:
    enable_rbac: true
    default_role: viewer
  
  encryption:
    at_rest: true
    in_transit: true
    algorithm: AES256
  
  network:
    enable_firewall: true
    allowed_ips:
      - "YOUR_IP_RANGE"  # Update this!
    rate_limit:
      enabled: true
      max_requests_per_minute: 1000
```

### Audit Configuration

Edit `config/audit.local.yaml`:

```yaml
audit:
  genesis_mode: true
  
  verification:
    enable_verification: true
    algorithm: sha256
  
  logging:
    level: INFO
    log_file: "/var/log/or1on/audit.log"  # Update path
    immutable_storage: true
```

### Environment Variables

Create `.env` file:

```bash
# Environment
OR1ON_ENV=production
OR1ON_DEBUG=false

# Security
OR1ON_SECRET_KEY=your-secret-key-here  # Generate strong key!
OR1ON_API_TOKEN=your-api-token-here    # Generate strong token!

# Database (if using persistent storage)
OR1ON_DB_HOST=localhost
OR1ON_DB_PORT=5432
OR1ON_DB_NAME=or1on
OR1ON_DB_USER=or1on_user
OR1ON_DB_PASSWORD=strong-password-here  # Use strong password!

# Monitoring
OR1ON_METRICS_PORT=9090
OR1ON_HEALTH_CHECK_PORT=8080
```

## Deployment Options

### Option 1: Standalone Server

```bash
# Start OR1ON as a service
python -m core.kernel.init --production

# Or use systemd
sudo cp deployment/or1on.service /etc/systemd/system/
sudo systemctl enable or1on
sudo systemctl start or1on
```

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy application
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run as non-root user
RUN useradd -m or1on
USER or1on

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "from core.kernel import initialize_kernel; initialize_kernel()"

# Start application
CMD ["python", "core/kernel/init.py", "--production"]
```

Build and run:
```bash
docker build -t or1on:latest .
docker run -d \
  --name or1on \
  -p 8080:8080 \
  -p 9090:9090 \
  -v /var/log/or1on:/var/log/or1on \
  -v /data/or1on:/data/or1on \
  --env-file .env \
  or1on:latest
```

### Option 3: Kubernetes Deployment

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: or1on
spec:
  replicas: 3
  selector:
    matchLabels:
      app: or1on
  template:
    metadata:
      labels:
        app: or1on
    spec:
      containers:
      - name: or1on
        image: or1on:latest
        ports:
        - containerPort: 8080
        - containerPort: 9090
        env:
        - name: OR1ON_ENV
          value: "production"
        volumeMounts:
        - name: logs
          mountPath: /var/log/or1on
        - name: data
          mountPath: /data/or1on
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: logs
        persistentVolumeClaim:
          claimName: or1on-logs
      - name: data
        persistentVolumeClaim:
          claimName: or1on-data
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

## Monitoring

### Metrics Collection

Collect key metrics:
- Evolution events per second
- Audit log entries per second
- Ethical constraint violations
- Agent decision latency
- System resource usage

### Alerting Rules

Configure alerts for:
- Ethical constraint violations (CRITICAL)
- Audit integrity failures (CRITICAL)
- High error rates (HIGH)
- Resource exhaustion (HIGH)
- Unusual behavior patterns (MEDIUM)

### Logging

Centralize logs:
```bash
# Configure log aggregation (e.g., ELK Stack)
# All logs include Genesis-level tracking

# View recent audit logs
tail -f /var/log/or1on/audit.log

# View evolution logs
tail -f /var/log/or1on/evolution.log
```

## Backup and Recovery

### Automated Backups

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backups/or1on/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup audit logs (critical!)
cp -r /var/log/or1on/audit.log "$BACKUP_DIR/"

# Backup data
cp -r /data/or1on "$BACKUP_DIR/"

# Backup configuration
cp -r config/*.local.yaml "$BACKUP_DIR/"

# Upload to secure storage
aws s3 sync "$BACKUP_DIR" s3://or1on-backups/
```

### Recovery Procedure

```bash
# Restore from backup
BACKUP_DATE="20240101_120000"  # Specify backup to restore

# Stop service
sudo systemctl stop or1on

# Restore data
aws s3 sync s3://or1on-backups/$BACKUP_DATE /restore/
cp -r /restore/data/or1on /data/
cp -r /restore/*.log /var/log/or1on/

# Verify audit integrity
python -c "
from core.audit import AuditLogger
auditor = AuditLogger(genesis_mode=True)
# Load audit logs
# Verify integrity
assert auditor.verify_integrity()
print('Audit integrity verified')
"

# Restart service
sudo systemctl start or1on
```

## Security Hardening

### Network Security

```bash
# Configure firewall (ufw example)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from YOUR_IP to any port 22
sudo ufw allow from YOUR_IP to any port 8080
sudo ufw enable
```

### Access Control

```bash
# Restrict file permissions
chmod 600 .env
chmod 600 config/*.local.yaml
chmod 700 /data/or1on
chmod 700 /var/log/or1on

# Set ownership
chown -R or1on:or1on /data/or1on
chown -R or1on:or1on /var/log/or1on
```

### Regular Security Updates

```bash
# Update system packages
sudo apt update
sudo apt upgrade

# Update Python dependencies
pip install --upgrade -r requirements.txt

# Scan for vulnerabilities
pip-audit
```

## Troubleshooting

### Common Issues

**Issue**: Audit integrity verification fails
```bash
# Check audit logs
python -c "
from core.audit import AuditLogger
auditor = AuditLogger(genesis_mode=True)
# Load audit trail
print('Integrity check:', auditor.verify_integrity())
print('Audit entries:', len(auditor.audit_trail))
"
```

**Issue**: Evolution tracking not working
```bash
# Verify evolution tracker
python -c "
from core.evolution import EvolutionTracker
tracker = EvolutionTracker()
print('Tracker initialized:', tracker is not None)
print('Genesis timestamp:', tracker.genesis_timestamp)
"
```

**Issue**: Ethical constraints blocking all decisions
```bash
# Review ethical rules
python -c "
from agents.framework import EthicalConstraints
ethics = EthicalConstraints()
print('Active rules:', ethics.get_rules())
"
```

## Support

For deployment issues:
1. Check logs: `/var/log/or1on/`
2. Review configuration files
3. Verify system requirements met
4. Check network connectivity
5. Review security settings

## Next Steps

After successful deployment:
1. Configure monitoring dashboards
2. Set up alerting workflows
3. Train operators on incident response
4. Schedule regular security audits
5. Plan capacity scaling

---

*For production deployments, always consult with security professionals and follow your organization's security policies.*
