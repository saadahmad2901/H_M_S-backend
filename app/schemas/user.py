from typing import  Optional
from datetime import datetime,date,time
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    status: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    fullname: str
    email: str
    username: str
    password: str
    is_active: bool=True
    status: str='Admin'
    class Config:
        orm_mode = True
class UserUpdate(BaseModel):
    email: str
    username: str
    password: str
    is_active: bool=True
    status: str='Admin'

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdatePassword(BaseModel):
    email: str
    password: str

class UserUpdateStatus(BaseModel):
    status: str

class UserOut(BaseModel):
    id: int
    fullname: str
    email: str
    username: str
    status: str
    is_active: bool

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
        access_token: str
        token_type: str
        user: UserOut

        class Config:
            orm_mode = True
