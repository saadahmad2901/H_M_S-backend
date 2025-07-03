from typing import  Optional
from datetime import datetime,date,time
from pydantic import BaseModel


class VisitBase(BaseModel):
    appointment_id: Optional[int]=None
    patient_id: Optional[int]
    check_out_time: Optional[datetime]=None
    check_in_time: Optional[datetime]=None

    doctor_id: Optional[int]
    visit_status: Optional[str]
    reason_for_visit: Optional[str]
    vitals: Optional[str]
    diagnosis: Optional[str]
    notes: Optional[str]
    follow_up_date: Optional[date]

class Visit(VisitBase):
    id: int
    class Config:
        orm_mode = True

class VisitCreate(BaseModel):
    appointment_id: Optional[int] = None
    patient_id: Optional[int]
    check_out_time: Optional[datetime] = None
    check_in_time: Optional[datetime] = None

    doctor_id: Optional[int]
    visit_status: Optional[str]
    reason_for_visit: Optional[str]
    vitals: Optional[str]
    diagnosis: Optional[str]
    notes: Optional[str]



class VisitUpdate(BaseModel):
    visit_status: Optional[str]
    vitals: Optional[str]
    diagnosis: Optional[str]
    notes: Optional[str]
    follow_up_date: Optional[date]

class UpdateVisitStatus(BaseModel):
    visit_status: Optional[str]
    follow_up_date: Optional[date] = None




class VisitWithDetails(BaseModel):
    visit:Visit
    patient_name: str

    doctor_name: str

