try:
    from .celery import app as celery_app
except (ImportError, ValueError):
    try:
        from celery import app as celery_app
    except (ImportError, ValueError):
        celery_app = None

__all__ = ('celery_app',)

