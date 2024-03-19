# Path: app/routers/timetable.py
# Description: This file contains routers for SRM Timetable API.

import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Dict
from app.utils.attendance_manager import AttendanceManager
from app.utils import database

router = APIRouter(tags=['TimeTable'], prefix='/timetable', dependencies=[Depends(database.get_db)])

@router.get("/", responses={
    200: {
        "model": Dict[str, Dict[str, str]],
        "description": "Timetable fetched successfully."
    },
    401: {
        "description": "Invalid Username or Password"
    },
    503: {
        "description": "SRM Student Portal is Down or Login Failed. Try Again Later."
    }
})
async def get_timetable(request: Request, refresh: bool = False, db: Session = Depends(database.get_db)):
    """Get Timetable."""
    if refresh:
        # Create Attendance Manager Instance
        am = AttendanceManager()
        await am.login()

        # Get Timetable
        timetable = await am.get_timetable(db)
        
        # Update Cache
        request.app.cached_timetable = timetable
        with open('cache/timetable.json', 'w') as f:
            f.write(json.dumps(timetable, indent=4))
        
        # Close Attendance Manager
        await am.close()

    else:
        timetable = request.app.cached_timetable
    
    return timetable
