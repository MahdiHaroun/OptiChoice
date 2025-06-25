#!/bin/bash

# Server setup script for Digital Ocean droplet
# Run this script on your Digital Ocean server to prepare it for deployment

set -e

echo "=== Setting up Digital Ocean server for OptiChoice ==="

# Update system
echo "Updating system packages..."
apt update && apt upgrade -y

# Install Docker
echo "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
    rm get-docker.sh
    echo "✅ Docker installed successfully"
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose
echo "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed successfully"
else
    echo "✅ Docker Compose already installed"
fi

# Install useful tools
echo "Installing useful tools..."
apt install -y curl wget git nano htop

# Create app directory
echo "Creating application directory..."
mkdir -p /app/optichoice
cd /app/optichoice

# Create production environment file
echo "Creating production environment file..."
cat > .env.prod << 'EOF'
# Django Settings
SECRET_KEY=django-insecure-nrwvf&1*5e0h$^%zy9&1uajyym2%wh*=!%i14u%%v!2ed4v1_)
DEBUG=False
ALLOWED_HOSTS=134.122.70.184,optichoice.com,www.optichoice.com

# Database Settings (for SQLite, no credentials needed, but ready for PostgreSQL/MySQL)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=mahdiharoun44@gmail.com
EMAIL_HOST_PASSWORD=ukpb cfzn eeky tnzo
DEFAULT_FROM_EMAIL=OptiChoice <mahdiharoun44@gmail.com>

# CORS Settings (for React frontend)
CORS_ALLOWED_ORIGINS=http://134.122.70.184:3000,https://optichoice.com,https://www.optichoice.com
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_ALL_ORIGINS=False

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1
JWT_ALGORITHM=HS256

# Security Settings
SESSION_COOKIE_AGE=1209600
EOF

# Set up firewall
echo "Configuring firewall..."
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw --force enable

# Install Nginx (optional)
echo "Installing Nginx..."
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
    echo "✅ Nginx installed successfully"
else
    echo "✅ Nginx already installed"
fi

# Create nginx configuration
echo "Creating Nginx configuration..."
cat > /etc/nginx/sites-available/optichoice << 'EOF'
server {
    listen 80;
    server_name 134.122.70.184 optichoice.com www.optichoice.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable nginx site
ln -sf /etc/nginx/sites-available/optichoice /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo
echo "=== Server setup complete! ==="
echo
echo "Next steps:"
echo "1. The production environment file .env.prod has been created with your settings"
echo "2. Set up your GitHub repository secrets (if using GitHub Actions)"
echo "3. Push your code to trigger the first deployment"
echo
echo "Important files:"
echo "- Production Environment: /app/optichoice/.env.prod"
echo "- Nginx config: /etc/nginx/sites-available/optichoice"
echo "- App directory: /app/optichoice"
echo
echo "Your application will be available at:"
echo "- http://134.122.70.184 (via Nginx)"
echo "- http://134.122.70.184:8000 (direct)"
echo "- http://optichoice.com (when domain is configured)"
echo "- http://www.optichoice.com (when domain is configured)"
