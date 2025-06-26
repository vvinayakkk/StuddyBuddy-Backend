# StuddyBuddy Backend

## Environment Variables
See `.env.example` for all required environment variables.

## Docker Usage

Build and run with Docker Compose:

```
docker-compose up --build
```

This will start Django, Postgres, and Redis. Static and media files are mounted as volumes.

## Production Checklist
- Set all secrets and DB credentials in your `.env` file
- Set `DJANGO_DEBUG=False`
- Set `DJANGO_ALLOWED_HOSTS` to your domain(s)
- Use S3 for static/media in production
- Set up HTTPS and secure CORS
- Configure email for password reset/verification
- Add monitoring and logging 