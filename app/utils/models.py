# Path: app/utils/models.py
# Description: This file contains the Pydantic models for the application.

from app.utils.database import DatabaseBase
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint, Time, VARCHAR

class Subjects(DatabaseBase):
    __tablename__ = "subjects"
    
    SubjectCode = Column(VARCHAR(10), nullable=False, primary_key=True)
    SubjectName = Column(String, nullable=False)
    Alias = Column(String, nullable=False)

