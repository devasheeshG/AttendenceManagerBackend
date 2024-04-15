"""Generates notifications for given user."""

import os
from utils.data_models import NotificationModel
from pymongo import MongoClient
import dotenv

dotenv.load_dotenv(".env")


class Notifications:
    def __init__(self):
        self.client = MongoClient(
            f"mongodb://{os.getenv('MONGO_DB_USER')}:{os.getenv('MONGO_DB_PASSWORD')}@{os.getenv('MONGO_DB_HOST')}:{os.getenv('MONGO_DB_PORT')}"
        )
        self.db = self.client[os.getenv("MONGO_DB_NAME")]
        self.unread_notifications = self.db["unread_notifications"]
        self.read_notifications = self.db["read_notifications"]

    def __del__(self):
        self.client.close()

    def push_notification(self, notification: NotificationModel):
        if not (
            self.read_notifications.find_one(notification.model_dump())
            or self.unread_notifications.find_one(notification.model_dump())
        ):
            self.unread_notifications.insert_one(notification.model_dump())

    def retrieve_unread_notifications(self, username: str) -> list:
        """Retrieve unread notifications for given user and mark them as read."""
        notifications = list(self.unread_notifications.find({"username": username}))
        if not notifications:
            return []
        self.unread_notifications.delete_many(
            {"_id": {"$in": [notification["_id"] for notification in notifications]}}
        )
        self.read_notifications.insert_many(notifications)
        return [
            {
                key: notification[key]
                for key in notification
                if key not in ["_id", "username"]
            }
            for notification in notifications
        ]

    def retrieve_all_notifications(self, username: str) -> list:
        """Retrieve all notifications for given user."""
        unread_notifications = list(
            self.unread_notifications.find({"username": username})
        )
        read_notifications = list(self.read_notifications.find({"username": username}))
        return [
            {
                key: notification[key]
                for key in notification
                if key not in ["_id", "username"]
            }
            for notification in unread_notifications + read_notifications
            if notification
        ]


if __name__ == "__main__":
    notifications = Notifications()
    print(notifications.retrieve_unread_notifications("dp4310"))
    del notifications
