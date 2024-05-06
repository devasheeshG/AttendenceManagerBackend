import requests
import time
import json
from utils.data_models import NotificationModel
from typing import List

URL_NOTIFY = "http://192.168.0.252:8123/api/webhook/attendence_manager_notification"
URL_GET_NOTIFICATIONS = 'http://127.0.0.1:8000/notifications/unread'

while True:
    notifications: List[NotificationModel] = requests.post(URL_GET_NOTIFICATIONS, data={'username': 'dm0359'}).json()

    for data in notifications:
        
        output_string = f"You have been marked {data['type']} in {data['subject']} for {data['num_lectures']} lectures. Your attendance has changed from {data['previous_attendance_percentage']}% on {data['previous_date']} at {data['previous_time']} to {data['current_attendance_percentage']}% on {data['current_date']} at {data['current_time']}"
        
        payload = json.dumps({
            "message": output_string
        })
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        
        requests.request("POST", URL_NOTIFY, headers=headers, data=payload)
        
        print(data)
        
        time.sleep(2)
        
    time.sleep(5)