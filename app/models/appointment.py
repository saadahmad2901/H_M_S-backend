from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Text, Enum, Float
from sqlalchemy.orm import relationship
from app.db import Base
import enum


class AppointmentTypeEnum(str, enum.Enum):
    new = "New"
    follow_up = "Follow-up"
    online = "Online"
    emergency = "Emergency"


class StatusEnum(str, enum.Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    cancelled = "Cancelled"
    completed = "Completed"


class PaymentStatusEnum(str, enum.Enum):
    paid = "Paid"
    unpaid = "Unpaid"
    partial = "Partial"


class PaymentMethodEnum(str, enum.Enum):
    cash = "Cash"
    online = "Online"
    card = "Card"
    insurance = "Insurance"


class BookingSourceEnum(str, enum.Enum):
    web = "Web"
    mobile = "Mobile"
    walk_in = "Walk-In"
    call = "Call"
    wa_bot = "WA-Bot"
    ig_bot = "IG-Bot"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)

    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    reason_for_visit = Column(Text, nullable=True)
    appointment_type = Column(Enum(AppointmentTypeEnum), nullable=True)
    status = Column(Enum(StatusEnum), nullable=True, default=StatusEnum.pending)

    doctor_fee = Column(Float, nullable=True)
    payment_status = Column(Enum(PaymentStatusEnum), nullable=True, default=PaymentStatusEnum.unpaid)
    payment_method = Column(Enum(PaymentMethodEnum), nullable=True)

    remarks = Column(Text, nullable=True)
    duration = Column(String, nullable=True)
    booking_source = Column(Enum(BookingSourceEnum), nullable=True)
    location_or_room = Column(String, nullable=True)
    cancellation_reason = Column(Text, nullable=True)

    # Relationships (Optional, depending on your ORM setup)
    patient = relationship("Patient", back_populates="appointments")
    department = relationship("Department", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    visits = relationship("Visit", back_populates="appointment")
