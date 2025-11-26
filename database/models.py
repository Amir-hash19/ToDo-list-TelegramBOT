from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
from .base import Base



class UserModel(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")



class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    is_done = Column(Boolean, default=False)
    priority = Column(Integer, default=3)  
    created_at = Column(DateTime, server_default=func.now())
    due_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="tasks")