import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


class MathService:
    @staticmethod
    def factorial(n: int) -> int:
        cache_key = f"factorial:{n}"
        cached = r.get(cache_key)
        if cached:
            return int(cached)
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        result = 1
        for i in range(2, n + 1):
            result *= i
        r.set(cache_key, result)
        return result

    @staticmethod
    def fibonacci(n: int) -> int:
        cache_key = f"fib:{n}"
        cached = r.get(cache_key)
        if cached:
            return int(cached)
        if n < 0:
            raise ValueError("Input must be a non-negative integer.")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        r.set(cache_key, a)
        return a

    @staticmethod
    def power(base: float, exponent: float) -> float:
        cache_key = f"power:{base}:{exponent}"
        cached = r.get(cache_key)
        if cached:
            return float(cached)
        result = base ** exponent
        r.set(cache_key, result)
        return result
