from sqlalchemy.orm import Session
from app.models.department import Department
from typing import List, Optional
from app.schemas.department import DepartmentCreate, DepartmentUpdate

def create_department(db: Session, department: DepartmentCreate) -> Department:
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def get_department(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()


def get_departments(db: Session, name: Optional[str] = None) -> List[Department]:
    query = db.query(Department)
    if name:
        query = query.filter(Department.name.ilike(f"%{name}%"))
    return query.all()


def update_department(db: Session, department_id: int, department: DepartmentUpdate) -> Optional[Department]:
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        return None
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_department, key, value)
    db.commit()
    db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: int) -> bool:
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        return False
    db.delete(db_department)
    db.commit()
    return True 