# define the models for a patient and appointment using SQLalchemy

import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    # patient_id,first_name,last_name,dob,email,phone,address,appointment_id,appointment_date,appointment_type

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(String, unique=True, index=True) # patient_id
    first_name = Column(String, index=True) # first_name
    last_name = Column(String, index=True) # last_name
    dob = Column(Date) # dob
    email = Column(String, unique=True, index=True) # email
    phone = Column(String, nullable=True) # phone
    address = Column(String, nullable=True) # address
    appointments = relationship("Appointment", back_populates="patient")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # appointment_id
    appointment_date = Column(DateTime) # appointment_date
