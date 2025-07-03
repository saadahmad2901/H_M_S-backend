from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services

router = APIRouter(prefix="/user", tags=["user"])

@router.post('/register', response_model=APIResponse[schemas.User])
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    res = services.create_user(user,db)
    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    return APIResponse(data=res ,message="User created successfully")

@router.post("/login", response_model=APIResponse[schemas.TokenResponse])
def login_user(user:schemas.UserLogin,db: Session = Depends(get_db)):
    res = services.login(user,db)
    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    return APIResponse(data=res ,message="User login successfully")
