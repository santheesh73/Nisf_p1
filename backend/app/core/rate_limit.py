import logging
import time
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import Request
from redis import Redis
from redis.exceptions import RedisError

from app.core.config import get_settings
from app.core.exceptions import NISFError

logger = logging.getLogger(__name__)


class RateLimitExceededError(NISFError):
    status_code = 429
    code = "rate_limit_exceeded"


class RequestTooLargeError(NISFError):
    status_code = 413
    code = "request_too_large"


class RateLimiter:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._memory: dict[str, deque[float]] = defaultdict(deque)
        self._redis: Redis | None = None
        self._redis_checked = False

    def enforce_request_size(self, request: Request) -> None:
        header = request.headers.get("content-length")
        if not header:
            return
        try:
            size = int(header)
        except ValueError:
            return
        if size > self.settings.max_request_bytes:
            raise RequestTooLargeError(
                f"Request body exceeds the {self.settings.max_request_bytes} byte limit."
            )

    def enforce(self, request: Request, action: str) -> None:
        limits = self._limits()
        limit, window = limits.get(action, (0, 0))
        if limit <= 0:
            return

        identity = self._identity(request)
        key = f"rate_limit:{action}:{identity}"
        allowed = self._allow_with_redis(key, limit, window)
        if allowed is None:
            allowed = self._allow_in_memory(key, limit, window)

        if not allowed:
            logger.warning(
                "rate_limit_exceeded",
                extra={"stage": "http", "job_id": None, "action": action, "identity": identity},
            )
            raise RateLimitExceededError(f"Rate limit exceeded for {action}. Please try again later.")

    def _limits(self) -> dict[str, tuple[int, int]]:
        if self.settings.app_env == "local":
            return {
                "generate": (200, 3600),
                "optimize": (100, 3600),
                "score": (600, 3600),
                "feedback": (1000, 3600),
            }
        return {
            "generate": (20, 3600),
            "optimize": (10, 3600),
            "score": (60, 3600),
            "feedback": (100, 3600),
        }

    def _identity(self, request: Request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        client = request.client.host if request.client else "unknown"
        return client or "unknown"

    def _redis_client(self) -> Redis | None:
        if self._redis_checked:
            return self._redis
        self._redis_checked = True
        try:
            self._redis = Redis.from_url(self.settings.redis_url, socket_timeout=1, socket_connect_timeout=1)
            self._redis.ping()
        except RedisError as exc:
            logger.info("redis_rate_limit_unavailable", extra={"error": str(exc)})
            self._redis = None
        return self._redis

    def _allow_with_redis(self, key: str, limit: int, window: int) -> bool | None:
        client = self._redis_client()
        if client is None:
            return None
        now = int(time.time())
        bucket = now // window
        redis_key = f"{key}:{bucket}"
        try:
            current = client.incr(redis_key)
            if current == 1:
                client.expire(redis_key, window)
            return current <= limit
        except RedisError as exc:
            logger.warning("redis_rate_limit_failed", extra={"error": str(exc)})
            return None

    def _allow_in_memory(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        bucket = self._memory[key]
        cutoff = now - window
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True


_rate_limiter: RateLimiter | None = None


def get_rate_limiter() -> RateLimiter:
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


def protect_endpoint(action: str) -> Callable[[Request], None]:
    def _guard(request: Request) -> None:
        limiter = get_rate_limiter()
        limiter.enforce_request_size(request)
        limiter.enforce(request, action)

    return _guard
