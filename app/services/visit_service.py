from app.db import get_db

from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import Depends,HTTPException
from typing import List,Optional
from app import schemas
from app import models

def create_visit_service(visit_service: schemas.VisitServiceCreate, db: Session = Depends(get_db)) -> schemas.VisitService:
    # Check if the combination already exists
    existing = db.query(models.VisitService).filter_by(
        visit_id=visit_service.visit_id,
        service_id=visit_service.service_id
    ).first()

    if existing:
        # Update existing quantity
        existing.quantity += visit_service.quantity
        # Optionally update price (if needed)
        existing.price = visit_service.price
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new entry
        db_visit_service = models.VisitService(**visit_service.dict())
        db.add(db_visit_service)
        db.commit()
        db.refresh(db_visit_service)
        return db_visit_service


def get_visit_services(
    visit_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> List[schemas.VisitService]:
    results = db.query(models.VisitService, models.Services.name.label("service_name")) \
        .join(models.Services, models.VisitService.service_id == models.Services.id) \
        .filter(models.VisitService.visit_id == visit_id) \
        .order_by(desc(models.VisitService.id)) \
        .all()

    # Convert result tuples to a list of VisitService schema-compatible dicts
    return [
        {
            **visit_service.__dict__,
            "service_name": service_name
        }
        for visit_service, service_name in results
    ]


def get_visit_service(id:int,db:Session = Depends(get_db))->schemas.VisitService:
    return db.query(models.VisitService).filter(models.VisitService.id == id).first()

def update_visit_service(id:int,visit_service:schemas.VisitServiceUpdate,db:Session = Depends(get_db))->schemas.VisitService:   

    db_visit_service = db.query(models.VisitService).filter(models.VisitService.id == id).first()
    if db_visit_service is None:
        raise HTTPException(status_code=404, detail="Visit service not found")
    for key,value in visit_service.dict(exclude_unset=True).items():
        setattr(db_visit_service,key,value)
    db.commit()
    db.refresh(db_visit_service)
    return db_visit_service

def delete_visit_service(id:int,db:Session = Depends(get_db))->bool:
    db_visit_service = db.query(models.VisitService).filter(models.VisitService.id == id).first()
    if db_visit_service is None:
        raise HTTPException(status_code=404, detail="Visit service not found")
    db.delete(db_visit_service)
    db.commit()
    return True
