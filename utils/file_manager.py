"""
utils/file_manager.py
Handles all JSON serialization / deserialization for EventHub.
Saves and loads users, events, and tickets to/from the data/ folder.
"""

import json
import os
from typing import Dict, List

from models.user import User, Admin
from models.event import Event
from models.ticket import Ticket
from utils.decorators import time_logger

# ── file paths ────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
TICKETS_FILE = os.path.join(DATA_DIR, "tickets.json")


def _ensure_data_dir():
    """Make sure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


# ── generic helpers ───────────────────────────────────────────────────────────

def _read_json(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write_json(filepath: str, data: list):
    _ensure_data_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ── Users ─────────────────────────────────────────────────────────────────────

@time_logger
def load_users() -> Dict[str, object]:
    """Load all users from users.json; returns {username: User/Admin}."""
    records = _read_json(USERS_FILE)
    users = {}
    for rec in records:
        if rec.get("role") == "admin":
            obj = Admin.from_dict(rec)
        else:
            obj = User.from_dict(rec)
        users[obj.username] = obj
    return users


def save_users(users: Dict[str, object]):
    """Persist all users to users.json."""
    _write_json(USERS_FILE, [u.to_dict() for u in users.values()])


# ── Events ────────────────────────────────────────────────────────────────────

@time_logger
def load_events() -> Dict[str, Event]:
    """Load all events from events.json; returns {event_id: Event}."""
    records = _read_json(EVENTS_FILE)
    return {rec["event_id"]: Event.from_dict(rec) for rec in records}


def save_events(events: Dict[str, Event]):
    """Persist all events to events.json."""
    _write_json(EVENTS_FILE, [e.to_dict() for e in events.values()])


# ── Tickets ───────────────────────────────────────────────────────────────────

@time_logger
def load_tickets() -> List[Ticket]:
    """Load all tickets from tickets.json."""
    records = _read_json(TICKETS_FILE)
    return [Ticket.from_dict(rec) for rec in records]


def save_tickets(tickets: List[Ticket]):
    """Persist all tickets to tickets.json."""
    _write_json(TICKETS_FILE, [t.to_dict() for t in tickets])


# ── seed default data ─────────────────────────────────────────────────────────

def seed_defaults():
    """
    If no data files exist yet, create a default admin account
    and a couple of sample events so the app is usable out of the box.
    """
    _ensure_data_dir()

    # seed admin
    if not os.path.exists(USERS_FILE):
        default_admin = Admin(
            username="admin",
            password="admin123",
            full_name="System Administrator",
        )
        save_users({default_admin.username: default_admin})
        print("  [✓] Default admin created  →  username: admin | password: admin123")

    # seed events
    if not os.path.exists(EVENTS_FILE):
        from models.event import Event
        sample_events = [
            Event(
                title="Python Workshop",
                description="Hands-on intro to Python data structures and OOP.",
                date="2026-06-15",
                time="10:00",
                location="Room 301, CS Building",
                capacity=30,
                category="workshop",
                created_by="admin",
            ),
            Event(
                title="University Hackathon 2026",
                description="48-hour coding competition. Form teams and build something amazing!",
                date="2026-07-01",
                time="09:00",
                location="Main Auditorium",
                capacity=100,
                category="hackathon",
                created_by="admin",
            ),
            Event(
                title="AI & Machine Learning Seminar",
                description="Guest lecture by Dr. Akhmetov on modern ML applications.",
                date="2026-06-20",
                time="14:00",
                location="Lecture Hall B",
                capacity=50,
                category="seminar",
                created_by="admin",
            ),
        ]
        save_events({e.event_id: e for e in sample_events})
        print("  [✓] Sample events seeded.")
