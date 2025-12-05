"""Optional Prometheus metrics helpers (no hard dependency).

If prometheus_client is available, expose counters/gauges; otherwise provide no-op stubs.
"""
try:
    from prometheus_client import Counter, Gauge
    has_prom = True
except Exception:
    has_prom = False

if has_prom:
    post_counter = Counter('gjh_posts_generated_total', 'Total posts generated')
    publish_counter = Counter('gjh_posts_published_total', 'Total posts published')
    last_update_gauge = Gauge('gjh_last_metrics_update_timestamp', 'Last metrics update timestamp')
else:
    class _Noop:
        def inc(self, *a, **k):
            return None
        def set(self, *a, **k):
            return None
    post_counter = _Noop()
    publish_counter = _Noop()
    last_update_gauge = _Noop()


def record_post_generated():
    post_counter.inc()


def record_post_published():
    publish_counter.inc()


def set_last_metrics_update(ts):
    try:
        last_update_gauge.set(ts)
    except Exception:
        pass
