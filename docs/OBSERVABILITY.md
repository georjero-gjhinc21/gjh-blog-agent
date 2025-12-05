Observability for Celery tasks

- Instrument tasks with Prometheus counters and expose metrics via an HTTP /metrics endpoint on a sidecar or separate metrics server.
- Use OpenTelemetry to trace long-running tasks (LLM generation, embedding batching) and propagate trace IDs in logs.
- Export Celery worker metrics (task success/failure/duration) and monitor queue depth to autoscale generator workers.
- Add alerting rules for high failure rate, open circuit breakers, and slow LLM response times.
