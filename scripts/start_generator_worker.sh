#!/usr/bin/env bash
# Start the generator worker (optimized for heavy workloads / GPU nodes)
celery -A tasks.celery_app.celery_app worker -Q generator --concurrency=1 --loglevel=info
