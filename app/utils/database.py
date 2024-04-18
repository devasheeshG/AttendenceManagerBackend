# Path: app/utils/database.py
# Description: Database Client for PostgreSQL.

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create the database if it doesn't exist
if not database_exists(settings.get_postgres_uri()):
    create_database(settings.get_postgres_uri())

# Create the engine
engine = create_engine(settings.get_postgres_uri())

# Create the session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class
DatabaseBase = declarative_base()

def get_db():
    """Get Database Session."""
    db = Session()
    try:
        yield db
    finally:
        db.close()
