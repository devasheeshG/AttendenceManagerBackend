from pydantic import BaseModel
from datetime import date, time

# class AttendanceRecord(BaseModel):
#     username: str
#     subject: str
#     max_hours: int
#     attended_hours: int
#     absent_hours: int
#     total_percentage: float
#     date: date
#     time: time

# def attendance_record(
#     username,
#     subject,
#     max_hours,
#     attended_hours,
#     absent_hours,
#     total_percentage,
#     date,
#     time,
# ):
#     return AttendanceRecord(
#         username=username,
#         subject=subject,
#         max_hours=max_hours,
#         attended_hours=attended_hours,
#         absent_hours=absent_hours,
#         total_percentage=total_percentage,
#         date=date,
#         time=time,
#     )

# class NotificationModel(BaseModel):
#     username: str
#     subject: str
#     type: str
#     num_lectures: int
#     previous_attendance_percentage: float
#     current_attendance_percentage: float
#     previous_date: str
#     previous_time: str
#     current_date: str
#     current_time: str
