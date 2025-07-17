from pydantic import BaseModel

class FactorialRequest(BaseModel):
    n: int

class FibonacciRequest(BaseModel):
    n: int 

class PowerRequest(BaseModel):
    base: float
    exponent: float