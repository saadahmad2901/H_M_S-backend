from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

class VisitService(Base):
    __tablename__ = "visit_services"

    id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_billed = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    purchased_billed_id = Column(String,  nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    visit = relationship("Visit", back_populates="visit_services")
    service = relationship("Services", back_populates="visit_services")

