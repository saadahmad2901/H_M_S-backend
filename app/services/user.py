from datetime import timedelta
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app import  user_utils
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(user: schemas.UserCreate, db: Session) -> schemas.User:
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = user_utils.hash_password(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password

    response = models.Users(**user_dict)
    db.add(response)
    db.commit()
    db.refresh(response)
    return response

def get_all_users(db: Session) -> List[schemas.User]:
    users=db.query(models.Users).all()
    return users




def login(user: schemas.UserLogin, db: Session):
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Email not found")

    if not user_utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Create JWT token
    access_token = user_utils.create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=60)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "fullname": db_user.fullname,
            "email": db_user.email,
            "username": db_user.username,
            "status": db_user.status,
            "is_active": db_user.is_active
        }
    }

def forget_password(user:schemas.UserUpdatePassword, db: Session) -> schemas.User:
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    db_user.password= hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user
    

def send_update_password_mail(email: str, db: Session) -> bool:
    db_user = db.query(models.Users).filter(models.Users.email == email).first()
    if not db_user:
        return False
    return True

def logout():
    # Placeholder – implement token blacklist if using JWT or session clearing
    pass

