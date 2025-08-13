import datetime
import json
import requests
from fastapi import (
    APIRouter, Request, Form, Cookie
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.database import SessionLocal
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
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": None}
    )


@router.get("/factorial", response_class=HTMLResponse)
def factorial_page(request: Request):
    return templates.TemplateResponse(
        "factorial.html", {"request": request, "result": None}
    )


@router.get("/pow", response_class=HTMLResponse)
def pow_page(request: Request):
    return templates.TemplateResponse(
        "pow.html", {"request": request, "result": None}
    )


@router.get("/fib", response_class=HTMLResponse)
def fib_page(request: Request):
    return templates.TemplateResponse(
        "fibonacci.html", {"request": request, "result": None}
    )

@router.post("/calculate_factorial", response_class=HTMLResponse)
def calculate_factorial(
    request: Request,
    n: int = Form(...),
    jwt_token: str = Cookie(None)
):
    if not jwt_token:
        return RedirectResponse("/auth", status_code=302)
    response = requests.post(
        "http://localhost:8000/factorial",
        json={"n": n},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    if response.status_code == 200:
        try:
            result = response.json()["result"]
        except Exception:
            result = "Error parsing result"
    else:
        try:
            result = response.json().get("detail", "Error")
        except Exception:
            result = response.text or "Unknown error"
    return templates.TemplateResponse(
        "factorial.html", {"request": request, "result": result}
    )


@router.post("/calculate_pow", response_class=HTMLResponse)
def calculate_pow(
    request: Request,
    n: int = Form(...),
    m: int = Form(...),
    jwt_token: str = Cookie(None)
):
    if not jwt_token:
        return RedirectResponse("/auth", status_code=302)
    response = requests.post(
        "http://localhost:8000/pow",
        json={"base": n, "exponent": m},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    if response.status_code == 200:
        try:
            result = response.json()["result"]
        except Exception:
            result = "Error parsing result"
    else:
        try:
            result = response.json().get("detail", "Error")
        except Exception:
            result = response.text or "Unknown error"
    return templates.TemplateResponse(
        "pow.html", {"request": request, "result": result}
    )


@router.post("/calculate_fibonacci", response_class=HTMLResponse)
def calculate_fibonacci(
    request: Request,
    n: int = Form(...),
    jwt_token: str = Cookie(None)
):

    if not jwt_token:
        return RedirectResponse("/auth", status_code=302)
    response = requests.post(
        "http://localhost:8000/fibonacci",
        json={"n": n},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    if response.status_code == 200:
        try:
            result = response.json()["result"]
        except Exception:
            result = "Error parsing result"
    else:
        try:
            result = response.json().get("detail", "Error")
        except Exception:
            result = response.text or "Unknown error"
    return templates.TemplateResponse(
        "fibonacci.html", {"request": request, "result": result}
    )


def calculate_factorial(
    request: Request,
    n: int = Form(...),
    jwt_token: str = Cookie(None)
):
    if not jwt_token:
        return RedirectResponse("/auth", status_code=302)
    response = requests.post(
        "http://localhost:8000/factorial",
        json={"n": n},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    if response.status_code == 200:
        try:
            result = response.json()["result"]
        except Exception:
            result = "Error parsing result"
    else:
        try:
            result = response.json().get("detail", "Error")
        except Exception:
            result = response.text or "Unknown error"
    return templates.TemplateResponse(
        "factorial.html", {"request": request, "result": result}
    )


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    response = requests.post(
        "http://localhost:8000/token",
        data={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        resp = RedirectResponse(url="/", status_code=302)
        resp.set_cookie(key="jwt_token", value=token, httponly=True)
        return resp
    return templates.TemplateResponse(
        request, "login.html", {"error": "Invalid credentials"}
    )


@router.get("/auth", response_class=HTMLResponse)
def auth_form(request: Request):
    return templates.TemplateResponse(
        "auth.html", {"request": request, "error": None}
    )


@router.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse(
        request, "signup.html", {"error": None}
    )


@router.post("/signup", response_class=HTMLResponse)
def signup_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    response = requests.post(
        "http://localhost:8000/signup2",
        data={"username": username, "password": password}
    )
    if response.status_code == 201:
        return RedirectResponse(url="/login", status_code=302)
    error = "Signup failed"
    try:
        error = response.json().get("detail", error)
    except Exception:
        pass
    return templates.TemplateResponse(
        request, "signup.html", {"error": error}
    )
