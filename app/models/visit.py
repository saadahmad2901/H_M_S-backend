import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.db import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    check_in_time = Column(DateTime, default=datetime.utcnow)
    check_out_time = Column(DateTime, nullable=True)

    visit_status = Column(Text, nullable=False)
    reason_for_visit = Column(Text, nullable=False)
    vitals = Column(Text, nullable=True, default="None Vitals")
    diagnosis = Column(Text, nullable=True, default="None Diagnosis")
    notes = Column(Text, nullable=True, default="None Notes")
    follow_up_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional relationships
    appointment = relationship("Appointment", back_populates="visits")
    patient = relationship("Patient", back_populates="visits")
    doctor = relationship("Doctor", back_populates="visits")
    visit_services = relationship("VisitService", back_populates="visit")
