from typing import Optional
from pydantic import BaseModel


class BillBase(BaseModel):
    visit_id: int
    purchased_billed_id: Optional[str] = None
    status: str
    total_bill_amount: int
    pay_bill_amount: int
    remaining_amount: int
    discount: int


class BillCreate(BillBase):
    pass


class BillUpdate(BillBase):
    pass


class BillOut(BillBase):
    id: int

    class Config:
        orm_mode = True
