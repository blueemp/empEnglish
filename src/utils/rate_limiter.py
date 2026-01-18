# 限流器伪代码
# 文件路径: utils/rate_limiter.py

from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimiter:
    """限流器"""

    def __init__(self, redis_client=None):
        """
        初始化限流器

        Args:
            redis_client: Redis客户端（如果使用Redis）
        """
        self.redis_client = redis_client
        self.local_store = defaultdict(list)  # 本地存储

    def is_allowed(self, key: str, limit: int, window: int = 60) -> Dict[str, bool]:
        """
        检查是否允许请求

        Args:
            key: 限流键
            limit: 限制次数
            window: 时间窗口（秒）

        Returns:
            检查结果
        """
        if self.redis_client:
            return self._is_allowed_redis(key, limit, window)
        else:
            return self._is_allowed_local(key, limit, window)

    def _is_allowed_local(self, key: str, limit: int, window: int) -> Dict[str, bool]:
        """
        本地限流检查

        Args:
            key: 限流键
            limit: 限制次数
            window: 时间窗口（秒）

        Returns:
            检查结果
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window)

        # 获取历史记录
        history = self.local_store[key]

        # 清理过期记录
        history = [t for t in history if t > window_start]

        # 检查是否超过限制
        if len(history) >= limit:
            return {
                "allowed": False,
                "remaining": 0,
                "reset_time": (history[0] + timedelta(seconds=window)).isoformat(),
            }

        # 添加当前请求
        history.append(now)
        self.local_store[key] = history

        return {"allowed": True, "remaining": limit - len(history), "reset_time": None}

    def _is_allowed_redis(self, key: str, limit: int, window: int) -> Dict[str, bool]:
        """
        Redis限流检查

        Args:
            key: 限流键
            limit: 限制次数
            window: 时间窗口（秒）

        Returns:
            检查结果
        """
        # 伪代码：实际实现使用Redis
        # import time
        #
        # current_time = int(time.time())
        # redis_key = f"ratelimit:{key}"
        #
        # # 使用Redis的滑动窗口算法
        # pipe = self.redis_client.pipeline()
        # pipe.zremrangebyscore(redis_key, 0, current_time - window)
        # pipe.zcard(redis_key)
        # pipe.zadd(redis_key, {str(current_time): current_time})
        # pipe.expire(redis_key, window)
        # results = pipe.execute()
        #
        # count = results[1]
        #
        # if count >= limit:
        #     # 获取最早的请求时间
        #     earliest = self.redis_client.zrange(redis_key, 0, 0, withscores=True)
        #     reset_time = earliest[0][1] + window if earliest else current_time + window
        #
        #     return {
        #         "allowed": False,
        #         "remaining": 0,
        #         "reset_time": reset_time
        #     }
        #
        # return {
        #     "allowed": True,
        #     "remaining": limit - count - 1,
        #     "reset_time": None
        # }

        # 模拟返回
        return {"allowed": True, "remaining": limit - 1, "reset_time": None}

    def reset(self, key: str):
        """
        重置限流

        Args:
            key: 限流键
        """
        if self.redis_client:
            self.redis_client.delete(f"ratelimit:{key}")
        else:
            del self.local_store[key]

    def reset_key(self, key: str):
        """
        重置限流（别名方法）

        Args:
            key: 限流键
        """
        self.reset(key)

    def get_usage(self, key: str, window: int = 60) -> Dict[str, int]:
        """
        获取限流使用统计

        Args:
            key: 限流键
            window: 时间窗口（秒）

        Returns:
            使用统计
        """
        if self.redis_client:
            return {"count": 0, "limit": 0, "remaining": 0}
        else:
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=window)
            history = [t for t in self.local_store.get(key, []) if t > window_start]
            return {
                "count": len(history),
                "limit": 0,
                "remaining": max(0, 0 - len(history)),
            }


class TokenBucketRateLimiter:
    """令牌桶限流器"""

    def __init__(self, capacity: int, refill_rate: float, redis_client=None):
        """
        初始化令牌桶限流器

        Args:
            capacity: 桶容量
            refill_rate: 填充速率（令牌/秒）
            redis_client: Redis客户端
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.redis_client = redis_client
        self.local_buckets = {}  # 本地存储

    def is_allowed(self, key: str) -> Dict[str, Any]:
        """
        检查是否允许请求

        Args:
            key: 限流键

        Returns:
            检查结果
        """
        if self.redis_client:
            return self._is_allowed_redis(key)
        else:
            return self._is_allowed_local(key)

    def _is_allowed_local(self, key: str) -> Dict[str, Any]:
        """
        本地令牌桶检查

        Args:
            key: 限流键

        Returns:
            检查结果
        """
        now = datetime.utcnow()

        # 获取或创建桶
        if key not in self.local_buckets:
            self.local_buckets[key] = {"tokens": self.capacity, "last_refill": now}

        bucket = self.local_buckets[key]

        # 填充令牌
        time_passed = (now - bucket["last_refill"]).total_seconds()
        tokens_to_add = time_passed * self.refill_rate
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = now

        # 检查是否有令牌
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return {
                "allowed": True,
                "remaining": int(bucket["tokens"]),
                "reset_time": None,
            }
        else:
            # 计算恢复时间
            time_to_refill = (1 - bucket["tokens"]) / self.refill_rate
            reset_time = now + timedelta(seconds=time_to_refill)

            return {
                "allowed": False,
                "remaining": 0,
                "reset_time": reset_time.isoformat(),
            }

    def _is_allowed_redis(self, key: str) -> Dict[str, Any]:
        """
        Redis令牌桶检查

        Args:
            key: 限流键

        Returns:
            检查结果
        """
        # 伪代码：实际实现使用Redis
        # import time
        #
        # redis_key = f"tokenbucket:{key}"
        # current_time = time.time()
        #
        # # 使用Lua脚本保证原子性
        # lua_script = """
        # local key = KEYS[1]
        # local capacity = tonumber(ARGV[1])
        # local refill_rate = tonumber(ARGV[2])
        # local current_time = tonumber(ARGV[3])
        #
        # local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        # local tokens = tonumber(bucket[1]) or capacity
        # local last_refill = tonumber(bucket[2]) or current_time
        #
        # -- 填充令牌
        # local time_passed = current_time - last_refill
        # local tokens_to_add = time_passed * refill_rate
        # tokens = math.min(capacity, tokens + tokens_to_add)
        #
        # -- 检查令牌
        # if tokens >= 1 then
        #     tokens = tokens - 1
        #     redis.call('HMSET', key, 'tokens', tokens, 'last_refill', current_time)
        #     redis.call('EXPIRE', key, math.ceil(capacity / refill_rate) + 1)
        #     return {1, math.floor(tokens)}
        # else
        #     redis.call('HMSET', key, 'tokens', tokens, 'last_refill', current_time)
        #     redis.call('EXPIRE', key, math.ceil(capacity / refill_rate) + 1)
        #     return {0, 0}
        # end
        # """
        #
        # result = self.redis_client.eval(
        #     lua_script,
        #     1,
        #     redis_key,
        #     self.capacity,
        #     self.refill_rate,
        #     current_time
        # )
        #
        # if result[0] == 1:
        #     return {
        #         "allowed": True,
        #         "remaining": result[1],
        #         "reset_time": None
        #     }
        # else:
        #     time_to_refill = 1 / self.refill_rate
        #     reset_time = current_time + time_to_refill
        #
        #     return {
        #         "allowed": False,
        #         "remaining": 0,
        #         "reset_time": reset_time
        #     }

        # 模拟返回
        return {"allowed": True, "remaining": self.capacity - 1, "reset_time": None}


