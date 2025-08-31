from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base  # adjust based on your actual import

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=True) 
    gender = Column(String, nullable=False)
    cnic = Column(String(15), unique=True, nullable=False)
    contact_number = Column(String, nullable=False)
    emergency_contact_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    marital_status = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    known_allergies = Column(String, nullable=True)
    existing_conditions = Column(String, nullable=True)
    current_condition = Column(String, nullable=True)
    preferred_language = Column(String, nullable=True)
    referred_by = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    remarks = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Appointment model
    appointments = relationship("Appointment", back_populates="patient")
    visits = relationship("Visit", back_populates="patient")

