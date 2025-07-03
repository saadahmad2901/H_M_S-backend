from typing import  Optional
from datetime import datetime,date,time
from pydantic import BaseModel


class VisitServiceBase(BaseModel):
    visit_id:int
    service_id:int
    quantity:int
    price:float


class VisitServiceCreate(VisitServiceBase):
    pass

class VisitServiceUpdate(BaseModel):
     quantity:int

class VisitService(VisitServiceBase):
    id:int
    service_name: str=None

   
    class Config:
        orm_mode=True


