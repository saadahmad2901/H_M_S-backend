from typing import  Optional
from datetime import datetime,date,time
from pydantic import BaseModel

class ServiceBase(BaseModel):
    name:str
    description:Optional[str]=None
    price:float
    

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    description:Optional[str]=None
    price:float


class Service(ServiceBase):
    id:int
    class Config:
        orm_mode=True




