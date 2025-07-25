from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from jose import jwt
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from auth import authenticate_user, get_db, SECRET_KEY, ALGORITHM
from models.request_log import User
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    data = {
        "sub": user.username,
        "role": user.role,
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup2", status_code=status.HTTP_201_CREATED)
def signup(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    hashed = pwd_context.hash(password)
    new_user = User(username=username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": f"User '{username}' created successfully!"}


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth", status_code=302)
    response.delete_cookie("jwt_token")
    return response
