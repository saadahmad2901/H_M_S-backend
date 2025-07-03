from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import services
from app.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate,AppointmentWithDetails
from app.core import APIResponse
from fastapi_pagination import Page, paginate, Params
from typing import Optional

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=APIResponse[Appointment])
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    data = services.create_appointment(db=db, appointment_data=appointment.dict())
    if data is None:
        raise HTTPException(status_code=400, detail="Appointment creation failed")
    return APIResponse(data=data, message="Appointment created successfully")

@router.get("/{appointment_id}", response_model=APIResponse[AppointmentWithDetails])
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    data = services.get_appointment(db=db, appointment_id=appointment_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return APIResponse(data=data, message="Appointment retrieved successfully")

@router.get("/", response_model=APIResponse[Page[AppointmentWithDetails]])
def list_appointments(
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    params: Params = Depends(),
):
    data = services.get_appointments(db=db, patient_id=patient_id, doctor_id=doctor_id, status=status)


    if not data:
        return APIResponse(data=paginate([],params), message="No appointments found")
        # raise HTTPException(status_code=404, detail="No appointments found")
    return APIResponse(data=paginate(data, params), message="Appointments retrieved successfully")

@router.put("/{appointment_id}", response_model=APIResponse[Appointment])
def update_appointment(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    data = services.update_appointment(db=db, appointment_id=appointment_id, update_data=appointment.dict(exclude_unset=True))
    if data is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return APIResponse(data=data, message="Appointment updated successfully")

@router.delete("/{appointment_id}", response_model=APIResponse[bool])
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    success = services.delete_appointment(db=db, appointment_id=appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return APIResponse(data=True, message="Appointment deleted successfully") 