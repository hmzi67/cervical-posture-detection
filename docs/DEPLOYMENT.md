# Deployment Guide for Cervical Pose Detection System

## Overview

This guide provides comprehensive instructions for deploying the Cervical Pose Detection System in various environments, from local development to production clinical settings.

## System Requirements

### Hardware Requirements

#### Minimum Requirements

- **CPU**: Intel Core i5-8400 or AMD Ryzen 5 2600
- **RAM**: 8 GB DDR4
- **Storage**: 10 GB available space
- **Camera**: USB webcam with 720p resolution at 30 FPS
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+

#### Recommended Requirements

- **CPU**: Intel Core i7-10700K or AMD Ryzen 7 3700X
- **RAM**: 16 GB DDR4
- **Storage**: 20 GB SSD
- **Camera**: USB webcam with 1080p resolution at 60 FPS
- **OS**: Latest stable versions

#### Clinical Environment Requirements

- **CPU**: Intel Core i7-11700K or better
- **RAM**: 32 GB DDR4
- **Storage**: 100 GB SSD (for session recordings)
- **Camera**: Professional USB camera with 1080p+ resolution
- **Network**: Stable internet connection for updates
- **Display**: Full HD monitor (1920x1080) minimum

### Software Dependencies

#### Core Dependencies

```python
# Production requirements
streamlit>=1.28.0
mediapipe>=0.10.3
opencv-python>=4.8.0
numpy>=1.24.0
Pillow>=10.0.0
plotly>=5.15.0
matplotlib>=3.7.0
```

#### Development Dependencies

```python
# Development and testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
black>=23.7.0
flake8>=6.0.0
mypy>=1.5.0
pre-commit>=3.3.0
```

## Local Development Setup

### Installation Steps

#### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/hmzi67/cervical-posture-detection
cd cervical-pose-detection

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

#### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

#### 3. Configuration

```bash
# Copy configuration template
cp config/settings.template.py config/settings.py

# Edit configuration as needed
nano config/settings.py
```

#### 4. Verify Installation

```bash
# Run basic tests
python -m pytest tests/ -v

# Launch application
streamlit run main.py
```

### Development Workflow

#### Code Quality Checks

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
pre-commit run --all-files
```

#### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test category
pytest tests/test_detection_system.py -v
```

## Production Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Dockerfile

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgstreamer1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Docker Compose

```yaml
version: "3.8"

services:
  cervical-pose-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_ENABLE_CORS=false
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - cervical-pose-app
    restart: unless-stopped
```

#### Deployment Commands

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Update application
docker-compose pull
docker-compose up -d --force-recreate

# Backup data
docker-compose exec cervical-pose-app tar -czf /tmp/backup.tar.gz /app/data
docker cp $(docker-compose ps -q cervical-pose-app):/tmp/backup.tar.gz ./backup.tar.gz
```

### Option 2: Cloud Deployment

#### Azure Container Instances

```bash
# Create resource group
az group create --name cervical-pose-rg --location eastus

# Create container instance
az container create \
  --resource-group cervical-pose-rg \
  --name cervical-pose-app \
  --image your-registry/cervical-pose:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8501 \
  --environment-variables STREAMLIT_SERVER_HEADLESS=true
