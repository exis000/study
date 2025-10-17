f# app/models.py
from sqlalchemy import Column, Integer, String, Text
from .database import Base

# This class defines the blueprint for our 'documents' table
class ProcessedDocument(Base):
    # The name of the actual database table
    __tablename__ = "processed_documents"

    # Define the columns (the fields for our table)
    # The 'id' column will be our unique identifier for each document
    id = Column(Integer, primary_key=True, index=True)

    # The filename of the original uploaded file
    filename = Column(String(255), index=True)

    # The full, restored text from OCR. We use Text for long strings.
    extracted_text = Column(Text)

    # The AI-generated summary. Also Text for long strings.
    summary = Column(Text)