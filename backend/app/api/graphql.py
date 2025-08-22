import datetime
import uuid
from typing import List, Optional
import strawberry

from app.db.models import Patient as PatientModel, Appointment as AppointmentModel
from app.db.database import get_db_session
from app.services.patient_services import ingest_patients_from_csv

@strawberry.type
class Appointment:
    id: uuid.UUID
    appointment_id: str
    appointment_date: Optional[datetime.datetime]
    appointment_type: Optional[str]

@strawberry.type
class Patient:
    id: uuid.UUID
    patient_id: str
    first_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[datetime.date]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    is_complete: bool
    appointments: List[Appointment]


    @strawberry.field
    def name(self) -> str:
        first_name = self.first_name if self.first_name else ""
        return f"{first_name} {self.last_name}"
    
    @strawberry.field
    def age(self) -> int:
        if not self.dob:
            return 0
        return datetime.datetime.now().year - self.dob.year
    
    @strawberry.field
    def appointment_count(self) -> int:
        return len(self.appointments)

@strawberry.type
class Query:
    @strawberry.field
    async def patients(self, info) -> List[Patient]:
        from sqlalchemy.future import select
        from sqlalchemy.orm import selectinload
        from sqlalchemy.ext.asyncio import AsyncSession

        session: AsyncSession = info.context["db_session"]
        result = await session.execute(select(PatientModel).options(selectinload(PatientModel.appointments)))
        return result.scalars().all()

    @strawberry.field
    async def patient(self, info, id: uuid.UUID) -> Optional[Patient]:
        from sqlalchemy.future import select
        from sqlalchemy.orm import selectinload
        from sqlalchemy.ext.asyncio import AsyncSession

        session: AsyncSession = info.context["db_session"]
        result = await session.execute(
            select(PatientModel)
            .where(PatientModel.id == id)
            .options(selectinload(PatientModel.appointments))
        )
        return result.scalars().first()

@strawberry.type
class IngestCsvResult:
    success: bool
    message: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def ingest_csv_data(self, info) -> IngestCsvResult:
        from sqlalchemy.ext.asyncio import AsyncSession
        session: AsyncSession = info.context["db_session"]
        try:
            await ingest_patients_from_csv(session)
            return IngestCsvResult(success=True, message="CSV data ingested successfully")
        except Exception as e:
            return IngestCsvResult(success=False, message=f"Error ingesting CSV data: {str(e)}")

schema = strawberry.Schema(query=Query, mutation=Mutation)