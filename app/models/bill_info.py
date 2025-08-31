from sqlalchemy.orm import relationship

from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float

class BillInfo(Base):
    __tablename__ = "bill_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    purchased_billed_id = Column(String, unique=True )
    status = Column(String, default="paid")
    total_bill_amount = Column(Integer, nullable=False ,default=0)
    pay_bill_amount = Column(Integer, nullable=False, default=0)
    remaining_amount = Column(Integer, nullable=False, default=0)
    discount = Column(Integer, default=0)

    visit = relationship("Visit", back_populates="bill_info")


