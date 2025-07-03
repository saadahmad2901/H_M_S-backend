from sqlalchemy import desc

from app.db import get_db
from app import schemas

from app.models.services import Services as ServiceModel
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException
from typing import List,Optional



def create_service(service:schemas.ServiceCreate,db:Session = Depends(get_db))->schemas.Service:
    db_service = ServiceModel(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_services(name: Optional[str] = None, db: Session = Depends(get_db)) -> List[schemas.Service]:
    query = db.query(ServiceModel)

    if name:
        query = query.filter(ServiceModel.name.ilike(f"%{name}%"))

    query = query.order_by(desc(ServiceModel.id))  # ✅ Show latest ID first

    return query.all()

def get_service(id:int,db:Session = Depends(get_db))->schemas.Service:
    service = db.query(ServiceModel).filter(ServiceModel.id == id).first()
    return service

def update_service(id:int,service:schemas.ServiceUpdate,db:Session = Depends(get_db))->schemas.Service:
    db_service = db.query(ServiceModel).filter(ServiceModel.id == id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    for key,value in service.dict(exclude_unset=True).items():
        setattr(db_service,key,value)
    db.commit()
    db.refresh(db_service)
    return db_service

def delete_service(id:int,db:Session = Depends(get_db)) -> bool :
    db_service = db.query(ServiceModel).filter(ServiceModel.id == id).first()
    if db_service is None:
        return False
    db.delete(db_service)
    db.commit()
    return True



