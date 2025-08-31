from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException



def get_bill_info(db: Session, visit_id: Optional[int] = None) -> List[models.BillInfo]:
    query = db.query(models.BillInfo)
    if visit_id:
        query = query.filter(models.BillInfo.visit_id == visit_id)
    return query.all()

def create_bill(bill_data: schemas.BillCreate, db: Session) -> models.BillInfo:
    new_bill = models.BillInfo(**bill_data.dict())
    db.add(new_bill)
    db.commit()

    # ✅ Update VisitService where purchased_billed_id matches
    db.query(models.VisitService).filter(
        models.VisitService.purchased_billed_id == bill_data.purchased_billed_id
    ).update(
        {models.VisitService.is_paid: True},
        synchronize_session=False
    )

    db.commit()  # Commit the update

    db.refresh(new_bill)
    return new_bill


def delete_bill(bill_id: int, db: Session):
    bill = db.query(models.BillInfo).filter(models.BillInfo.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    db.delete(bill)
    db.commit()