```

#### AWS ECS Deployment

```json
{
  "family": "cervical-pose-detection",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "cervical-pose-app",
      "image": "your-ecr-repo/cervical-pose:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "STREAMLIT_SERVER_HEADLESS",
          "value": "true"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cervical-pose-detection",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Option 3: Traditional Server Deployment

#### Ubuntu/Debian Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application user
sudo useradd -m -s /bin/bash cervicalpose
sudo usermod -aG sudo cervicalpose

# Setup application
sudo -u cervicalpose -i
git clone <repository-url> /home/cervicalpose/app
cd /home/cervicalpose/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Systemd Service

```ini
[Unit]
Description=Cervical Pose Detection App
After=network.target

[Service]
Type=simple
User=cervicalpose
WorkingDirectory=/home/cervicalpose/app
Environment=PATH=/home/cervicalpose/app/venv/bin
ExecStart=/home/cervicalpose/app/venv/bin/streamlit run main.py --server.port=8501 --server.address=127.0.0.1
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket support
    location /_stcore/stream {
        proxy_pass http://127.0.0.1:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Clinical Environment Setup

### Dedicated Clinical Workstation

#### Hardware Configuration

- **Computer**: High-performance desktop or laptop
- **Camera**: Professional USB camera with manual focus
- **Mount**: Adjustable camera mount for consistent positioning
- **Lighting**: Adequate room lighting (avoid backlighting)
- **Network**: Wired internet connection preferred

#### Software Installation

```bash
# Create dedicated user account
sudo useradd -m clinicaluser
sudo passwd clinicaluser

# Install application for clinical user
sudo -u clinicaluser -i
git clone <repository-url> ~/cervical-pose-app
cd ~/cervical-pose-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create desktop shortcut
cat > ~/Desktop/CervicalPoseDetection.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Cervical Pose Detection
Comment=Clinical cervical exercise assessment
Exec=/home/clinicaluser/cervical-pose-app/venv/bin/streamlit run /home/clinicaluser/cervical-pose-app/main.py
Icon=/home/clinicaluser/cervical-pose-app/assets/icon.png
Terminal=false
Categories=Medical;
EOF
chmod +x ~/Desktop/CervicalPoseDetection.desktop
```

#### Clinical Configuration

```python
# config/clinical_settings.py
CLINICAL_CONFIG = {
    'session_timeout': 1800,  # 30 minutes
    'auto_save_sessions': True,
    'session_storage_path': '/clinical_data/sessions',
    'backup_enabled': True,
    'backup_interval': 300,  # 5 minutes
    'calibration_frames': 20,
    'detection_confidence_threshold': 0.8,
    'enable_audio_feedback': True,
    'enable_progress_tracking': True,
    'patient_privacy_mode': True,
    'hipaa_compliance_logging': True
}
```

### Multi-User Clinical Setup

#### Network Deployment

```bash
# Central server setup
sudo apt install docker docker-compose nginx certbot -y

# Clone application
git clone <repository-url> /opt/cervical-pose-app
cd /opt/cervical-pose-app

# Configure for multi-user
cp docker-compose.clinical.yml docker-compose.yml
docker-compose up -d

# Setup SSL certificate
sudo certbot --nginx -d your-clinical-domain.com
```

#### Load Balancer Configuration

```nginx
upstream cervical_pose_backends {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    listen 443 ssl http2;
    server_name your-clinical-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-clinical-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-clinical-domain.com/privkey.pem;

    location / {
        proxy_pass http://cervical_pose_backends;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Session affinity
        proxy_cookie_path / "/; HTTPOnly; Secure";
    }
}
```

## Security Configuration

### HTTPS Setup

#### Let's Encrypt Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Test renewal
sudo certbot renew --dry-run

# Setup auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

#### Self-Signed Certificate (Development)

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configure Nginx for HTTPS
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### Access Control

#### Basic Authentication

```bash
# Install apache2-utils
sudo apt install apache2-utils

# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd clinician1
sudo htpasswd /etc/nginx/.htpasswd clinician2

# Configure Nginx
location / {
    auth_basic "Clinical Access Required";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://127.0.0.1:8501;
}
```

#### IP Whitelisting

```nginx
# Restrict access to specific IP ranges
location / {
    allow 192.168.1.0/24;  # Internal network
    allow 10.0.0.0/8;      # VPN network
    deny all;

    proxy_pass http://127.0.0.1:8501;
}
```

## Monitoring and Maintenance

### Health Monitoring

#### System Health Check

```bash
#!/bin/bash
# health_check.sh

# Check if application is running
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "Application: HEALTHY"
else
    echo "Application: UNHEALTHY"
    # Restart application
    sudo systemctl restart cervical-pose-app
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2{print $5}' | cut -d'%' -f1)
if [ $DISK_USAGE -gt 80 ]; then
    echo "WARNING: Disk usage at ${DISK_USAGE}%"
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.2f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
    echo "WARNING: Memory usage at ${MEMORY_USAGE}%"
fi
```

#### Automated Monitoring Script

```python
#!/usr/bin/env python3
# monitoring.py

import requests
import psutil
import smtplib
from email.mime.text import MIMEText
import time
import logging

def check_application_health():
    try:
        response = requests.get('http://localhost:8501/_stcore/health', timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_system_resources():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    return {
        'cpu': cpu_percent,
        'memory': memory_percent,
        'disk': disk_percent
    }

def send_alert(message):
    # Configure email settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'alerts@yourdomain.com'
    password = 'your-app-password'

    msg = MIMEText(message)
    msg['Subject'] = 'Cervical Pose Detection System Alert'
    msg['From'] = username
    msg['To'] = 'admin@yourdomain.com'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

def main():
    logging.basicConfig(level=logging.INFO)

    while True:
        # Check application health
        if not check_application_health():
            logging.error("Application health check failed")
            send_alert("Cervical Pose Detection application is not responding")

        # Check system resources
        resources = check_system_resources()

        if resources['cpu'] > 80:
            logging.warning(f"High CPU usage: {resources['cpu']}%")

        if resources['memory'] > 85:
            logging.warning(f"High memory usage: {resources['memory']}%")
            send_alert(f"High memory usage detected: {resources['memory']}%")

        if resources['disk'] > 90:
            logging.error(f"High disk usage: {resources['disk']}%")
            send_alert(f"Critical disk usage: {resources['disk']}%")

        time.sleep(300)  # Check every 5 minutes

if __name__ == '__main__':
    main()
```

### Backup and Recovery

#### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/cervical-pose"
DATE=$(date +"%Y%m%d_%H%M%S")
APP_DIR="/opt/cervical-pose-app"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application data
tar -czf $BACKUP_DIR/app_data_$DATE.tar.gz $APP_DIR/data

# Backup configuration
tar -czf $BACKUP_DIR/app_config_$DATE.tar.gz $APP_DIR/config

# Backup logs
tar -czf $BACKUP_DIR/app_logs_$DATE.tar.gz $APP_DIR/logs

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

# Log backup completion
echo "$(date): Backup completed successfully" >> $BACKUP_DIR/backup.log
```

#### Recovery Procedures

```bash
# Stop application
sudo systemctl stop cervical-pose-app

# Restore from backup
BACKUP_DATE="20240815_143000"
cd /opt/cervical-pose-app

# Restore data
tar -xzf /backups/cervical-pose/app_data_$BACKUP_DATE.tar.gz -C /

# Restore configuration
tar -xzf /backups/cervical-pose/app_config_$BACKUP_DATE.tar.gz -C /

# Restore logs
tar -xzf /backups/cervical-pose/app_logs_$BACKUP_DATE.tar.gz -C /

# Start application
sudo systemctl start cervical-pose-app

# Verify recovery
curl http://localhost:8501/_stcore/health
```

### Updates and Maintenance

#### Update Procedure

```bash
#!/bin/bash
# update.sh

# Backup current version
./backup.sh

# Stop application
sudo systemctl stop cervical-pose-app

# Pull latest changes
cd /opt/cervical-pose-app
git fetch origin
git checkout main
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run database migrations (if any)
python manage.py migrate

# Start application
sudo systemctl start cervical-pose-app

# Verify update
sleep 10
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "Update successful"
else
    echo "Update failed, rolling back"
    # Rollback procedure
    git checkout HEAD~1
    sudo systemctl restart cervical-pose-app
fi
```

#### Maintenance Schedule

```bash
# Add to crontab (crontab -e)

# Daily health check
0 6 * * * /opt/cervical-pose-app/scripts/health_check.sh

# Daily backup
0 2 * * * /opt/cervical-pose-app/scripts/backup.sh

# Weekly log rotation
0 3 * * 0 /usr/sbin/logrotate /etc/logrotate.d/cervical-pose-app

# Monthly system update check
0 4 1 * * /opt/cervical-pose-app/scripts/check_updates.sh

# Quarterly full system maintenance
0 5 1 1,4,7,10 * /opt/cervical-pose-app/scripts/full_maintenance.sh
```

## Troubleshooting

### Common Issues

#### Application Won't Start

```bash
# Check system logs
sudo journalctl -u cervical-pose-app -f

# Check Python environment
source venv/bin/activate
python -c "import streamlit; print('Streamlit OK')"
python -c "import mediapipe; print('MediaPipe OK')"

# Check port availability
sudo netstat -tulpn | grep :8501

# Reset application
sudo systemctl stop cervical-pose-app
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl start cervical-pose-app
```

#### Camera Issues

```bash
# List available cameras
ls /dev/video*

# Test camera access
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('Camera accessible')
    cap.release()
else:
    print('Camera not accessible')
"

# Check permissions
sudo usermod -aG video $USER
```

#### Performance Issues

```bash
# Monitor resource usage
htop

# Check application performance
curl http://localhost:8501/_stcore/health

# Review application logs
tail -f logs/application.log

# Check for memory leaks
python3 -c "
import psutil
import time
process = psutil.Process()
for i in range(10):
    print(f'Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB')
    time.sleep(1)
"
```

### Emergency Recovery

#### Complete System Reset

```bash
#!/bin/bash
# emergency_reset.sh

echo "Starting emergency system reset..."

# Stop all services
sudo systemctl stop cervical-pose-app
sudo systemctl stop nginx

# Backup current state
tar -czf /tmp/emergency_backup_$(date +%s).tar.gz /opt/cervical-pose-app

# Reset to known good state
cd /opt/cervical-pose-app
git reset --hard HEAD
git clean -fd

# Reinstall dependencies
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Reset configuration to defaults
cp config/settings.template.py config/settings.py

# Restart services
sudo systemctl start cervical-pose-app
sudo systemctl start nginx

# Verify system health
sleep 30
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "Emergency reset successful"
else
    echo "Emergency reset failed - manual intervention required"
fi
```

## Support and Maintenance

### Documentation

- **User Manual**: `/docs/USER_GUIDE.md`
- **Clinical Guide**: `/docs/CLINICAL_GUIDE.md`
- **API Documentation**: `/docs/API.md`
- **Testing Guide**: `/docs/TESTING.md`

### Support Contacts

- **Technical Support**: hamzawaheed057@gmail.com
- **Clinical Support**: +92-314-3288112
- **Emergency Contact**: [24/7 Phone]

### Maintenance Schedule

- **Daily**: Automated health checks and backups
- **Weekly**: Log review and system updates
- **Monthly**: Performance optimization and security updates
- **Quarterly**: Full system review and clinical validation updates

---

**Deployment Guide Version**: 1.0  
**Last Updated**: August 2025  
**Deployment Lead**: [Name]  
**Technical Lead**: [Name]
