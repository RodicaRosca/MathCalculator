from sqlalchemy.orm import Session
from models.request_log import User
from db.database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(username: str, password: str, role="user"):
    db: Session = SessionLocal()
    hashed = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    print(f"Created user: {username}")
