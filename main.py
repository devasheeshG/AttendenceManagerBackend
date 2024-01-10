"""Main File for FastAPI SRM Student Portal Attendance Manager API."""

import asyncio
from contextlib import asynccontextmanager
import datetime
from fastapi import FastAPI, Form, HTTPException
from utils.database import Database
from utils.update_attendence_database import update_attendence_database
from utils.attendance_manager import AttendanceManager
from utils.data_models import User
from utils.notifications import Notifications


async def update_attendence():
    """Update Attendence Database."""
    while True:
        db = Database()
        users = db.get_all_users()
        tasks = []
        for username, password in users:
            tasks.append(
                update_attendence_database(
                    username, password, AttendanceManager, db.cursor, db.conn
                )
            )

        result = await asyncio.gather(*tasks)
        print("Today:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for r in result:
            print(r)
        del db
        await asyncio.sleep(1000)


# Schedule the update_attendence_database function to run every 10min for each user
@asynccontextmanager
async def update_attendence_lifespan(app: FastAPI):
    print("Starting Update Attendence Lifespan")
    asyncio.create_task(update_attendence())
    yield
    print("Stopping Update Attendence Lifespan")


app = FastAPI(
    title="SRM Student Portal Attendance Manager API",
    description="API to get SRM Student Portal Attendance Details",
    version="0.0.1",
    docs_url=None,
    redoc_url=None,
    lifespan=update_attendence_lifespan,
)


@app.post("/get_attendance_details")
async def get_attendance(
    username: str = Form(default=""), password: str = Form(default="")
):
    """Get Attendance Details."""
    # Check Username and Password
    user = User(username=username, password=password)
    err_msg = user.check_username_password()
    if err_msg:
        raise HTTPException(status_code=400, detail=err_msg)

    # Create Attendance Manager Instance
    attendance_manager = AttendanceManager(user.username, user.password)

    # Login
    try:
        await attendance_manager.login()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Get Attendance Details
    course_wise_attendance, monthly_absent_hours = (
        await attendance_manager.get_attendance_details()
    )

    await attendance_manager.close()

    return {
        "CourseWiseAttendance": course_wise_attendance,
        "MonthlyAttendance": monthly_absent_hours,
    }


@app.post("/get_timetable")
async def get_timetable(
    username: str = Form(default=""), password: str = Form(default="")
):
    """Get Timetable."""
    # Check Username and Password
    user = User(username=username, password=password)
    err_msg = user.check_username_password()
    if err_msg:
        raise HTTPException(status_code=400, detail=err_msg)

    # Create Attendance Manager Instance
    attendance_manager = AttendanceManager(user.username, user.password)

    # Login
    try:
        await attendance_manager.login()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Get Timetable
    timetable = await attendance_manager.get_timetable()

    await attendance_manager.close()

    return {"Timetable": timetable}


@app.post("/notifications/register")
async def register_user(
    username: str = Form(default=""), password: str = Form(default="")
):
    """Register User."""
    # Check Username and Password
    user = User(username=username, password=password)
    err_msg = user.check_username_password()
    if err_msg:
        raise HTTPException(status_code=400, detail=err_msg)

    # Create Attendance Manager Instance
    attendance_manager = AttendanceManager(user.username, user.password)

    # Try to Login to check if the credentials are valid
    try:
        await attendance_manager.login()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Add User to Database
    db = Database()
    status = db.add_user(user.username, user.password)
    return status


@app.post("/notifications/unregister")
async def unregister_user(username: str = Form(default="")):
    """Unregister User."""
    # Check Username
    if not username:
        raise HTTPException(
            status_code=400, detail="username is required form parameter"
        )

    # Remove User from Database
    db = Database()
    status = db.remove_user(username)
    return status


@app.post("/notifications/unread")
async def get_unread_notifications(username: str = Form(default="")):
    """Get Notifications."""
    # Check Username
    if not username:
        raise HTTPException(
            status_code=400, detail="username is required form parameter"
        )

    # Check if User Exists in Database
    db = Database()
    if username not in [user for user, _ in db.get_all_users()]:
        raise HTTPException(
            status_code=400, detail=f"{username}: User Not registered for Notifications"
        )

    return Notifications().retrieve_unread_notifications(username)


@app.post("/notifications/all")
async def get_all_notifications(username: str = Form(default="")):
    """Get Notifications."""
    # Check Username
    if not username:
        raise HTTPException(
            status_code=400, detail="username is required form parameter"
        )

    # Check if User Exists in Database
    db = Database()
    if username not in [user for user, _ in db.get_all_users()]:
        raise HTTPException(
            status_code=400, detail=f"{username}: User Not registered for Notifications"
        )

    return Notifications().retrieve_all_notifications(username)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
