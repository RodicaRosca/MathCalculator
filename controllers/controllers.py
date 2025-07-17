from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.services import MathService
from schemas.schemas import FactorialRequest

router = APIRouter()

@router.post("/factorial")
def factorial_endpoint(req: FactorialRequest):
    try:
        result = MathService.factorial(req.n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"result": result}
