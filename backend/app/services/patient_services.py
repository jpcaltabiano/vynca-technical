## A file containing helper functions for loading and cleaning the data
# things to do:
# names not capitalized, leading/trailing spaces
# dates in multiple formats, including european and american
    # convert all to one format, determine how to handle euro dates when ambiguous
# emails contain diff formats, @/[at], some domains have one part or are "email"
# phones numbers have diff formats, dashes/slashes, int format, not real phone numbers (less than 10 digits)
# most addresses contain only street, assume correct format. malformed ones include a extra comma and one has apt number and one has the town name
# addresses contain diff street type format ex "st" and "street"
# some missing appointment_id
# appointment dates also in different formats, handle w generic helper

# on FE, put a flag on patients missing large amounts of critical data ?

import os
from typing import Optional
import csv
import re
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ValidationError, validator, EmailStr, root_validator
from app.db.models import Patient as PatientModel, Appointment as AppointmentModel


# helper cleaners and date parser
def _clean_email(value: Optional[str]) -> Optional[str]:
	if value is None:
		return None
	s = str(value).strip().lower()
	if not s:
		return None
	# convert all formats to'@'
	s = s.replace("[at]", "@").replace("(at)", "@")
	# require an '@' else return None
	if "@" not in s:
		return None
	return s


def _clean_phone(value: Optional[str]) -> Optional[str]:
	# produce +1XXXXXXXXXX for valid US numbers (does not handle international)
	# partial numbers are preserved but not considered "contactable"
	if value is None:
		return None
	raw = str(value).strip()
	starts_plus = raw.startswith("+")
	digits = re.sub(r"\D", "", raw)
	if len(digits) == 0:
		return None
	# capture placeholder/fake numbers - also check non-complete numbers
	core = digits[-10:] if len(digits) >= 10 else digits
	if len(core) >= 7:
		# if number is only one digit repeated, return None
		if len(set(core)) == 1:
			return None
		# if number is a common placeholder, return None
		if core in {"1234567890", "0123456789", "9876543210"}:
			return None
	if starts_plus:
		# accept only +1XXXXXXXXXX (11 digits total after '+')
		if digits.startswith("1") and len(digits) == 11:
			return f"+{digits}"
		return digits
	if len(digits) >= 11 and digits.startswith("1"):
		return f"+{digits}"
	if len(digits) == 10:
		return f"+1{digits}"
	# preserve partial numbers (ex missing area code)
	if 7 <= len(digits) <= 9:
		return digits
	return None


def _clean_address(value: Optional[str]) -> Optional[str]:
    # keeps as a single field, does not standardize suffixes or units
    # and does not break out apt/city/state/zip etc
    # future work would make this check far more robust and could also break out apt/city/state/zip etc
	if value is None:
		return None
	s = str(value).strip().strip('"').strip("'")
	if not s:
		return None

	# normalize comma spacing and extra spaces; remove leading/trailing commas
	s = re.sub(r"\s*,\s*", ", ", s)
	s = re.sub(r"\s+", " ", s).strip(", ").strip()

	# drop the address if it contains placeholder 'unknown' or 'none'
	if re.search(r"\b(unknown|none)\b", s, flags=re.IGNORECASE):
		return None
	return s


def _parse_human_date(value: Optional[object]):
	# returns a date or None and defers typing to Pydantic coercion
	if value is None or (isinstance(value, str) and not value.strip()):
		return None
	if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
		return value
	if isinstance(value, datetime.datetime):
		return value.date()

	s = str(value).strip()
	if s.lower() in {"none", "unknown"}:
		return None

	# formats observed in the provided dataset:
	# - MM/DD/YYYY
	# - YYYY-MM-DD
	# - MM-DD-YYYY
	# - YYYY/MM/DD
	# - monthname DD YYYY (e.g., April 25 1977)

	# monthname DD YYYY and variations
	for fmt in ("%B %d %Y", "%B %d, %Y", "%b %d %Y", "%b %d, %Y"):
		try:
			return datetime.datetime.strptime(s, fmt).date()
		except ValueError:
			pass

	# year-first with dash or slash
	for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
		try:
			return datetime.datetime.strptime(s, fmt).date()
		except ValueError:
			pass

	# month-first with dash or slash
	for fmt in ("%m-%d-%Y", "%m/%d/%Y"):
		try:
			return datetime.datetime.strptime(s, fmt).date()
		except ValueError:
			pass

	return None

def _is_complete_patient(values: dict) -> bool:
	# completeness: required last_name, dob; contact: valid email OR valid phone; and patient_id
    # allows for setting the is_complete flag on the patient object,
    # which can be used on the FE to flag patients missing large amounts of critical data
	patient_id = (values.get("patient_id") or "").strip()
	last_name = values.get("last_name")
	dob = values.get("dob")
	email = values.get("email")
	phone = values.get("phone")
	if not patient_id:
		return False
	if not last_name or not dob:
		return False
	# check if phone is contactable - missing area code is not contactable
	digits = re.sub(r"\D", "", str(phone or ""))
	contactable_phone = (len(digits) == 10) or (len(digits) == 11 and digits.startswith("1"))
	if not (email or contactable_phone):
		return False
	return True


class PatientData(BaseModel):
	patient_id: str
	first_name: Optional[str]
	last_name: str
	dob: Optional[datetime.date]
	email: Optional[EmailStr]
	phone: Optional[str]
	address: Optional[str]
	is_complete: bool = False

	@validator("patient_id", pre=True)
	def _strip_patient_id(cls, v):
		if v is None:
			return v
		return str(v).strip()

	@validator("first_name", pre=True)
	def _normalize_first_name(cls, v):
		if v is None:
			return None
		s = str(v).strip()
		return s.title() if s else None

	@validator("last_name", pre=True)
	def _normalize_last_name(cls, v):
		if v is None:
			return v
		s = str(v).strip()
		return s.title()

	@validator("email", pre=True)
	def _validate_email(cls, v):
		return _clean_email(v)

	@validator("phone", pre=True, always=True)
	def _validate_phone(cls, v):
		return _clean_phone(v)

	@validator("address", pre=True)
	def _validate_address(cls, v):
		return _clean_address(v)

	@validator("dob", pre=True)
	def _validate_dob(cls, v):
		return _parse_human_date(v)

	@root_validator(pre=False)
	def _set_is_complete(cls, values):
		values["is_complete"] = _is_complete_patient(values)
		return values


class AppointmentData(BaseModel):
	appointment_id: Optional[str]
	appointment_date: Optional[datetime.date]
	appointment_type: Optional[str]

	@validator("appointment_id", pre=True)
	def _normalize_aid(cls, v):
		if v is None:
			return None
		s = str(v).strip()
		return s or None

	@validator("appointment_type", pre=True)
	def _normalize_appointment_type(cls, v):
		if v is None:
			return None
		s = str(v).strip()
		return s or None

	@validator("appointment_date", pre=True)
	def _validate_appointment_date(cls, v):
		return _parse_human_date(v)

def ingest_patients_from_csv(session: AsyncSession):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_file_path = os.path.join(BASE_DIR, "patients_and_appointments.txt")