class RateLimiterConfig:
    """限流配置"""

    # 限流规则
    RATE_LIMITS = {
        "default": {"limit": 100, "window": 60},
        "auth": {"limit": 10, "window": 60},
        "practice": {"limit": 20, "window": 60},
        "upload": {"limit": 5, "window": 60},
        "api": {"limit": 1000, "window": 60},
    }

    # 令牌桶配置
    TOKEN_BUCKETS = {
        "default": {"capacity": 100, "refill_rate": 1.67},  # 100/60
        "premium": {"capacity": 200, "refill_rate": 3.33},  # 200/60
        "vip": {"capacity": 500, "refill_rate": 8.33},  # 500/60
    }

    @classmethod
    def get_rate_limit(cls, endpoint: str) -> Dict[str, Any]:
        """
        获取限流规则

        Args:
            endpoint: 端点名称

        Returns:
            限流规则
        """
        return cls.RATE_LIMITS.get(endpoint, cls.RATE_LIMITS["default"])

    @classmethod
    def get_limit(cls, endpoint: str) -> int:
        """
        获取端点限制

        Args:
            endpoint: 端点名称

        Returns:
            限制次数
        """
        rule = cls.get_rate_limit(endpoint)
        return rule.get("limit", 100)

    @classmethod
    def get_token_bucket(cls, user_type: str) -> Dict[str, float]:
        """
        获取令牌桶配置

        Args:
            user_type: 用户类型

        Returns:
            令牌桶配置
        """
        return cls.TOKEN_BUCKETS.get(user_type, cls.TOKEN_BUCKETS["default"])

    @classmethod
    def is_rate_limited(cls, endpoint: str) -> bool:
        """
        检查端点是否需要限流

        Args:
            endpoint: 端点名称

        Returns:
            是否需要限流
        """
        return endpoint in cls.RATE_LIMITS
