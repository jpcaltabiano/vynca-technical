# Vynca - Technical Assessment
### Submitted by Joseph Caltabiano
---
### Setup Instructions

First, install the packages required for the backend and start:
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Then, we create the database.

Option 1 (using queries + sqlite3 CLI tool):
```
sqlite3 app.db < queries.sql

curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { ingestCsvData { success message } }"}'
```

Option 2 (using GraphiQL):
- Navigate to `localhost:8000/graphql` in the browser
- In the editor, paste in the following command and press the run button
```
mutation {
    ingestCsvData { success message }
}
```

Then, start the frontend:
```
cd ../frontend
npm i
npm run start
```

---

I developed the backend using SQLite. I used SQLAlchemy to establish data models, aiosqlite to handle asynchronous database operations, and Strawberry GraphQL to design the API. `Patient` and `Appointment` data models describe the structure of patient and appointment data. They use UUID primary keys, uniqueness on the patient ID, appointment ID, and patient email. I use a one-to-many relationship on a `Patient` to store a list of their `Appointment`s. In the Strawberry type, I also provide a field for the number of appointments.

I also have added a boolean field `is_complete` to a `Patient` that I compute during ingestion. Since it is critical to preserve patient information, even when incomplete, I keep all given rows. However, I require a last name, a DOB, and either a valid phone number or email in order to consider a patient `is_complete==True`. This allows me to show a flag on the frontend, warning the user that the patient record is missing some ciritcal information. 

The API is written using Strawberry GraphQL + FastAPI, exposing queries for all patients, all appointments, and a single patient + their appointments (identified via UUID). I also provide the mutation `ingest_csv_data` to ingest the data from the provided .txt file. I define my own validation functions, then use Pydantic to validate. 

For emails, I clean the various formats into one and enforce a name@domain.xyz format. For phone, I toss placeholder numbers, format everything into a +1... 11-digit format, and preserve numbers that are smaller (eg missing area code). The is_complete check does not consider a phone number valid if the area code is missing. I clean the address and remove none/unknown values and provide date parsing to handle multiple date formats. Rows failing validation are safely skipped (patient rows are ignored; appointment rows are ignored independently), and transactions are rolled back on unexpected errors. A small helper (generate_sql.py) can emit the DDL to queries.sql for visibility into the schema.

On the frontend, I used React in Typescript with MUI for themeing and components, and Apollo Client for the GraphQL queries. On load, I grab all the patients and their info in the list view. This renders a table with pretinent patient info. The patient missing critical information is flagged, and clicking the warning icon produces a modal explaining the warning. On clicking a patient row, the detail view on the right of the page is populated with 1) a card showing the patient information and 2) a table showing the appointments the patient has.