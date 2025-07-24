import pytest
from services.math_services import MathService


def test_factorial_basic():
    assert MathService.factorial(0) == 1
    assert MathService.factorial(1) == 1
    assert MathService.factorial(5) == 120


def test_factorial_negative():
    with pytest.raises(ValueError):
        MathService.factorial(-3)


def test_fibonacci_basic():
    assert MathService.fibonacci(0) == 0
    assert MathService.fibonacci(1) == 1
    assert MathService.fibonacci(5) == 5
    assert MathService.fibonacci(10) == 55


def test_fibonacci_negative():
    with pytest.raises(ValueError):
        MathService.fibonacci(-2)


def test_power_basic():
    assert MathService.power(2, 3) == 8
    assert MathService.power(10, 0) == 1
    assert MathService
