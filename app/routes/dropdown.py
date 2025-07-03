from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Appointment
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.services import Services
from app.models.patient import Patient
from typing import List, Optional
from app.schemas import DropDownSchema
from app import utils
import app.data as data 

router = APIRouter(prefix="/dropdowns", tags=["dropdowns"])

@router.get("/departments", response_model=List[DropDownSchema])
def departments_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, Department, "id", "name")


@router.get("/services", response_model=List[DropDownSchema])
def services_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, Services, "id", "name")

@router.get("/appointments", response_model=List[DropDownSchema])
def departments_dropdown(patient_id:Optional[int] = Query(None),
        db: Session = Depends(get_db)):
    condition={}
    if patient_id is  not None:
        condition["patient_id"] = patient_id

    return utils.get_dropdown_options(db, Appointment, "id", "reason_for_visit",condition)

@router.get("/patients", response_model=List[DropDownSchema])
def patient_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, Patient, "id", "name")


@router.get("/doctors", response_model=List[DropDownSchema])
def doctors_dropdown(department_id: Optional[int] = None, db: Session = Depends(get_db)):
    condition = {}
    if department_id is not None:
        condition["department_id"] = department_id
    return utils.get_dropdown_options(db, Doctor, "id", "full_name", condition)

@router.get("/appointment-status")
def appointment_dropdown(search: str = Query(None)):
    
    return utils.get_json_dropdown_options(data.appointment_status, "value", "label", search=search)

@router.get("/appointment-type")
def appointment_type(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.appointment_type, "value", "label", search=search)

@router.get("/booking-source")
def booking_source(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.booking_source, "value", "label", search=search)

@router.get("/payment-method")
def payment_method(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.payment_method, "value", "label", search=search)

@router.get("/payment-status")
def payment_status(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.payment_status, "value", "label", search=search)

@router.get("/blood-groups")
def blood_groups(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.blood_groups, "value", "label", search=search)

@router.get("/doctor-status")
def doctor_status(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.doctor_status, "value", "label", search=search)

@router.get("/gender")
def gender(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.gender, "value", "label", search=search)

@router.get("/marital-status")
def marital_status(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.marital_status, "value", "label", search=search)

@router.get("/preferred-languages")
def preferred_languages(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.preferred_languages, "value", "label", search=search)

@router.get("/visit-status")
def visit_status(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.visit_status, "value", "label", search=search)

