"""
models/ticket.py
Ticket model class for EventHub.
"""

import uuid
from datetime import datetime


class Ticket:
    """Represents a registration ticket linking a User to an Event."""

    def __init__(
        self,
        user_id: str,
        event_id: str,
        username: str,
        event_title: str,
        ticket_id: str = None,
    ):
        self.ticket_id = ticket_id or str(uuid.uuid4())
        self.user_id = user_id
        self.event_id = event_id
        self.username = username
        self.event_title = event_title
        self.booked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "active"   # active | cancelled

    def cancel(self):
        self.status = "cancelled"

    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "username": self.username,
            "event_title": self.event_title,
            "booked_at": self.booked_at,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        ticket = cls(
            user_id=data["user_id"],
            event_id=data["event_id"],
            username=data["username"],
            event_title=data["event_title"],
            ticket_id=data["ticket_id"],
        )
        ticket.booked_at = data.get("booked_at", "")
        ticket.status = data.get("status", "active")
        return ticket

    def __repr__(self):
        return (
            f"Ticket(id={self.ticket_id[:8]}, user={self.username}, "
            f"event={self.event_title!r}, status={self.status})"
        )
