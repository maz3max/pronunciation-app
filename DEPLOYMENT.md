# Phonetics App - Production Deployment

This directory contains the production d3. **Port conflicts**: Change port mapping in docker-compose.yml
4. **Database**: Consider PostgreSQL for better performance at scalet configuration for the Norwegian phonetics web application.

## Quick Start

```bash
# Build and run the application
./deploy.sh

# Access the application
open http://localhost:8000
```

## Manual Deployment

### Prerequisites
- Docker and Docker Compose
- At least 2GB of available disk space (for models and data)

### Build and Run
```bash
# Build the Docker image
docker build -t phonetics-app:latest .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

## Configuration

### Environment Variables
- `DEBUG`: Set to `false` for production (default: false)
- `PORT`: Application port inside container (default: 8000)

### Data Management
The application downloads required model files during the build process. For production deployments, consider:

1. **Pre-built data volumes**: Mount pre-downloaded data to avoid download time
2. **Cloud storage**: Store models in cloud storage and download during startup
3. **Persistent volumes**: Use Docker volumes for data persistence

### Security Considerations

The Dockerfile includes several security best practices:
- Runs as non-root user
- Input sanitization in the Flask app
- Minimal system dependencies

### Scaling

For high-traffic deployments:
1. Increase Gunicorn workers in `gunicorn.conf.py`
2. Use an external load balancer if needed
3. Consider horizontal scaling with multiple container instances
4. Use external databases instead of SQLite for better concurrency

### Monitoring

- Health checks are configured for Docker
- Application logs are available via `docker-compose logs`
- Consider adding monitoring tools like Prometheus/Grafana

## File Structure

- `Dockerfile`: Multi-stage production build
- `docker-compose.yml`: Service orchestration
- `gunicorn.conf.py`: Production WSGI server configuration
- `deploy.sh`: Automated deployment script
- `.dockerignore`: Optimizes Docker build context

## Troubleshooting

### Common Issues

1. **Application fails to start**: Check logs with `docker-compose logs phonetics-app`
2. **Model files missing**: Ensure internet connectivity during build
3. **Permission errors**: Check file ownership and Docker daemon permissions
4. **Port conflicts**: Change port mapping in docker-compose.yml

### Performance Tuning

1. **Memory**: Increase Docker memory limit if OOM errors occur
2. **Workers**: Adjust Gunicorn workers based on CPU cores
3. **Caching**: Configure nginx caching for static assets
4. **Database**: Consider PostgreSQL for better performance at scale
