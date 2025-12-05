"""Lightweight task utilities: idempotency decorator and simple circuit breaker.

These are intentionally minimal to avoid heavy dependencies in tests. They prefer Redis (REDIS_URL) when available, and fall back to in-process behavior for local runs.
"""
import os
import functools
import time

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


def _get_redis():
    try:
        import redis
        return redis.from_url(REDIS_URL)
    except Exception:
        return None


def idempotent_task(ttl: int = 24 * 3600):
    """Decorator to make tasks idempotent using Redis keys.

    Usage:
        @idempotent_task()
        def my_task(..., task_id=None):
            ...
    If task_id is not provided, a deterministic key based on function name
    and arguments will be used.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task_id = kwargs.get('task_id')
            if not task_id:
                # create a lightweight deterministic id
                try:
                    key_body = f"{func.__name__}:{args}:{sorted(kwargs.items())}"
                except Exception:
                    key_body = f"{func.__name__}:{int(time.time())}"
                task_id = key_body

            key = f"gjh:idempotent:{task_id}"

            r = _get_redis()
            if r:
                # set if not exists
                try:
                    if not r.set(key, 'in-progress', nx=True, ex=ttl):
                        # key exists: task already running or completed
                        return None
                    result = func(*args, **kwargs)
                    # mark completed
                    r.set(key, 'done', ex=ttl)
                    return result
                finally:
                    # best-effort: do not delete the key immediately to avoid races
                    pass
            else:
                # no redis available: run function (non-idempotent fallback)
                return func(*args, **kwargs)

        return wrapper
    return decorator


class SimpleCircuitBreaker:
    """A tiny circuit breaker using Redis for shared state.

    Tracks consecutive failures and opens the circuit after `max_failures`.
    When open, calls will raise CircuitOpenError until reset_timeout has passed.
    """
    class CircuitOpenError(Exception):
        pass

    def __init__(self, name: str, max_failures: int = 5, reset_timeout: int = 60):
        self.name = name
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self._redis = _get_redis()
        self._fail_key = f"gjh:cb:fail:{self.name}"
        self._open_key = f"gjh:cb:open:{self.name}"

    def _is_open(self):
        if self._redis:
            return self._redis.get(self._open_key) is not None
        return False

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self._is_open():
                raise SimpleCircuitBreaker.CircuitOpenError(f"Circuit {self.name} is open")

            try:
                result = func(*args, **kwargs)
                # on success, reset failure counter
                if self._redis:
                    self._redis.delete(self._fail_key)
                return result
            except Exception as e:
                if self._redis:
                    failures = self._redis.incr(self._fail_key)
                    if failures == 1:
                        # set an expiry to limit counting period
                        self._redis.expire(self._fail_key, self.reset_timeout)
                    if failures >= self.max_failures:
                        # open the circuit
                        self._redis.set(self._open_key, '1', ex=self.reset_timeout)
                raise

        return wrapper
