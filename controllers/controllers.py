# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from services.services import MathService
# from schemas.schemas import FactorialRequest

# router = APIRouter()

# @router.post("/factorial")
# def factorial_endpoint(req: FactorialRequest):
#     try:
#         result = MathService.factorial(req.n)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     return {"result": result}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.services import MathService
from schemas.schemas import PowRequest, FibonacciRequest, FactorialRequest
from db.database import SessionLocal
from models.request_log import RequestLog
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pow")
def pow_endpoint(req: PowRequest, db: Session = Depends(get_db)):
    result = MathService.power(req.base, req.exponent)

    log = RequestLog(
        operation="pow",
        parameters=json.dumps(req.model_dump()),
        result=str(result)
    )

    db.add(log)
    db.commit()
    return {"result": result}

@router.post("/fibonacci")
def fibonacci_endpoint(req: FibonacciRequest, db: Session = Depends(get_db)):
    try:
        result = MathService.fibonacci(req.n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    log = RequestLog(
        operation="fibonacci",
        parameters=json.dumps(req.model_dump()),
        result=str(result)
    )

    db.add(log)
    db.commit()
    return {"result": result}

@router.post("/factorial")
def factorial_endpoint(req: FactorialRequest, db: Session = Depends(get_db)):
    try:
        result = MathService.factorial(req.n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    log = RequestLog(
    operation="factorial",
    parameters=json.dumps(req.model_dump()),
    result=str(result)
)

    db.add(log)
    db.commit()
    return {"result": result}

@router.post("/testlog")
def test_log(db: Session = Depends(get_db)):
    log = RequestLog(operation="test", parameters="{}", result="test")
    db.add(log)
    db.commit()
    return {"status": "inserted"}
