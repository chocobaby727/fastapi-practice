from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(512), unique=True)
    username = Column(String(512), unique=True)
    first_name = Column(String(512))
    last_name = Column(String(512))
    hashed_password = Column(String(512))
    is_active = Column(Boolean, default=True)
    role = Column(String(512))
