from sqlalchemy.orm import Session
from app.models import Patient,Appointment
from fastapi import HTTPException
from typing import List, Optional
from app.utils import get_dropdown_options
from app.schemas import DropDownSchema
from app import schemas,models
from datetime import datetime

now = datetime.now()


BASE_URL = "http://localhost:8000"

def get_patient(db: Session, patient_id: int) -> schemas.Patient:

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if patient.photo:
        patient.photo =f"{BASE_URL}/uploads/{patient.photo}"
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

def create_patients_and_appointment(db: Session, schema: schemas.PatientAndAppointmentWithBot):
    # Check if patient exists
    
    exist_patient = db.query(models.Patient).filter(models.Patient.cnic == schema.cnic).first()

    if exist_patient:
        # Create follow-up appointment
        existing_appo = db.query(models.Appointment).filter(models.Appointment.patient_id == exist_patient.id).first()

        new_appointment = models.Appointment(
            patient_id=exist_patient.id,
            reason_for_visit=schema.reason_for_visit,
            booking_source="IG-Bot",
            date=now.date(),
            time=now.time(),
            status="Pending",
            appointment_type="Follow-up",
            department_id=existing_appo.department_id if existing_appo else 1,
            doctor_id=existing_appo.doctor_id if existing_appo else 1,
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        return {
            "name": exist_patient.name,
            "gender": exist_patient.gender,
            "dob": exist_patient.dob,
            "cnic": exist_patient.cnic,
            "contact_number": exist_patient.contact_number,
            "remarks": exist_patient.remarks,
            "reason_for_visit": new_appointment.reason_for_visit,
            "booking_source": new_appointment.booking_source,
            "date": new_appointment.date,
            "time": new_appointment.time,
            "status": new_appointment.status
        }

    # If not exists, create new patient and appointment
    new_patient = models.Patient(
        name=schema.name,
        gender=schema.gender,
        cnic=schema.cnic,
        contact_number=schema.contact_number,
        emergency_contact_number=schema.contact_number,
        email='no@gmail.com',
        remarks=schema.remarks,
        dob=schema.dob
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    new_appointment = models.Appointment(
        patient_id=new_patient.id,
        reason_for_visit=schema.reason_for_visit,
        booking_source="IG-Bot",
        date=now.date(),
        time=now.time(),
        status="Pending",
        appointment_type="New",
        department_id=1,
        doctor_id=1,
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "name": new_patient.name,
        "gender": new_patient.gender,
        "dob": new_patient.dob,
        "cnic": new_patient.cnic,
        "contact_number": new_patient.contact_number,
        "remarks": new_patient.remarks,
        "reason_for_visit": new_appointment.reason_for_visit,
        "booking_source": new_appointment.booking_source,
        "date": new_appointment.date,
        "time": new_appointment.time,
        "status": new_appointment.status
    }
