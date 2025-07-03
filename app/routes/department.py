from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import services
from app.schemas.department import Department, DepartmentCreate, DepartmentUpdate
from app.core import APIResponse
from fastapi_pagination import Page, paginate, Params
from typing import Optional

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=APIResponse[Department])
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    data = services.create_department(db=db, department=department)
    if data is None:
        raise HTTPException(status_code=400, detail="Department creation failed")
    return APIResponse(data=data, message="Department created successfully")

@router.get("/{department_id}", response_model=APIResponse[Department])
def get_department(department_id: int, db: Session = Depends(get_db)):
    data = services.get_department(db=db, department_id=department_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return APIResponse(data=data, message="Department retrieved successfully")

@router.get("/", response_model=APIResponse[Page[Department]])
def list_departments(
    name: Optional[str] = None,
    db: Session = Depends(get_db),
    params: Params = Depends(),
):
    data = services.get_departments(db=db, name=name)
    if not data:
        raise HTTPException(status_code=404, detail="No departments found")
    return APIResponse(data=paginate(data, params), message="Departments retrieved successfully")

@router.put("/{department_id}", response_model=APIResponse[Department])
def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    data = services.update_department(db=db, department_id=department_id, department=department)
    if data is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return APIResponse(data=data, message="Department updated successfully")

@router.delete("/{department_id}", response_model=APIResponse[bool])
def delete_department(department_id: int, db: Session = Depends(get_db)):
    success = services.delete_department(db=db, department_id=department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return APIResponse(data=True, message="Department deleted successfully") 