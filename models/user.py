"""
models/user.py
User and Admin model classes for EventHub.
"""

import uuid
from datetime import datetime


class User:
    """Base class representing a student user."""

    def __init__(self, username: str, password: str, full_name: str, user_id: str = None):
        self.user_id = user_id or str(uuid.uuid4())[:8]
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = "student"
        self.registered_events: list = []   # list of event_ids
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "full_name": self.full_name,
            "role": self.role,
            "registered_events": self.registered_events,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(
            username=data["username"],
            password=data["password"],
            full_name=data["full_name"],
            user_id=data["user_id"],
        )
        user.role = data.get("role", "student")
        user.registered_events = data.get("registered_events", [])
        user.created_at = data.get("created_at", "")
        return user

    def __repr__(self):
        return f"User(id={self.user_id}, username={self.username}, role={self.role})"


class Admin(User):
    """Admin user with elevated permissions, inherits from User."""

    def __init__(self, username: str, password: str, full_name: str, user_id: str = None):
        super().__init__(username, password, full_name, user_id)
        self.role = "admin"
        self.events_created: list = []   # list of event_ids created by this admin

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["events_created"] = self.events_created
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Admin":
        admin = cls(
            username=data["username"],
            password=data["password"],
            full_name=data["full_name"],
            user_id=data["user_id"],
        )
        admin.registered_events = data.get("registered_events", [])
        admin.events_created = data.get("events_created", [])
        admin.created_at = data.get("created_at", "")
        return admin

    def __repr__(self):
        return f"Admin(id={self.user_id}, username={self.username})"
