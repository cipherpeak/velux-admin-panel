# Quick Docker Commands Reference

## First Time Setup

```bash
# 1. Configure environment
cp .env.example .env
nano .env  # Edit with your production values

# 2. Build and start
docker-compose build
docker-compose up -d

# 3. Create superuser
docker-compose exec web python manage.py createsuperuser

# 4. Access at http://localhost
```

## Daily Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart after code changes
docker-compose restart web
```

## Maintenance

```bash
# Database backup
docker-compose exec db pg_dump -U postgres velux_db > backup_$(date +%Y%m%d).sql

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## Troubleshooting

```bash
# Check service status
docker-compose ps

# View specific service logs
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

See [DEPLOYMENT.md](file:///Users/amal/velux-admin-panel/DEPLOYMENT.md) for complete documentation.
