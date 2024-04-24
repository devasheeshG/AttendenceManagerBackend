# Path: app/utils/schemas.py
# Description: This file contains schemas for API Endpoints.

from pydantic import BaseModel

class CreateSubjectAlias(BaseModel):
    subject_code: str
    alias: str

class ResponseGetSubjectDetails(CreateSubjectAlias):
    subject_name: str

class ErrorResponse(BaseModel):
    detail: str