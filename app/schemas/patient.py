import datetime
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    name: str
    dob: date
    gender: str
    cnic: constr(min_length=13, max_length=15)  # e.g. 1234512345671
    contact_number: str
    emergency_contact_number: str
    email: Optional[EmailStr]
    address: Optional[str]
    occupation: Optional[str]
    marital_status: Optional[str]
    blood_group: Optional[str]
    known_allergies: Optional[str]
    existing_conditions: Optional[str]
    current_condition: Optional[str]
    preferred_language: Optional[str]
    referred_by: Optional[str]
    photo: Optional[str]  # can be a URL or file path
    remarks: Optional[str]
    created_at: Optional[datetime.datetime] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True

class PatientDropdown(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe"
            }
        }
