"""This script updates the `attendence` database for a user to latest data."""

from typing import Type
import os
import sys
import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
import dotenv

dotenv.load_dotenv(".env")

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import check_if_user_exists
from utils.attendance_manager import AttendanceManager
from utils.notifications import Notifications
from utils.data_models import attendance_record, NotificationModel


async def update_attendence_database(
    username: str,
    password: str,
    attendence_manager_cls: Type[AttendanceManager],
    cursor: psycopg2.extensions.connection,
    conn: psycopg2.extensions.connection,
) -> dict:
    """Update Attendence Database."""
    # Check if User Exists
    if not check_if_user_exists(username, cursor):
        return {"status": "error", "message": f"{username}: User Not Found"}

    # Get Attendance Details
    attendence_manager = attendence_manager_cls(username, password)
    await attendence_manager.login()
    attendence, _ = await attendence_manager.get_attendance_details()

    for data in attendence:
        # Insert Attendance Data
        try:
            cursor.execute(
                """
                INSERT INTO attendence_table (
                    username, subject, max_hours, attended_hours, absent_hours, total_percentage, date, time
                ) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME)
            """,
                (
                    username,
                    data["Description"],
                    data["Max. hours"],
                    data["Att. hours"],
                    data["Absent hours"],
                    data["Total Percentage"],
                ),
            )
            conn.commit()
        except psycopg2.Error as e:
            if str(e.pgcode) != str(UNIQUE_VIOLATION):
                return {
                    "status": "error",
                    "message": f"{username}: SQL Unique Violation Error",
                }
            conn.rollback()

        # Add Absent Notifications (if any)
        try:
            notifications = Notifications()
            cursor.execute(
                """
                SELECT * 
                FROM attendence_table 
                WHERE username=%s
                AND subject=%s
                ORDER BY date DESC, time DESC
                LIMIT 2;
            """,
                (username, data["Description"]),
            )
            latest_attendence = cursor.fetchall()

            if len(latest_attendence) != 2:
                return {
                    "status": "error",
                    "message": f"{username}: Not Enough Data for Notifications",
                }
            current_attendence, previous_attendence = attendance_record(
                *latest_attendence[0]
            ), attendance_record(*latest_attendence[1])

            if current_attendence.max_hours == previous_attendence.max_hours:
                continue

            # Logic for Notifications
            max_hours_diff = (
                current_attendence.max_hours - previous_attendence.max_hours
            )
            present_hours_diff = (
                current_attendence.attended_hours - previous_attendence.attended_hours
            )
            absent_hours_diff = (
                current_attendence.absent_hours - previous_attendence.absent_hours
            )

            if present_hours_diff + absent_hours_diff != max_hours_diff:
                return {
                    "status": "error",
                    "message": f"{username}: Invalid Attendance Data",
                }

            if absent_hours_diff > 0:
                notifications.push_notification(
                    NotificationModel(
                        username=username,
                        subject=current_attendence.subject,
                        type="absent",
                        num_lectures=absent_hours_diff,
                        previous_attendance_percentage=previous_attendence.total_percentage,
                        current_attendance_percentage=current_attendence.total_percentage,
                        previous_date=str(
                            previous_attendence.date.strftime("%d-%m-%Y")
                        ),
                        previous_time=str(
                            previous_attendence.time.strftime("%H:%M:%S")
                        ),
                        current_date=str(current_attendence.date.strftime("%d-%m-%Y")),
                        current_time=str(current_attendence.time.strftime("%H:%M:%S")),
                    )
                )

            if present_hours_diff > 0:
                notifications.push_notification(
                    NotificationModel(
                        username=username,
                        subject=current_attendence.subject,
                        type="present",
                        num_lectures=present_hours_diff,
                        previous_attendance_percentage=previous_attendence.total_percentage,
                        current_attendance_percentage=current_attendence.total_percentage,
                        previous_date=str(
                            previous_attendence.date.strftime("%d-%m-%Y")
                        ),
                        previous_time=str(
                            previous_attendence.time.strftime("%H:%M:%S")
                        ),
                        current_date=str(current_attendence.date.strftime("%d-%m-%Y")),
                        current_time=str(current_attendence.time.strftime("%H:%M:%S")),
                    )
                )

        except Exception as e:
            return {
                "status": "error",
                "message": f'{username}: Error in Notifications, {e.with_traceback(None) if hasattr(e, "with_traceback") else e}',
            }

        finally:
            del notifications

    return {
        "status": "success",
        "message": f"{username}: Attendance Updated Successfully",
    }
