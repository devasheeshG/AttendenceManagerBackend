from utils.notifications import Notifications, NotificationModel
import random
notifications = Notifications()

test_data = {
    'username': 'dm0359',
    'subject': f'DATABASE MANAGEMENT SYSTEM_test_{random.randint(0, 1000)}',
    'type': 'present',
    'num_lectures': 1,
    'previous_attendance_percentage': 71.88,
    'current_attendance_percentage': 73.13,
    'previous_date': '21-04-2024',
    'previous_time': '19:56:10',
    'current_date': '24-04-2024',
    'current_time': '18:07:08'
}

notifications.push_notification(NotificationModel(**test_data))

print('Done')