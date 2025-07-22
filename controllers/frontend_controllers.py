import datetime
import json
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import SessionLocal
from models.request_log import RequestLog
from services.math_services import MathService
from kafka_logging import log_to_kafka
from auth import verify_token
import requests

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
def calculate(request: Request, 
              n: int = Form(...), 
              db: Session = Depends(get_db),
              user=Depends(verify_token)):
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
def calculate(request: Request, 
              n: int = Form(...), 
              m: int = Form(...), 
              db: Session = Depends(get_db),
              user=Depends(verify_token)):
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
        "operation": "pow",
        "parameters": {"base": n, "exponent": m},
        "result": result,
        "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
    })

    return templates.TemplateResponse("pow.html", {"request": request, "result": result})

@router.post("/calculate_fibonacci", response_class=HTMLResponse)
def calculate(request: Request, 
              n: int = Form(...), 
              db: Session = Depends(get_db), 
              user=Depends(verify_token)):
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
        "operation": "fibonacci",
        "parameters": {"n": n},
        "result": result,
        "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
    })

    return templates.TemplateResponse("fibonacci.html", {"request": request, "result": result})

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    response = requests.post("http://localhost:8000/token", data={"username": username, "password": password})
    
    if response.status_code == 200:
        token = response.json()["access_token"]

        resp = RedirectResponse(url="/", status_code=302)
        resp.set_cookie(key="jwt_token", value=token, httponly=True)
        return resp
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
