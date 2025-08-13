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
        if n > 1500:
            raise ValueError(f"Factorial is limited to n <= 1500.")
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
        if n > 100:
            raise ValueError("Fibonacci is limited to n <= 100.")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        r.set(cache_key, a)
        return a

    @staticmethod
    def power(base: float, exponent: float) -> float:
        cache_key = f"power:{base}:{exponent}"
        cached = r.get(cache_key)
        if base > 100 or exponent > 100:
            raise ValueError("Base and exponent must be less than or equal to 100.")
        if cached:
            return float(cached)
        result = base ** exponent
        r.set(cache_key, result)
        return result
