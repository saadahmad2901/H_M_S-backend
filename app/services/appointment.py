from sqlalchemy.orm import Session

from app.models import Patient, Department, Doctor
from app.models.appointment import Appointment, StatusEnum
from typing import List, Optional
from fastapi import HTTPException

# If you add schemas/appointment.py later, update the type hints accordingly

def create_appointment(db: Session, appointment_data: dict) -> Appointment:
    appointment = Appointment(**appointment_data)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointment(db: Session, appointment_id: int) -> Optional[dict]:
    res = (
        db.query(Appointment, Patient.name, Department.name, Doctor.full_name)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Department, Appointment.department_id == Department.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not res:
        return None

    appointment, patient_name, department_name, doctor_name = res

    print("Appointment ID:", appointment.id)
    print("Patient Name:", patient_name)
    print("Department Name:", department_name)
    print("Doctor Name:", doctor_name)

    return {
        "appointment": appointment,
        "patient_name": patient_name,
        "department_name": department_name,
        "doctor_name": doctor_name
    }

def get_appointments(
    db: Session,
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    status: Optional[StatusEnum] = None,
) -> List[dict]:
    query = db.query(Appointment, Patient.name, Department.name, Doctor.full_name)\
        .join(Patient, Appointment.patient_id == Patient.id)\
        .join(Department, Appointment.department_id == Department.id)\
        .join(Doctor, Appointment.doctor_id == Doctor.id)

    if patient_id is not None:
        query = query.filter(Appointment.patient_id == patient_id)
    if doctor_id is not None:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if status is not None:
        query = query.filter(Appointment.status == status)

    results = []
    for appointment, patient_name, department_name, doctor_name in query.all():
        results.append({
            "appointment": appointment,  # You can serialize this if needed
            "patient_name": patient_name,
            "department_name": department_name,
            "doctor_name": doctor_name
        })

    return results


def update_appointment(db: Session, appointment_id: int, update_data: dict) -> Optional[Appointment]:
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        return None
    for key, value in update_data.items():
        setattr(appointment, key, value)
    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment_id: int) -> bool:
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        return False
    db.delete(appointment)
    db.commit()
    return True
