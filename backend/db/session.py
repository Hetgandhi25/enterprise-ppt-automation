import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import urllib.parse

# The user explicitly provided: Het@2004 for local postgresql
# Using synchronous driver psycopg2 since the DB initialization and pandas scripts are synchronous
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Het@2004")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "custppt")

encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# Connection String
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Setup Engine and SessionLocal
try:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Failed to create database engine. Ensure PostgreSQL is running. Error: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
