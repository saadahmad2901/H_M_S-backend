from typing import List, Optional

from sqlalchemy.orm import Session
from app import schemas
from app.models import Appointment, Patient, Doctor
from app.models.visit import Visit

def create_visit(db: Session, visit: schemas.VisitCreate) -> schemas.Visit:
    db_visit = Visit(**visit.dict())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

def get_visits(
    db: Session,
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    appointment_id: Optional[int] = None
) -> List[Visit]:
    query = (
        db.query(Visit, Patient.name.label("patient_name"), Doctor.full_name.label("doctor_name"))
        .join(Patient, Visit.patient_id == Patient.id)
        .join(Doctor, Visit.doctor_id == Doctor.id)
    )

    if patient_id is not None:
        query = query.filter(Visit.patient_id == patient_id)
    if appointment_id is not None:
        query = query.filter(Visit.appointment_id == appointment_id)
    if doctor_id is not None:
        query = query.filter(Visit.doctor_id == doctor_id)

    query = query.order_by(Visit.id.desc()).all()
  # Run after all filters

    results = []
    for visit, patient_name, doctor_name in query:
        results.append({
            "visit": visit,
            "patient_name": patient_name,
            "doctor_name": doctor_name,
        })

    return results

def get_visit(db: Session, id: int) -> Optional[dict]:
    res = (
        db.query(Visit, Patient.name, Doctor.full_name)
        .join(Patient, Visit.patient_id == Patient.id)
        .join(Doctor, Visit.doctor_id == Doctor.id)
        .filter(Visit.id == id)
        .first()
    )

    if res is None:
        return None

    visit_obj, patient_name, doctor_name = res

    return {
        "visit": visit_obj,
        "patient_name": patient_name,
        "doctor_name": doctor_name
    }

def delete_visit(id: int, db: Session) -> bool:
    db_visit = db.query(Visit).filter(Visit.id == id).first()
    if  db_visit is None:
        return False
    db.delete(db_visit)
    db.commit()
    return True


def update_visit(id: int, visit: schemas.VisitUpdate, db: Session) -> Optional[Visit]:
    db_visit = db.query(Visit).filter(Visit.id == id).first()
    if not db_visit:
        return None

    for key, value in visit.dict(exclude_unset=True).items():
        setattr(db_visit, key, value)

    db.commit()
    db.refresh(db_visit)
    return db_visit

def update_visit_status(id: int, visit: schemas.UpdateVisitStatus, db: Session) -> Optional[Visit]:
    db_visit = db.query(Visit).filter(Visit.id == id).first()
    if not db_visit:
        return None
    for key, value in visit.dict(exclude_unset=True).items():
        setattr(db_visit, key, value)

    db.commit()
    db.refresh(db_visit)
    return db_visit