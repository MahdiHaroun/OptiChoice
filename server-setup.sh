#!/bin/bash

# Server setup script for OPC Django application
# This script should be run once on the DigitalOcean droplet

set -e

echo "Starting server setup..."

# Update system packages
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install essential packages
echo "Installing essential packages..."
apt-get install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install Docker
echo "Installing Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
echo "Installing Docker Compose..."
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create application directory
echo "Creating application directory..."
mkdir -p /opt/opc
chown -R root:root /opt/opc

# Enable and start Docker
echo "Enabling and starting Docker..."
systemctl enable docker
systemctl start docker

# Install fail2ban for security
echo "Installing fail2ban..."
apt-get install -y fail2ban

# Configure fail2ban
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-noproxy]
enabled = true
port = http,https
filter = nginx-noproxy
logpath = /var/log/nginx/access.log
maxretry = 2
EOF

# Start fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Configure firewall
echo "Configuring firewall..."
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable

# Create log directory
mkdir -p /var/log/opc

# Set up logrotate for application logs
cat > /etc/logrotate.d/opc << EOF
/var/log/opc/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        docker-compose -f /opt/opc/docker-compose.prod.yml restart web nginx || true
    endscript
}
EOF

# Create a cron job for health checks
echo "Setting up health check cron job..."
cat > /etc/cron.d/opc-health-check << EOF
# Health check every 5 minutes
*/5 * * * * root /opt/opc/health-check.sh >> /var/log/opc/health-check.log 2>&1
EOF

# Clean up
echo "Cleaning up..."
apt-get autoremove -y
apt-get autoclean

echo "Server setup completed successfully!"
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"
echo ""
echo "Next steps:"
echo "1. The server is now ready for deployment"
echo "2. The application will be deployed to /opt/opc"
echo "3. Health checks will run every 5 minutes"
echo "4. Check logs in /var/log/opc/"
