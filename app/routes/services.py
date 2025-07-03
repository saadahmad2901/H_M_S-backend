from typing import Optional,List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from fastapi_pagination  import  Page,paginate,Params
from app.schemas.services import Service,ServiceCreate,ServiceUpdate

from app import services



router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=APIResponse[Service])
def create_service(service:ServiceCreate,db:Session = Depends(get_db)):
    data = services.create_service(service,db)
    if data is None:
        raise HTTPException(status_code=400, detail="Service creation failed")
    return APIResponse(data=data, message="Service creation successful")


@router.get("/", response_model=APIResponse[Page[Service]])
def get_services(name:Optional[str] = None,db:Session = Depends(get_db), params: Params = Depends()):
    data = services.get_services(name,db)
    if data is None:
        empty_paginate=paginate([],params)
        return APIResponse(data=empty_paginate, message="Services not found")
    paginated_data=paginate(data,params)
    return APIResponse(data=paginated_data, message="Services fetched successfully")


@router.get("/{id}", response_model=APIResponse[Service])
def get_service(id:int,db:Session = Depends(get_db)):
    data = services.get_service(id,db)
    if data is None:
        raise HTTPException(status_code=400, detail="Service not found")
    return APIResponse(data=data, message="Service fetched successfully")
    


@router.put("/{id}", response_model=APIResponse[Service])
def update_service(id:int,service:ServiceUpdate,db:Session = Depends(get_db)):
    data = services.update_service(id,service,db)
    if data is None:
        raise HTTPException(status_code=400, detail="Service update failed")
    return APIResponse(data=data, message="Service updated successfully")


@router.delete("/{id}", response_model=APIResponse[bool])
def delete_service(id:int,db:Session = Depends(get_db)):
    success = services.delete_service(id=id,db=db)
    if not success:
        raise HTTPException(status_code=404, detail="Visit not found")
    return APIResponse(data=True, message="Service deleted successfully")







