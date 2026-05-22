"""
models/event.py
Event model class for EventHub.
"""

import uuid
from datetime import datetime


class Event:
    """Represents a university campus event."""

    CATEGORIES = {"lecture", "hackathon", "club", "seminar", "workshop", "other"}

    def __init__(
        self,
        title: str,
        description: str,
        date: str,
        time: str,
        location: str,
        capacity: int,
        category: str,
        created_by: str,
        event_id: str = None,
    ):
        self.event_id = event_id or str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.date = date          # "YYYY-MM-DD"
        self.time = time          # "HH:MM"
        self.location = location
        self.capacity = int(capacity)
        self.category = category.lower() if category.lower() in self.CATEGORIES else "other"
        self.created_by = created_by   # admin username
        self.attendees: list = []      # list of user_ids
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = True

    # ── computed properties ──────────────────────────────────────────────────

    @property
    def spots_left(self) -> int:
        return self.capacity - len(self.attendees)

    @property
    def is_full(self) -> bool:
        return self.spots_left <= 0

    @property
    def datetime_obj(self) -> datetime:
        try:
            return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.min

    @property
    def is_past(self) -> bool:
        return self.datetime_obj < datetime.now()

    # ── serialization ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "capacity": self.capacity,
            "category": self.category,
            "created_by": self.created_by,
            "attendees": self.attendees,
            "created_at": self.created_at,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        event = cls(
            title=data["title"],
            description=data["description"],
            date=data["date"],
            time=data["time"],
            location=data["location"],
            capacity=data["capacity"],
            category=data["category"],
            created_by=data["created_by"],
            event_id=data["event_id"],
        )
        event.attendees = data.get("attendees", [])
        event.created_at = data.get("created_at", "")
        event.is_active = data.get("is_active", True)
        return event

    def __repr__(self):
        return (
            f"Event(id={self.event_id}, title={self.title!r}, "
            f"date={self.date}, spots_left={self.spots_left})"
        )
