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

@router.get('/', response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    data = services.get_all_users(db)
    return data

@router.post("/login", response_model=APIResponse[schemas.TokenResponse])
def login_user(user:schemas.UserLogin,db: Session = Depends(get_db)):
    res = services.login(user,db)
    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    return APIResponse(data=res ,message="User login successfully")

@router.put("/forget-password", response_model=APIResponse[schemas.User])
def forget_password(user:schemas.UserUpdatePassword,db: Session = Depends(get_db)):
    res = services.forget_password(user,db)
    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    return APIResponse(data=res ,message="Forget password successfully")


@router.post("/send-mail-for-update-password", response_model=APIResponse[bool])
def send_update_password_mail(email: str, db: Session = Depends(get_db)):
    res = services.send_update_password_mail(email, db)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(data=True, message="Password update email sent successfully")
