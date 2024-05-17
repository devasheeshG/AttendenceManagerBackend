"""Main File for FastAPI SRM Student Portal Attendance Manager API."""

import os
import json
import asyncio
from contextlib import asynccontextmanager
from app.logging import logger
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
# from app.utils.update_attendence_database import update_attendence_database
from app.utils.attendance_manager import AttendanceManager
from app.routers import timetable, subject_alias, attendance
from app.utils import database

# async def update_attendence():
#     """Update Attendence Database."""
#     while True:
#         db = Database()
#         users = db.get_all_users()
#         tasks = []
#         for username, password in users:
#             tasks.append(
#                 update_attendence_database(
#                     username, password, AttendanceManager, db.cursor, db.conn
#                 )
#             )

#         result = await asyncio.gather(*tasks)
#         print("Today:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         for r in result:
#             print(r)
#         del db
#         await asyncio.sleep(1000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Lifespan")

    while True:
        if os.path.exists('cache/timetable.json'):
            with open('cache/timetable.json', 'r') as f:
                app.cached_timetable = json.loads(f.read())
                logger.info("Timetable Cached")
                break
        else:
            try:
                am = AttendanceManager()
                await am.login()
                # FIXME: db should be a dependency
                db: Session = next(database.get_db())
                app.cached_timetable = await am.get_timetable(db)
                
                # Write Timetable to Cache
                with open('cache/timetable.json', 'w') as f:
                    f.write(json.dumps(app.cached_timetable, indent=4))
                
                logger.info("Timetable Cached")
                break
            
            except HTTPException as e:
                logger.error(f"Error in caching timetable: {e}")
                await asyncio.sleep(2)
                
            finally:
                await am.close()
    
    # asyncio.create_task(update_attendence())
    yield
    logger.info("Stopping Lifespan")

app = FastAPI(
    title="SRM Student Portal Attendance Manager API",
    description="API to get SRM Student Portal Attendance Details",
    version="0.0.1",
    docs_url='/docs',
    redoc_url=None,
    lifespan=lifespan,
    logger=logger
)

app.include_router(timetable.router)
app.include_router(subject_alias.router)
app.include_router(attendance.router)
