import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

from backend.db.models import Base
from backend.db.session import engine, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def create_database_if_not_exists():
    """Connects to the default 'postgres' database to create 'custppt' if it doesn't exist."""
    print(f"Connecting to PostgreSQL at {DB_HOST}:{DB_PORT} as {DB_USER}...")
    try:
        # Connect to default database
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if target db exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Database '{DB_NAME}' does not exist. Creating it now...")
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        print("Please ensure PostgreSQL is running and credentials are correct.")
        raise

def initialize_schema():
    """Uses SQLAlchemy to create all tables defined in models.py"""
    print("Initializing database schema...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Schema initialization complete! All tables have been successfully created.")
    except Exception as e:
        print(f"Failed to create schema: {e}")
        raise

if __name__ == "__main__":
    create_database_if_not_exists()
    initialize_schema()
