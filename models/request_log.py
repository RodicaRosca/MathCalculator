from sqlalchemy import Column, Integer, String, DateTime, Text
from db.database import Base
import datetime

class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    parameters = Column(Text)
    result = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") 
