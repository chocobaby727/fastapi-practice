from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime

class Todos(Base):
    __tablename__ = "Todos"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    description = Column(String(512))
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
