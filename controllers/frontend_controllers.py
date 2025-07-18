import datetime
import json
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import SessionLocal
from models.request_log import RequestLog
from services.math_services import MathService
from kafka_logging import log_to_kafka

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@router.get("/factorial", response_class=HTMLResponse)
def factorial_page(request: Request):
    return templates.TemplateResponse("factorial.html", {"request": request, "result": None})

@router.get("/pow", response_class=HTMLResponse)
def factorial_page(request: Request):
    return templates.TemplateResponse("pow.html", {"request": request, "result": None})

@router.get("/fib", response_class=HTMLResponse)
def factorial_page(request: Request):
    return templates.TemplateResponse("fibonacci.html", {"request": request, "result": None})

@router.post("/calculate_factorial", response_class=HTMLResponse)
def calculate(request: Request, n: int = Form(...), db: Session = Depends(get_db)):
    try:
        result = MathService.factorial(n)
    except Exception as e:
        result = str(e)

    log = RequestLog(
        operation="factorial",
        parameters=json.dumps({"n": n}),
        result=str(result)
    )
    db.add(log)
    db.commit()

    log_to_kafka({
        "operation": "factorial",
        "parameters": {"n": n},
        "result": result,
        "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
    })

    return templates.TemplateResponse("factorial.html", {"request": request, "result": result})

@router.post("/calculate_pow", response_class=HTMLResponse)
def calculate(request: Request, n: int = Form(...), m: int = Form(...), db: Session = Depends(get_db)):
    try:
        result = MathService.power(n, m)
    except Exception as e:
        result = str(e)

    log = RequestLog(
        operation="pow",
        parameters=json.dumps({"base": n, "exponent": m}),
        result=str(result)
    )
    db.add(log)
    db.commit()

    log_to_kafka({
        "operation": "factorial",
        "parameters": {"n": n},
        "result": result,
        "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
    })

    return templates.TemplateResponse("pow.html", {"request": request, "result": result})

@router.post("/calculate_fibonacci", response_class=HTMLResponse)
def calculate(request: Request, n: int = Form(...), db: Session = Depends(get_db)):
    try:
        result = MathService.fibonacci(n)
    except Exception as e:
        result = str(e)
    
    log = RequestLog(
        operation="fibonacci",
        parameters=json.dumps({"n": n}),
        result=str(result)
    )
    db.add(log)
    db.commit()

    log_to_kafka({
        "operation": "factorial",
        "parameters": {"n": n},
        "result": result,
        "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
    })

    return templates.TemplateResponse("fibonacci.html", {"request": request, "result": result})