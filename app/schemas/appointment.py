from typing import Optional
from datetime import date, time
from pydantic import BaseModel
from app.models.appointment import AppointmentTypeEnum, StatusEnum, PaymentStatusEnum, PaymentMethodEnum, BookingSourceEnum

class AppointmentBase(BaseModel):
    patient_id: int
    department_id: int
    doctor_id: int
    date: date
    time: time
    reason_for_visit: str
    appointment_type: AppointmentTypeEnum
    status: StatusEnum
    doctor_fee: Optional[float] = None
    payment_status: PaymentStatusEnum
    payment_method: Optional[PaymentMethodEnum] = None
    remarks: Optional[str] = None
    duration: Optional[str] = None
    booking_source: Optional[BookingSourceEnum] = None
    location_or_room: Optional[str] = None
    cancellation_reason: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    date: Optional[date] = None
    time: Optional[time] = None
    reason_for_visit: Optional[str] = None
    appointment_type: Optional[AppointmentTypeEnum] = None
    status: Optional[StatusEnum] = None
    doctor_fee: Optional[float] = None
    payment_status: Optional[PaymentStatusEnum] = None
    payment_method: Optional[PaymentMethodEnum] = None
    remarks: Optional[str] = None
    duration: Optional[str] = None
    booking_source: Optional[BookingSourceEnum] = None
    location_or_room: Optional[str] = None
    cancellation_reason: Optional[str] = None

class Appointment(AppointmentBase):
    id: int


    class Config:
        orm_mode = True

class AppointmentWithDetails(BaseModel):
    appointment: Appointment
    patient_name: str
    department_name: str
    doctor_name: str