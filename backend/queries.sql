
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
)




CREATE TABLE appointments (
	id UUID NOT NULL, 
	appointment_id VARCHAR, 
	appointment_date DATETIME, 
	appointment_type VARCHAR, 
	patient_uuid UUID, 
	PRIMARY KEY (id), 
	FOREIGN KEY(patient_uuid) REFERENCES patients (id)
)


