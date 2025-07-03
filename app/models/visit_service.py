from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class VisitService(Base):
    __tablename__ = "visit_services"

    id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

 
    visit = relationship("Visit", back_populates="visit_services")
    service = relationship("Services", back_populates="visit_services")
