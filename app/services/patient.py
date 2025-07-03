from sqlalchemy.orm import Session
from app.models import Patient
from fastapi import HTTPException
from typing import List, Optional
from app.utils import get_dropdown_options
from app.schemas import DropDownSchema
from app import schemas


def get_patient(db: Session, patient_id: int) -> schemas.Patient:
    """
    Retrieve a patient by ID.
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def get_patients(
    db: Session,
    patient_id: Optional[str] = None,
    name: Optional[str] = None,
    gender: Optional[str] = None,
    blood_group: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    cnic: Optional[str] = None,
) -> List[schemas.Patient]:
    """
    Retrieve all patients.
    """
    query = db.query(Patient)
    if patient_id:
        query = query.filter(Patient.id == patient_id)
    if name:
        query = query.filter(Patient.name.ilike(f"%{name}%"))
    if gender:
        query = query.filter(Patient.gender == gender)
    if blood_group:
        query = query.filter(Patient.blood_group == blood_group)
    if phone:
        query = query.filter(Patient.phone.ilike(f"%{phone}%"))
    if email:
        query = query.filter(Patient.email.ilike(f"%{email}%"))
    if cnic:
        query = query.filter(Patient.cnic.ilike(f"%{cnic}%"))
    return query.all()


def create_patient(db: Session, patient: schemas.PatientCreate) -> schemas.Patient:
    """
    Create a new patient.
    """
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(
    db: Session, patient_id: int, patient: schemas.PatientUpdate
) -> schemas.Patient:
    """
    Update an existing patient.
    """
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int) -> schemas.Patient:
    """
    Delete a patient by ID.
    """
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return db_patient


def get_patient_by_cnic(db: Session, cnic: str) -> schemas.Patient:
    """
    Retrieve a patient by phone number.
    """
    patient = db.query(Patient).filter(Patient.phone == cnic).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

