# Docker Setup Guide for OptiChoice

This guide explains how to set up and run the OptiChoice project using Docker.

## Prerequisites

- Docker
- Docker Compose

## Local Development Setup

1. **Clone the repository (if you haven't already)**

2. **Navigate to the project directory**
   ```bash
   cd /path/to/OPC
   ```

3. **Make sure you have the .env file**
   The `.env` file should be in the project root directory (same level as `manage.py`).
   If you don't have one, copy from the example:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual values.

4. **Build and start the Docker containers**
   ```bash
   docker-compose up -d --build
   ```
   This command will:
   - Build the Docker image
   - Start the container
   - Run database migrations
   - Start the development server

5. **Access the application**
   Open your browser and go to:
   ```
   http://localhost:8000
   ```

6. **View logs**
   ```bash
   docker-compose logs -f
   ```

7. **Stop the application**
   ```bash
   docker-compose down
   ```

## Running Commands in the Container

You can run Django management commands inside the container:

```bash
# Run a management command
docker-compose exec web python manage.py <command>

# Open a shell in the container
docker-compose exec web bash

# Create a superuser
docker-compose exec web python manage.py createsuperuser
```

## Production Deployment (Digital Ocean)

For deploying to Digital Ocean:

1. **Create a Digital Ocean Droplet**
   - Choose a Docker image when creating the droplet
   - Select appropriate size based on your needs

2. **SSH into your Droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Clone your repository**
   ```bash
   git clone <your-repository-url>
   cd OPC
   ```

4. **Create production .env file**
   ```bash
   cp .env.example .env
   nano .env
   ```
   Update with production settings:
   - Set `DEBUG=False`
   - Set a strong `SECRET_KEY`
   - Update `ALLOWED_HOSTS` with your domain/IP
   - Configure other settings as needed

5. **Build and start the app**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

6. **Set up Nginx for reverse proxy (optional but recommended)**
   ```bash
   apt-get update
   apt-get install nginx
   ```

7. **Configure Nginx as a reverse proxy**
   Create a new configuration file:
   ```bash
   nano /etc/nginx/sites-available/optichoice
   ```

   Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # Replace with your domain or IP

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

8. **Enable the site and restart Nginx**
   ```bash
   ln -s /etc/nginx/sites-available/optichoice /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx
   ```

9. **Set up SSL with Let's Encrypt (recommended)**
   ```bash
   apt-get install certbot python3-certbot-nginx
   certbot --nginx -d your-domain.com
   ```

## Troubleshooting

- **Container won't start**: Check logs with `docker-compose logs`
- **Database errors**: Make sure the database file is available and has proper permissions
- **Web server not responding**: Check if the container is running with `docker ps`
- **Permissions issues**: Files created in the container may have different ownership, fix with `chown`

## Data Persistence

The SQLite database file is stored in a volume, so your data will persist between container restarts.
