
CREATE TABLE patients (
	id UUID NOT NULL, 
	patient_id VARCHAR, 
	first_name VARCHAR, 
	last_name VARCHAR, 
	dob DATE, 
	email VARCHAR, 
	phone VARCHAR, 
	address VARCHAR, 
	is_complete BOOLEAN, 
	PRIMARY KEY (id)
);




CREATE TABLE appointments (
	id UUID NOT NULL, 
	appointment_id VARCHAR, 
	appointment_date DATETIME, 
	appointment_type VARCHAR, 
	patient_uuid UUID, 
	PRIMARY KEY (id), 
	FOREIGN KEY(patient_uuid) REFERENCES patients (id)
);



CREATE UNIQUE INDEX IF NOT EXISTS uq_patients_patient_id ON patients(patient_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_patients_email ON patients(email);
CREATE UNIQUE INDEX IF NOT EXISTS uq_appointments_appointment_id ON appointments(appointment_id);