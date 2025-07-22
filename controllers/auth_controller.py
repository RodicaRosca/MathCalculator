from fastapi import APIRouter, Form, Depends, HTTPException
from jose import jwt
import datetime
from sqlalchemy.orm import Session
from auth import authenticate_user, get_db, SECRET_KEY, ALGORITHM

router = APIRouter()

@router.post("/token")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    data = {
        "sub": user.username,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
