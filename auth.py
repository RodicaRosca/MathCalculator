# import os
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt


# SECRET_KEY = os.getenv("SECRET_KEY")

# if not SECRET_KEY:
#     raise RuntimeError("SECRET_KEY environment variable must be set! See the project README.")

# ALGORITHM = "HS256"
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload 
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials"
#         )

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.request_log import User
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable must be set! See the project README.")

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
