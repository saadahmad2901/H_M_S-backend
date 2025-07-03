from sqlalchemy.orm import Session
from app.models import Doctor
from fastapi import HTTPException
from typing import List, Optional
from app import schemas

def create_doctor(db: Session, doctor: schemas.DoctorCreate) -> Doctor:
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def get_doctors(
    db: Session,
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    specialization: Optional[str] = None,
) -> List[Doctor]:
    query = db.query(Doctor)
    if department_id is not None:
        query = query.filter(Doctor.department_id == department_id)
    if status is not None:
        query = query.filter(Doctor.status == status)
    if specialization is not None:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    return query.all()


def get_doctor(db: Session, doctor_id: int) -> Optional[Doctor]:
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def update_doctor(db: Session, doctor_id: int, doctor: schemas.DoctorUpdate) -> Optional[Doctor]:
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        return None
    for key, value in doctor.dict(exclude_unset=True).items():
        setattr(db_doctor, key, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: int) -> bool:
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        return False
    db.delete(db_doctor)
    db.commit()
    return True
