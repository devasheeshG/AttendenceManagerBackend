# Path: app/routers/attendance.py
# Description: This file contains routers for viewing attendance details.

from fastapi import APIRouter, Depends, status, HTTPException, Response, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.utils.attendance_manager import AttendanceManager
from app.utils import database, models, schemas
from app.config import settings

router = APIRouter(
    prefix='/attendance',
    tags=['Student Attendance']
)

@router.post("/")
async def get_attendance_details():
    """Get Attendance Details."""
    # Create Attendance Manager Instance
    am = AttendanceManager()

    # Login to SRM Student Portal
    await am.login()

    # Get Attendance Details
    course_wise_attendance, monthly_absent_hours = await am.get_attendance_details()

    await am.close()

    return {
        "CourseWiseAttendance": course_wise_attendance,
        "MonthlyAttendance": monthly_absent_hours,
    }