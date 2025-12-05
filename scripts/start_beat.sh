#!/usr/bin/env bash
# Start Celery beat scheduler
celery -A tasks.celery_app.celery_app beat --loglevel=info
