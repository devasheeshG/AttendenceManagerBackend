# Path: app/routers/subject_alias.py
# Description: This file contains routers to create and manage subject aliases.

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.utils.attendance_manager import AttendanceManager
from app.utils import database, models, schemas
from app.config import settings

router = APIRouter(
    prefix='/alias',
    tags=['Subject Alias']
)

# add a new alias for a subject code
@router.post("/", responses={
    201: {
        "model": schemas.ResponseGetSubjectDetails,
        "description": "Alias added successfully.",
        "content": {
            "application/json": {"example": {"subject_code": "21CSC204J", "subject_name": "Design and Analysis of Algorithms", "alias": "DAA"}}
        }
    },
    404: {
        "model": schemas.ErrorResponse,
        "description": "`SubjectName` for given `SubjectCode` not found on SRM Portal."
    },
    409: {
        "model": schemas.ErrorResponse,
        "description": "Alias already exists for the given `SubjectCode`."
    },
})
async def add_subject_alias(data: schemas.CreateSubjectAlias, db: Session = Depends(database.get_db)):
    # FIXME: This comment is not being displayed properly on FastAPI Swagger UI Docs.
    """Add Alias of a Subject.

    If the subject code is not present:
        1. First, get the subject name from `get_subject_name_from_subject_code_form_timetable_page` function of `attendance_manager.py`.
            1.1. If subject name is not found, raise an HTTPException with status code 404.
            1.2. If subject name is found, add the subject code, subject name and alias to the database.

    If the subject code is present and alias is None, add the alias to the database.
    """
    
    # Check if the subject code is present in the database
    subject = db.query(models.Subjects).filter(models.Subjects.SubjectCode == data.subject_code).first()
    
    # If the subject code is present
    if subject:
        # If the alias is already present
        if subject.Alias:
            raise HTTPException(status_code=409, detail=f"Alias already exists for Subject Code {data.subject_code}")
        
        # Add the alias to the database
        subject.Alias = data.alias
        db.commit()
        return JSONResponse({"subject_code": subject.SubjectCode, "subject_name": subject.SubjectName, "alias": data.alias}, status_code=status.HTTP_201_CREATED)
    
    # If the subject code is not present
    else:
        # Create Attendance Manager Instance
        am = AttendanceManager()
        await am.login()
        
        # Get the subject name from the subject code
        subject_name = await am.get_subject_name_from_subject_code_from_timetable_page(data.subject_code)
        
        # Close the Attendance Manager Instance
        await am.close()
        
        if not subject_name:
            raise HTTPException(status_code=404, detail=f"Subject Name for Subject Code {data.subject_code} not found for user {settings.SRM_PORTAL_USERNAME}")
        
        try:
            # Add the subject code, subject name and alias to the database
            new_subject = models.Subjects(SubjectCode=data.subject_code, SubjectName=subject_name, Alias=data.alias)
            db.add(new_subject)
            db.commit()
            return JSONResponse({"subject_code": data.subject_code, "subject_name": subject_name, "alias": data.alias}, status_code=status.HTTP_201_CREATED)
        
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=409, detail=f"Alias already exists for Subject Code {data.subject_code}")

@router.get("/", responses={
    200: {
        "model": schemas.ResponseGetSubjectDetails,
        "description": "Subject details for the given query parameter.",
        "content": {
            "application/json": {"example": {"subject_code": "21CSC204J", "subject_name": "Design and Analysis of Algorithms", "alias": "DAA"}}
        }
    },
    400: {
        "model": schemas.ErrorResponse,
        "description": "Please provide subject_code, alias, or subject_name as a query parameter."
    },
    404: {
        "model": schemas.ErrorResponse,
        "description": "Subject not found for the given query parameter."
    },
})
async def get_subject_details(subject_code: str = None, alias: str = None, subject_name: str = None, db: Session = Depends(database.get_db)) -> schemas.ResponseGetSubjectDetails:
    """Get Subject details by subject code, alias, or subject name."""
    if subject_code:
        subject = db.query(models.Subjects).filter(models.Subjects.SubjectCode == subject_code).first()
        if not subject:
            raise HTTPException(status_code=404, detail=f"Alias not found for Subject Code {subject_code}")
    elif alias:
        subject = db.query(models.Subjects).filter(models.Subjects.Alias == alias).first()
        if not subject:
            raise HTTPException(status_code=404, detail=f"Subject not found for Alias {alias}")
    elif subject_name:
        subject = db.query(models.Subjects).filter(models.Subjects.SubjectName == subject_name).first()
        if not subject:
            raise HTTPException(status_code=404, detail=f"Subject not found for Subject Name {subject_name}")
    else:
        raise HTTPException(status_code=400, detail="Please provide subject_code, alias, or subject_name as a query parameter.")

    return JSONResponse({"subject_code": subject.SubjectCode, "subject_name": subject.SubjectName, "alias": subject.Alias}, status_code=status.HTTP_200_OK)

@router.delete("/", responses={
    204: {
        "description": "Alias deleted successfully."
    },
    404: {
        "model": schemas.ErrorResponse,
        "description": "Alias not found for the given query parameter."
    },
})
async def delete_subject_alias(subject_code: str = None, alias: str = None, subject_name: str = None, db: Session = Depends(database.get_db)):
    """Delete Alias of a Subject."""
    if subject_code:
        subject = db.query(models.Subjects).filter(models.Subjects.SubjectCode == subject_code).first()
        if not subject:
            raise HTTPException(status_code=404, detail=f"Alias not found for Subject Code {subject_code}")
    elif alias:
        subject = db.query(models.Subjects).filter(models.Subjects.Alias == alias).first()
        if not subject:
            raise HTTPException(status_code=404, detail=f"Subject not found for Alias {alias}")
    elif subject_name:
        subject = db.query(models.Subjects).filter(models.Subjects.SubjectName == subject_name).first()
        if not subject:
            raise HTTPException(status_code=404, detail=f"Subject not found for Subject Name {subject_name}")
    else:
        raise HTTPException(status_code=400, detail="Please provide subject_code, alias, or subject_name as a query parameter.")
    
    db.delete(subject)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/", responses={
    200: {
        "model": schemas.ResponseGetSubjectDetails,
        "description": "Alias updated successfully.",
        "content": {
            "application/json": {"example": {"subject_code": "21CSC204J", "subject_name": "Design and Analysis of Algorithms", "alias": "DAA"}}
        }
    },
    404: {
        "model": schemas.ErrorResponse,
        "description": "Alias not found for the given query parameter."
    },
})
async def update_subject_alias(data: schemas.CreateSubjectAlias, db: Session = Depends(database.get_db)):
    """Update Alias of a Subject."""
    subject = db.query(models.Subjects).filter(models.Subjects.SubjectCode == data.subject_code).first()
    if not subject:
        raise HTTPException(status_code=404, detail=f"Alias not found for Subject Code {data.subject_code}")
    
    subject.Alias = data.alias
    db.commit()
    return JSONResponse({"subject_code": subject.SubjectCode, "subject_name": subject.SubjectName, "alias": data.alias}, status_code=status.HTTP_200_OK)
