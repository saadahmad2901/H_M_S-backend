from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Doctor
from app.schemas import DoctorCreate, DoctorUpdate, Doctor
from app import services
from app.db import get_db
from fastapi_pagination import Page, paginate, Params
from app.core import APIResponse
from typing import Optional

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=APIResponse[Doctor], status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    data = services.create_doctor(db=db, doctor=doctor)
    if data is None:
        raise HTTPException(status_code=400, detail="Doctor creation failed")
    return APIResponse(data=data, message="Doctor created successfully")


@router.get("/", response_model=APIResponse[Page[Doctor]])
def list_doctors(
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    specialization: Optional[str] = None,
    db: Session = Depends(get_db),
    params: Params = Depends(),
):
    doctors = services.get_doctors(db=db, department_id=department_id, status=status, specialization=specialization)
    if not doctors:
        return APIResponse(data=paginate([], params), message="Doctors Not Found ")
    return APIResponse(data=paginate(doctors, params), message="Doctors retrieved successfully")


@router.get("/{doctor_id}", response_model=APIResponse[Doctor])
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = services.get_doctor(db=db, doctor_id=doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return APIResponse(data=db_doctor, message="Doctor retrieved successfully")


@router.put("/{doctor_id}", response_model=APIResponse[Doctor])
def update_doctor(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db)):
    db_doctor = services.update_doctor(db=db, doctor_id=doctor_id, doctor=doctor)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return APIResponse(data=db_doctor, message="Doctor has been updated successfully")


@router.delete("/{doctor_id}", response_model=APIResponse[bool])
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    success = services.delete_doctor(db=db, doctor_id=doctor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return APIResponse(data=True, message="Doctor has been deleted")
