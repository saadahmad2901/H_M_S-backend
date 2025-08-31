from typing import Optional,List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from fastapi_pagination  import  Page,paginate,Params
from app import schemas
from app import services

router = APIRouter(prefix="/visit-services", tags=["visit-services"])

@router.post("/", response_model=APIResponse[schemas.VisitService])
def create_visit_service(visit_service:schemas.VisitServiceCreate,db:Session = Depends(get_db)):
    data = services.create_visit_service(visit_service,db)
    if data is None:
        raise HTTPException(status_code=400, detail="Visit service creation failed")
    return APIResponse(data=data, message="Visit service created successfully")

@router.get("/", response_model=APIResponse[Page[schemas.VisitService]])
def get_visit_services(visit_id:Optional[int]=None,paid_status:Optional[str]=None,bill_no:Optional[str]=None, db:Session = Depends(get_db), params: Params = Depends()):
    data = services.get_visit_services(visit_id,paid_status,bill_no,db)
    if data is None:
        paginated_empty = paginate([], params)
        return APIResponse(data=paginated_empty, message="Visit services not found")
    paginated_data = paginate(data, params)
    return APIResponse(data=paginated_data, message="Visit services fetched successfully")

@router.get("/{id}", response_model=APIResponse[schemas.VisitService])
def get_visit_service(id:int,db:Session = Depends(get_db)):
    data = services.get_visit_service(id,db)
    if data is None:
        raise HTTPException(status_code=400, detail="Visit service not found")
    return APIResponse(data=data, message="Visit service fetched successfully")

@router.put("/{id}", response_model=APIResponse[schemas.VisitService])
def update_visit_service(id:int,visit_service:schemas.VisitServiceUpdate,db:Session = Depends(get_db)):
    data = services.update_visit_service(id,visit_service,db)
    if data is None:
        raise HTTPException(status_code=400, detail="Visit service update failed")
    return APIResponse(data=data, message="Visit service updated successfully")

@router.delete("/{id}", response_model=APIResponse[bool])
def delete_visit_service(id:int,db:Session = Depends(get_db)):
    data = services.delete_visit_service(id,db)
    if data is None:
        raise HTTPException(status_code=400, detail="Visit service deletion failed")
    return APIResponse(data=data, message="Visit service deleted successfully")

@router.put("/is_billed/{visit_id}", response_model=APIResponse[List[schemas.UpdateUserVisitServiceBillNo]])
def update_isbilled_billno(
    visit_id: int,
    update_schema: schemas.UpdateUserVisitServiceBillNo,
    db: Session = Depends(get_db)
):
    data = services.update_isbilled_billno(visit_id, update_schema, db)
    if not data:
        raise HTTPException(status_code=400, detail="Billed update failed")
    return APIResponse(data=data, message="Billed update successful")

