# /backend/generate_sql.py

from app.db.models import Base
from app.db.database import engine
from sqlalchemy.schema import CreateTable

def generate_ddl():
    with open("queries.sql", "w") as f:
        f.write(str(CreateTable(Base.metadata.tables['patients'])))
        f.write("\n\n")
        f.write(str(CreateTable(Base.metadata.tables['appointments'])))
        f.write("\n")

if __name__ == "__main__":
    generate_ddl()