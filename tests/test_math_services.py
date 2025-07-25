

import pytest
from unittest.mock import patch
from services.math_services import MathService


@pytest.fixture(autouse=True)
def mock_redis():
    with patch("services.math_services.r") as mock_r:
        cache = {}
        mock_r.get.side_effect = lambda k: cache.get(k)
        mock_r.set.side_effect = lambda k, v: cache.__setitem__(k, v)
        yield


def test_factorial_large():
    assert MathService.factorial(10) == 3628800
    assert MathService.factorial(7) == 5040


def test_factorial_negative():
    with pytest.raises(ValueError):
        MathService.factorial(-3)


def test_factorial_invalid_type():
    with pytest.raises(TypeError):
        MathService.factorial(3.5)
    with pytest.raises(TypeError):
        MathService.factorial("abc")


def test_fibonacci_large():
    assert MathService.fibonacci(15) == 610
    assert MathService.fibonacci(20) == 6765


def test_fibonacci_negative():
    with pytest.raises(ValueError):
        MathService.fibonacci(-2)


def test_fibonacci_invalid_type():
    with pytest.raises(TypeError):
        MathService.fibonacci(2.5)
    with pytest.raises(TypeError):
        MathService.fibonacci("abc")


def test_power_basic():
    assert MathService.power(2, 3) == 8
    assert MathService.power(10, 0) == 1
    assert MathService.power(5, 1) == 5
    assert MathService.power(0, 5) == 0
    assert MathService.power(-2, 3) == -8
    assert MathService.power(-2, 2) == 4
    assert MathService.power(2, -2) == 0.25
    assert MathService.power(0, 0) == 1  # By convention


def test_power_invalid():
    with pytest.raises(TypeError):
        MathService.power("a", 2)
    with pytest.raises(TypeError):
        MathService.power(2, "b")
    with pytest.raises(TypeError):
        MathService.power(None, 2)
