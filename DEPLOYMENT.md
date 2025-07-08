# OPC Django Application Deployment Guide

## Overview

This guide covers the deployment of the OPC Django application to a DigitalOcean droplet using Docker containers and GitHub Actions for CI/CD.

## Prerequisites

- DigitalOcean droplet with Ubuntu 20.04 or later
- GitHub repository with the application code
- GitHub Secrets configured for deployment

## Server Setup

### 1. Initial Server Setup

Run the server setup script on your DigitalOcean droplet:

```bash
chmod +x server-setup.sh
./server-setup.sh
```

This script will:

- Update system packages
- Install Docker and Docker Compose
- Configure firewall (UFW)
- Install fail2ban for security
- Set up logging and log rotation
- Create health check cron job

### 2. GitHub Secrets Configuration

Configure the following secrets in your GitHub repository:

- `DROPLET_HOST`: 46.101.145.147
- `DROPLET_USERNAME`: root
- `DROPLET_PASSWORD`: BMI$46515M

**Note**: Using password authentication. For better security, consider setting up SSH key authentication later.

## Deployment Process

### Automatic Deployment (Recommended)

The application automatically deploys on every push to the main/master branch via GitHub Actions.

### Manual Deployment

You can also trigger deployment manually:

1. Go to your GitHub repository
2. Click on "Actions"
3. Select "Rebuild and Deploy to DigitalOcean"
4. Click "Run workflow"
5. Choose between regular or full deployment

## Application Architecture

### Services

- **Web**: Django application running with Gunicorn
- **Database**: SQLite database (file-based)
- **Nginx**: Reverse proxy and static file server

### Ports

- **80**: HTTP (handled by Nginx)
- **443**: HTTPS (handled by Nginx)
- **8000**: Django application (internal)

## File Structure

```
/opt/opc/
├── docker-compose.prod.yml
├── nginx.conf
├── .env.production
├── deploy.sh
├── deploy-prod.sh
├── health-check.sh
└── django.tar (temporary)
```

## Environment Variables

### Production Environment (.env.production)

```
SECRET_KEY=your-very-secure-secret-key-for-production
DEBUG=False
ALLOWED_HOSTS=46.101.145.147,localhost,127.0.0.1,your-domain.com

# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static/Media Files
STATIC_URL=/static/
STATIC_ROOT=/app/static
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
```

## Deployment Commands

### Start Services

```bash
cd /opt/opc
docker-compose -f docker-compose.prod.yml up -d
```

### Stop Services

```bash
cd /opt/opc
docker-compose -f docker-compose.prod.yml down
```

### View Logs

```bash
cd /opt/opc
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f nginx
docker-compose -f docker-compose.prod.yml logs -f db
```

### Check Service Status

```bash
cd /opt/opc
docker-compose -f docker-compose.prod.yml ps
```

## Health Monitoring

### Health Check Endpoint

The application provides a health check endpoint at `/health/` that returns HTTP 200 with "healthy" response.

### Automated Health Checks

Health checks run every 5 minutes via cron job. Check logs:

```bash
tail -f /var/log/opc/health-check.log
```

### Manual Health Check

```bash
cd /opt/opc
./health-check.sh
```

## Database Management

### Access Database

```bash
docker-compose -f docker-compose.prod.yml exec db psql -U opc_user -d opc_db
```

### Backup Database

```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U opc_user opc_db > backup.sql
```

### Restore Database

```bash
docker-compose -f docker-compose.prod.yml exec -T db psql -U opc_user opc_db < backup.sql
```

## Security Features

### Fail2ban Protection

- SSH brute force protection
- Nginx bad bot protection
- HTTP auth protection

### Firewall Configuration

- Only ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) are open
- All other ports are blocked by default

### Docker Security

- Containers run with non-root users where possible
- Sensitive data is passed via environment variables
- Images are rebuilt from scratch on each deployment

## Troubleshooting

### Common Issues

1. **Container won't start**

   ```bash
   docker-compose -f docker-compose.prod.yml logs web
   ```

2. **Database connection issues**

   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
   ```

3. **Static files not loading**

   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic
   ```

4. **Nginx configuration issues**
   ```bash
   docker-compose -f docker-compose.prod.yml exec nginx nginx -t
   ```

### Log Locations

- Application logs: `/var/log/opc/`
- Docker logs: `docker-compose logs`
- System logs: `/var/log/syslog`
- Nginx logs: Container logs via docker-compose

## Maintenance

### Update Application

Push changes to the main/master branch, and GitHub Actions will automatically deploy.

### Update System Packages

```bash
apt update && apt upgrade -y
```

### Clean Up Docker Resources

```bash
docker system prune -f
docker volume prune -f
```

## Monitoring

### System Resources

```bash
htop
df -h
docker stats
```

### Application Metrics

- Health check endpoint: `http://46.101.145.147/health/`
- Admin interface: `http://46.101.145.147/admin/`

## Backup Strategy

### Database Backups

Set up automated database backups using cron:

```bash
# Add to crontab
0 2 * * * docker-compose -f /opt/opc/docker-compose.prod.yml exec db pg_dump -U opc_user opc_db > /opt/backups/opc_db_$(date +\%Y\%m\%d).sql
```

### Application Backups

- Code is backed up in GitHub repository
- Configuration files are in `/opt/opc/`
- Static files are regenerated on each deployment

## Support

For issues or questions about deployment, check:

1. GitHub Actions logs
2. Application logs in `/var/log/opc/`
3. Docker container logs
4. Health check logs

Remember to update the production environment variables and secrets as needed for your specific deployment requirements.
