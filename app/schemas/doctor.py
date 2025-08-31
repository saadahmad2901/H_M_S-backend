from typing import Optional
from datetime import date, time, datetime
from pydantic import BaseModel, EmailStr
from app.models.doctor import GenderEnum, DoctorStatus

# Import your enums from the relevant module

class DoctorBase(BaseModel):
    full_name: str
    photo: Optional[str] = None
    email: EmailStr
    phone_number: str
    cnic: str
    gender: GenderEnum
    date_of_birth: Optional[date] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    department_id: Optional[int] = None
    available_days: Optional[str] = None
    available_time_from: Optional[time] = None
    available_time_to: Optional[time] = None
    consultation_fee: Optional[float] = None
    status: Optional[DoctorStatus] = None

class DoctorCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    cnic: str
    gender: GenderEnum
    date_of_birth: Optional[date] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    department_id: Optional[int] = None
    available_days: Optional[str] = None
    available_time_from: Optional[time] = None
    available_time_to: Optional[time] = None
    consultation_fee: Optional[float] = None
    status: Optional[DoctorStatus] = None

class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    department_id: Optional[int] = None
    available_days: Optional[str] = None
    available_time_from: Optional[time] = None
    available_time_to: Optional[time] = None
    consultation_fee: Optional[float] = None
    status: Optional[DoctorStatus] = None

class DoctorInDBBase(DoctorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Doctor(DoctorInDBBase):
    pass