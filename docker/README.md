# Docker Setup for FitScheduler

This directory contains Docker configuration files for the FitScheduler application.

## Quick Start

1. Make sure you have Docker and Docker Compose installed on your system.

2. In the root directory of the project (one level up from this directory), run:

```bash
docker-compose up -d
```

This will start the application and MySQL database in detached mode.

3. Access the API at http://localhost:8000

## Available Configurations

### Development Environment

Use the default docker-compose.yml file for development:

```bash
docker-compose up -d
```

This configuration:
- Mounts the local code as a volume for quick development
- Sets the environment to development
- Uses a longer token expiration time
- Sets CORS for local development

### Production Environment

For production, use the production configuration:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Before running this command, make sure to set the following environment variables:
- `SECRET_KEY`: A secure random string for JWT token generation
- `DB_PASSWORD`: Password for the database user
- `MYSQL_ROOT_PASSWORD`: Root password for MySQL
- `CORS_ORIGINS`: JSON string of allowed origins, e.g., '["https://example.com"]'

Example:
```bash
export SECRET_KEY=your_secure_secret_key
export DB_PASSWORD=secure_db_password
export MYSQL_ROOT_PASSWORD=secure_root_password
export CORS_ORIGINS='["https://example.com"]'
docker-compose -f docker-compose.prod.yml up -d
```

## Database Migrations

Database migrations run automatically on startup using Alembic.

## Customization

You can customize the Docker setup by:
1. Modifying the Dockerfile for application changes
2. Updating docker-compose.yml or docker-compose.prod.yml for service configuration changes

## Troubleshooting

If you encounter issues:

1. Check container logs:
```bash
docker-compose logs app  # For application logs
docker-compose logs db   # For database logs
```

2. Ensure the database is reachable:
```bash
docker-compose exec app python -m app.utils.wait_for_db
```

3. Restart the services:
```bash
docker-compose restart
``` 