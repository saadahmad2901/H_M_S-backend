from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import schemas, services
from app.core import APIResponse
from fastapi_pagination  import  Page,paginate,Params



router = APIRouter(prefix="/bills-information", tags=["bills"])

@router.get("/", response_model=APIResponse[Page[schemas.BillOut]])
def get_bill_info(visit_id: Optional[int] = None, db: Session = Depends(get_db)  ,params: Params = Depends()):
    data = services.get_bill_info(visit_id=visit_id, db=db)
    if not data:
        paginated_empty = paginate([], params)
        return APIResponse(data=paginated_empty, message="No bills found")

    paginated_data = paginate(data, params)
    return APIResponse(data=paginated_data, message="Bills fetched successfully")

@router.post("/", response_model=APIResponse[schemas.BillOut])
def create_bill(bill_data: schemas.BillCreate, db: Session = Depends(get_db)):
    new_bill = services.create_bill(bill_data, db)
    return APIResponse(data=new_bill, message="Bill created successfully")

@router.delete("/{bill_id}", response_model=APIResponse[str])
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    services.delete_bill(bill_id, db)
    return APIResponse(data="Bill deleted successfully", message="Bill deleted")

