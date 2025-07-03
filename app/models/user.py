from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
        UniqueConstraint('username', name='uq_user_username'),
    )

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    status = Column(String, default='Admin')
