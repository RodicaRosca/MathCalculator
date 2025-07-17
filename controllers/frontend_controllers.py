from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.services import MathService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

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
    return templates.TemplateResponse("factorial.html", {"request": request, "result": None})

@router.post("/calculate_factorial", response_class=HTMLResponse)
def calculate(request: Request, n: int = Form(...)):
    try:
        result = MathService.factorial(n)
    except Exception as e:
        result = str(e)
    return templates.TemplateResponse("factorial.html", {"request": request, "result": result})

@router.post("/calculate_pow", response_class=HTMLResponse)
def calculate(request: Request, n: int = Form(...), m: int = Form(...)):
    try:
        result = MathService.power(n, m)
    except Exception as e:
        result = str(e)
    return templates.TemplateResponse("pow.html", {"request": request, "result": result})

@router.post("/calculate_fibonacci", response_class=HTMLResponse)
def calculate(request: Request, n: int = Form(...)):
    try:
        result = MathService.fibonacci(n)
    except Exception as e:
        result = str(e)
    return templates.TemplateResponse("fibonacci.html", {"request": request, "result": result})