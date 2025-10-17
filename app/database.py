# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the database URL. For SQLite, this is the path to the file.
# The file will be created in the root of our project as 'studysphere.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./studysphere.db"

# 2. Create the SQLAlchemy 'engine'.
# The engine is the main entry point to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class.
# Each instance of a SessionLocal will be a single database session (a conversation).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class.
# Our data model classes (like ProcessedDocument) will inherit from this class.
Base = declarative_base()