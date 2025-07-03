from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.visit import VisitCreate, Visit,VisitUpdate,VisitWithDetails,UpdateVisitStatus
from app.core import APIResponse
from app import services
from fastapi_pagination  import  Page,paginate,Params

router = APIRouter(prefix="/visits", tags=["visits"])

@router.post("/", response_model=APIResponse[Visit])
def create_visit(visit: VisitCreate, db: Session = Depends(get_db)):
    data = services.create_visit(db=db, visit=visit)
    if data is None:
        raise HTTPException(status_code=400, detail="Visit creation failed")
    return APIResponse(data=data, message="Visit creation successful")

@router.get("/", response_model=APIResponse[Page[VisitWithDetails]])
def list_visits(
doctor_id:Optional[int] = None,
patient_id:Optional[int] = None,
appointment_id:Optional[int] = None,
        db: Session = Depends(get_db), params: Params = Depends()):
    data = services.get_visits(
        db=db,
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_id=appointment_id
    )
    if data is None:
        paginated_empty = paginate([], params)
        return APIResponse(data=paginated_empty, message="No visits found")

    paginated_data = paginate(data, params)
    return APIResponse(data=paginated_data, message="Visits retrieved successfully")


@router.get("/{id}",response_model=APIResponse[VisitWithDetails])
def get_visit(id:int,db:Session = Depends(get_db)):
    data=services.get_visit(db=db,id=id)
    if data is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return APIResponse(data=data, message="Visit retrieved successfully")

@router.put("/{id}",response_model=APIResponse[Visit])
def update_visit(id:int,visit:VisitUpdate,db:Session = Depends(get_db)):
    data = services.update_visit(id,visit,db)
    if data is None:
        raise HTTPException(status_code=404, detail="Visit update failed")
    return APIResponse(data=data, message="Visit updated successfully")

@router.put("/visit-status/{id}",response_model=APIResponse[Visit])
def update_visit_status(id:int,visit:UpdateVisitStatus,db:Session = Depends(get_db)):
    data = services.update_visit_status(id,visit,db)
    if data is None:
        raise HTTPException(status_code=404, detail="Visit update failed")
    return APIResponse(data=data, message="Visit updated successfully")
@router.delete("/{id}", response_model=APIResponse[bool])
def delete_visit(id: int, db: Session = Depends(get_db)) -> APIResponse[bool]:
    success = services.delete_visit(id=id, db=db)
    if not success:
        raise HTTPException(status_code=404, detail="Visit not found")
    return APIResponse(data=True, message="Visit deleted successfully")

