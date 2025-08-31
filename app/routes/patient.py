from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from sqlalchemy.orm import Session
from app.core import APIResponse
from app import schemas
from app import services
from fastapi_pagination import Page, paginate, Params
from typing import Optional


router = APIRouter()


@router.post("/patients/", response_model=APIResponse[schemas.Patient])
async def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient.
    """
    data = services.create_patient(db=db, patient=patient)
    if data is None:
        raise HTTPException(status_code=400, detail="Patient creation failed")
    return APIResponse(data=data, message="Patient created successfully")


@router.get("/patients/{patient_id}", response_model=APIResponse[schemas.Patient])
async def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a patient by ID.
    """
    db_patient = services.get_patient(db=db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return APIResponse(data=db_patient, message="Patient retrieved successfully")


@router.put("/patients/{patient_id}", response_model=APIResponse[schemas.Patient])
async def update_patient(
    patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing patient.
    """
    db_patient = services.update_patient(db=db, patient_id=patient_id, patient=patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return APIResponse(data=db_patient, message="Patient has been updated successfully")


@router.delete(
    "/patients/{patient_id}", response_model=APIResponse[schemas.Patient]
)
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient by ID.
    """
    db_patient = services.delete_patient(db=db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return APIResponse(data=db_patient, message="Patient has been deleted")


@router.get("/patients/", response_model=APIResponse[Page[schemas.Patient]])
async def read_patients(
    patient_id: Optional[str] = None,
    name: Optional[str] = None,
    gender: Optional[str] = None,
    blood_group: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    cnic: Optional[str] = None,
    db: Session = Depends(get_db),
    params: Params = Depends(),
):
    """
    Retrieve all patients with pagination.
    """
    data = services.get_patients(
        db=db,
        patient_id=patient_id,
        name=name,
        gender=gender,
        blood_group=blood_group,
        phone=phone,
        email=email,
        cnic=cnic,
    )
    if not data:
        return APIResponse(data=paginate([],params), message="Patients Not Found")
    return APIResponse(data=paginate(data,params), message="Patients retrieved successfully")

@router.post("/patients-appointment/add-by-bot", response_model=APIResponse[schemas.PatientAndAppointmentWithBot])
async def create_patients_and_appointment_endpoint(
    schema: schemas.PatientAndAppointmentWithBot,
    db: Session = Depends(get_db)
):
    data = services.create_patients_and_appointment(db=db, schema=schema)
    if not data:
        raise HTTPException(status_code=400, detail="patients_and_appointment creation failed")
    return APIResponse(data=data, message="patients_and_appointment created successfully")
