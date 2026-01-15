# Velux Admin Panel - Docker Deployment Guide

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

## Quick Start

### 1. Clone and Setup Environment

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd velux-admin-panel

# Copy environment template
cp .env.example .env

# Edit .env with your production values
nano .env
```

### 2. Configure Environment Variables

Edit `.env` and set the following **required** values:

```env
# Generate a secure secret key (use: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
SECRET_KEY=your-generated-secret-key-here

# Set to False in production
DEBUG=False

# Add your domain(s)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database credentials
DB_NAME=velux_db
DB_USER=postgres
DB_PASSWORD=your-strong-password-here
DB_HOST=db
DB_PORT=5432
```

### 3. Build and Run

```bash
# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Create Superuser

```bash
# Create Django admin superuser
docker-compose exec web python manage.py createsuperuser
```

### 5. Access Application

- **Main Application**: http://localhost
- **Admin Panel**: http://localhost/admin/
- **Health Check**: http://localhost/health/

## Docker Commands Reference

### Service Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Logs and Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# Execute commands in container
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
docker-compose exec db psql -U postgres -d velux_db
```

### Database Operations

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Database backup
docker-compose exec db pg_dump -U postgres velux_db > backup.sql

# Database restore
cat backup.sql | docker-compose exec -T db psql -U postgres velux_db
```

### Static Files

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## Production Deployment

### Security Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Set strong database password
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Enable HTTPS (configure SSL certificates)
- [ ] Set up firewall rules
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging

### SSL/HTTPS Setup

To enable HTTPS, modify `nginx/nginx.conf`:

1. Add SSL certificate paths
2. Redirect HTTP to HTTPS
3. Update `docker-compose.yml` to mount certificates

Example SSL configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... rest of configuration
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Environment-Specific Configurations

For different environments (staging, production), create separate compose files:

```bash
# docker-compose.prod.yml
# docker-compose.staging.yml

# Run with specific config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Backup and Restore

### Database Backup

```bash
# Create backup
docker-compose exec db pg_dump -U postgres velux_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Restore from backup
gunzip -c backup_20260115_120000.sql.gz | docker-compose exec -T db psql -U postgres velux_db
```

### Media Files Backup

```bash
# Backup media files
docker run --rm -v velux-admin-panel_media_volume:/data -v $(pwd):/backup alpine tar czf /backup/media_backup.tar.gz -C /data .

# Restore media files
docker run --rm -v velux-admin-panel_media_volume:/data -v $(pwd):/backup alpine tar xzf /backup/media_backup.tar.gz -C /data
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs web

# Check if port is already in use
lsof -i :80
lsof -i :8000

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database connection issues

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec web python manage.py check --database default
```

### Static files not loading

```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Check nginx logs
docker-compose logs nginx

# Verify volume mounts
docker-compose exec nginx ls -la /app/staticfiles
```

### Permission issues

```bash
# Fix ownership in container
docker-compose exec web chown -R appuser:appuser /app/media
docker-compose exec web chown -R appuser:appuser /app/staticfiles
```

## Monitoring

### Health Checks

All services have health checks configured:

```bash
# Check health status
docker-compose ps

# Manual health check
curl http://localhost/health/
```

### Resource Usage

```bash
# View resource usage
docker stats

# View specific container
docker stats velux_web
```

## Scaling

To scale the web service:

```bash
# Scale to 3 instances
docker-compose up -d --scale web=3

# Note: You'll need to configure Nginx for load balancing
```

## Updates and Maintenance

### Update Application Code

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose build web
docker-compose up -d web

# Run migrations if needed
docker-compose exec web python manage.py migrate
```

### Update Dependencies

```bash
# Update requirements.txt
# Then rebuild
docker-compose build --no-cache web
docker-compose up -d web
```

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Review Django documentation: https://docs.djangoproject.com/
- Review Docker documentation: https://docs.docker.com/
