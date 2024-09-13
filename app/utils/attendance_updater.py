from app.utils.attendance_manager import AttendanceManager
from app.utils.email_sender import send_email
from app.utils.models import User
from app.utils.models import Attendance
from app.utils.database import get_db
from sqlalchemy.orm import Session

async def update_attendance_and_notify():
    db = next(get_db())
    am = AttendanceManager()
    await am.login()

    users = db.query(User).all()
    for user in users:
        old_attendance = db.query(Attendance).filter(Attendance.username == user.username).all()
        new_attendance, _ = await am.get_attendance_details()

        old_attendance_dict = {att.subject_code: att.percentage for att in old_attendance}
        changes = []
        for new_subject in new_attendance:
            if new_subject['Code'] in old_attendance_dict:
                old_percentage = old_attendance_dict[new_subject['Code']]
                new_percentage = float(new_subject['Percentage'])
                if new_percentage < old_percentage:
                    changes.append({
                        'subject': new_subject['Course Title'],
                        'old_percentage': old_percentage,
                        'new_percentage': new_percentage
                    })

        if changes:
            message = "Attendance Update:\n\n"
            for change in changes:
                message += f"Subject: {change['subject']}\n"
                message += f"Old Percentage: {change['old_percentage']}%\n"
                message += f"New Percentage: {change['new_percentage']}%\n\n"

            send_email(user.email, "Attendance Update", message)

        # Update the database with new attendance
        for subject in new_attendance:
            db_subject = db.query(Attendance).filter(Attendance.username == user.username, Attendance.subject_code == subject['Code']).first()
            if db_subject:
                db_subject.percentage = float(subject['Percentage'])
            else:
                new_subject = Attendance(username=user.username, subject_code=subject['Code'], percentage=float(subject['Percentage']))
                db.add(new_subject)

    db.commit()
    await am.close()