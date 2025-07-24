from pydantic import BaseModel


class FactorialRequest(BaseModel):
    n: int


class FibonacciRequest(BaseModel):
    n: int


class PowRequest(BaseModel):
    base: float
    exponent: float
