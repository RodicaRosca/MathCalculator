class MathService:
    @staticmethod
    def factorial(n: int) -> int:
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        result = 1
        
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def fibonacci(n: int) -> int:
        if n < 0:
            raise ValueError("Input must be a non-negative integer.")
        a, b = 0, 1

        for _ in range(n):
            a, b = b, a + b
        return a
    
    @staticmethod
    def power(base: float, exponent: float) -> float:
        return base ** exponent