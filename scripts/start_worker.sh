#!/usr/bin/env bash
# Start a Celery worker for the given queue (default: research)
QUEUE=${1:-research}
celery -A tasks.celery_app.celery_app worker -Q ${QUEUE} --loglevel=info
