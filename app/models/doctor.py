from sqlalchemy import Column, String, Integer, Float, Date, Time, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum

class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class DoctorStatus(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    cnic = Column(String, unique=True, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    qualification = Column(String)
    specialization = Column(String)
    experience_years = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))
    available_days = Column(String)
    available_time_from = Column(Time)
    available_time_to = Column(Time)
    consultation_fee = Column(Float)
    status = Column(Enum(DoctorStatus), default=DoctorStatus.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = relationship("Department", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")
    visits = relationship("Visit", back_populates="doctor")
