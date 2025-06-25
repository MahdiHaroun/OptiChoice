# OptiChoice - CI/CD Deployment Guide

This guide explains how to set up continuous deployment for OptiChoice to Digital Ocean using GitHub Actions.

## Prerequisites

1. **Digital Ocean Droplet** with Docker installed
2. **Docker Hub Account** for storing images
3. **GitHub Repository** with the project code

## Setup Instructions

### 1. GitHub Repository Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
DO_HOST=134.122.70.184
DO_USERNAME=root
DO_PASSWORD=BMI$46515M
SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### 2. Docker Hub Setup

1. Create an account on [Docker Hub](https://hub.docker.com/)
2. Create a new repository called `optichoice`
3. Update the GitHub secrets with your Docker Hub credentials

### 3. Server Preparation

SSH into your Digital Ocean droplet and run:

```bash
# Install Docker if not already installed
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create app directory
mkdir -p /app/optichoice
cd /app/optichoice

# Create .env file (you can copy from .env.production and modify)
nano .env
```

### 4. Environment File Setup

Create `/app/optichoice/.env` on your server with the production values:

```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=134.122.70.184,localhost,127.0.0.1

# Email settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Other settings as needed...
```

### 5. Deployment Workflow

The GitHub Action will automatically:

1. **Build** the Docker image when you push to `main` or `master`
2. **Push** the image to Docker Hub
3. **Deploy** to your Digital Ocean droplet
4. **Start** the application

### 6. Manual Deployment (if needed)

You can also deploy manually:

```bash
# On your local machine
docker build -t your-username/optichoice:latest ./OPC
docker push your-username/optichoice:latest

# On the server
cd /app/optichoice
./deploy.sh your-username/optichoice:latest
```

## Monitoring and Maintenance

### Check Application Status
```bash
cd /app/optichoice
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

### Update Application
Push to your main branch and the CI/CD pipeline will handle the update automatically.

### Backup Database
```bash
cd /app/optichoice
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
```

### SSL Setup (Recommended)

Install Nginx and Certbot for SSL:

```bash
apt update
apt install nginx certbot python3-certbot-nginx

# Create Nginx config
cat > /etc/nginx/sites-available/optichoice << 'EOF'
server {
    listen 80;
    server_name 134.122.70.184;  # Replace with your domain

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable the site
ln -s /etc/nginx/sites-available/optichoice /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Get SSL certificate (if you have a domain)
# certbot --nginx -d your-domain.com
```

## Troubleshooting

### Common Issues

1. **Build fails**: Check Docker Hub credentials in GitHub secrets
2. **Deployment fails**: Verify server credentials and Docker installation
3. **App won't start**: Check .env file and Docker logs
4. **Database issues**: Ensure proper permissions and backup exists

### Useful Commands

```bash
# View application logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart application
docker-compose -f docker-compose.prod.yml restart

# Access container shell
docker-compose -f docker-compose.prod.yml exec web bash

# Check Django status
docker-compose -f docker-compose.prod.yml exec web python manage.py check
```

## Security Notes

- Change all default passwords and secret keys
- Use environment variables for sensitive data
- Enable SSL/HTTPS in production
- Regularly update Docker images and dependencies
- Monitor application logs for security issues

## Support

For issues with deployment, check:
1. GitHub Actions logs
2. Docker container logs
3. Server system logs
4. Network connectivity
