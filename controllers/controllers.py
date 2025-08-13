import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.math_services import MathService
from schemas.schemas import PowRequest, FibonacciRequest, FactorialRequest
from db.database import SessionLocal
from models.request_log import RequestLog
from datetime import datetime, timezone
from kafka_logging import log_to_kafka
from auth import verify_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/pow")
def pow_endpoint(
    req: PowRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    try:
        result = MathService.power(req.base, req.exponent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    log = RequestLog(
        operation="pow",
        parameters=json.dumps(req.model_dump()),
        result=str(result)
    )
    db.add(log)
    db.commit()
    log_to_kafka({
        "operation": "pow",
        "parameters": req.model_dump(),
        "result": result,
        "timestamp": str(datetime.now(timezone.utc))
    })
    return {"result": result}


@router.post("/fibonacci")
def fibonacci_endpoint(
    req: FibonacciRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
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
    log_to_kafka({
        "operation": "fibonacci",
        "parameters": req.model_dump(),
        "result": result,
        "timestamp": str(datetime.now(timezone.utc))
    })
    return {"result": result}


@router.post("/factorial")
def factorial_endpoint(
    req: FactorialRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
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
    log_to_kafka({
        "operation": "factorial",
        "parameters": req.model_dump(),
        "result": result,
        "timestamp": str(datetime.now(timezone.utc))
    })
    return {"result": result}


@router.post("/testlog")
def test_log(db: Session = Depends(get_db)):
    log = RequestLog(operation="test", parameters="{}", result="test")
    db.add(log)
    db.commit()
    return {"status": "inserted"}
