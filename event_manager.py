"""
event_manager.py
EventManager — the central business-logic class for EventHub.
Handles all operations: user auth, event CRUD, registrations, tickets.
"""

from datetime import datetime
from typing import Dict, List, Optional

from models.user import User, Admin
from models.event import Event
from models.ticket import Ticket
from utils.decorators import admin_required, time_logger
from utils import file_manager as fm


class EventManager:
    """
    Central manager class.
    Holds in-memory state and delegates persistence to file_manager.
    """

    def __init__(self):
        self.users: Dict[str, User] = {}     # {username: User/Admin}
        self.events: Dict[str, Event] = {}   # {event_id: Event}
        self.tickets: List[Ticket] = []
        self._unique_usernames: set = set()  # fast duplicate check

    # ── bootstrap ─────────────────────────────────────────────────────────────

    @time_logger
    def load_all(self):
        """Load all data from disk into memory."""
        self.users = fm.load_users()
        self.events = fm.load_events()
        self.tickets = fm.load_tickets()
        self._unique_usernames = set(self.users.keys())

    def save_all(self):
        """Persist all in-memory data to disk."""
        fm.save_users(self.users)
        fm.save_events(self.events)
        fm.save_tickets(self.tickets)

    # ── authentication ────────────────────────────────────────────────────────

    def register_user(self, username: str, password: str, full_name: str) -> Optional[User]:
        """Register a new student account. Returns User on success, None on failure."""
        if username in self._unique_usernames:
            return None   # username taken
        user = User(username=username, password=password, full_name=full_name)
        self.users[username] = user
        self._unique_usernames.add(username)
        fm.save_users(self.users)
        return user

    def login(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user. Returns User/Admin object or None."""
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    # ── event management (admin) ──────────────────────────────────────────────

    @admin_required
    def create_event(
        self,
        current_user: Admin,
        title: str,
        description: str,
        date: str,
        time: str,
        location: str,
        capacity: int,
        category: str,
    ) -> Event:
        """Create a new event. Admin only."""
        event = Event(
            title=title,
            description=description,
            date=date,
            time=time,
            location=location,
            capacity=capacity,
            category=category,
            created_by=current_user.username,
        )
        self.events[event.event_id] = event
        current_user.events_created.append(event.event_id)
        fm.save_events(self.events)
        fm.save_users(self.users)
        return event

    @admin_required
    def edit_event(
        self,
        current_user: Admin,
        event_id: str,
        **kwargs,
    ) -> Optional[Event]:
        """Edit an existing event's fields. Admin only."""
        event = self.events.get(event_id)
        if not event:
            return None
        allowed = {"title", "description", "date", "time", "location", "capacity", "category"}
        for key, value in kwargs.items():
            if key in allowed and value:
                if key == "capacity":
                    value = int(value)
                setattr(event, key, value)
        fm.save_events(self.events)
        return event

    @admin_required
    def delete_event(self, current_user: Admin, event_id: str) -> bool:
        """
        Soft-delete an event (mark inactive).
        Cancels all active tickets for that event. Admin only.
        """
        event = self.events.get(event_id)
        if not event:
            return False
        event.is_active = False
        # cancel all active tickets for this event
        for ticket in self.tickets:
            if ticket.event_id == event_id and ticket.status == "active":
                ticket.cancel()
                user = self.users.get(ticket.username)
                if user and event_id in user.registered_events:
                    user.registered_events.remove(event_id)
        fm.save_events(self.events)
        fm.save_tickets(self.tickets)
        fm.save_users(self.users)
        return True

    @admin_required
    def get_attendee_list(self, current_user: Admin, event_id: str) -> List[dict]:
        """Return list of attendee info for an event. Admin only."""
        event = self.events.get(event_id)
        if not event:
            return []
        result = []
        for user_id in event.attendees:
            # find user by user_id
            for user in self.users.values():
                if user.user_id == user_id:
                    result.append({
                        "user_id": user.user_id,
                        "username": user.username,
                        "full_name": user.full_name,
                    })
                    break
        return result

    # ── registration (student) ────────────────────────────────────────────────

    def get_available_events(self) -> List[Event]:
        """Return all active, non-full, upcoming events sorted by date."""
        events = [
            e for e in self.events.values()
            if e.is_active and not e.is_past
        ]
        return sorted(events, key=lambda e: e.datetime_obj)

    def get_all_events(self) -> List[Event]:
        """Return all events sorted by date (for admin view)."""
        return sorted(self.events.values(), key=lambda e: e.datetime_obj)

    def register_for_event(self, user: User, event_id: str) -> Optional[Ticket]:
        """
        Book a ticket for a user.
        Checks: event exists, is active, not full, no double-booking,
                no schedule conflict.
        Returns Ticket on success or None on failure with a reason set.
        """
        self.last_error = ""
        event = self.events.get(event_id)

        if not event:
            self.last_error = "Event not found."
            return None
        if not event.is_active:
            self.last_error = "This event is no longer active."
            return None
        if event.is_past:
            self.last_error = "This event has already passed."
            return None
        if event.is_full:
            self.last_error = "Sorry, this event is fully booked."
            return None
        if user.user_id in event.attendees:
            self.last_error = "You are already registered for this event."
            return None
        # schedule conflict check
        if self._has_schedule_conflict(user, event):
            self.last_error = "Schedule conflict: you already have an event at that time."
            return None

        # all checks passed — book
        event.attendees.append(user.user_id)
        user.registered_events.append(event_id)
        ticket = Ticket(
            user_id=user.user_id,
            event_id=event_id,
            username=user.username,
            event_title=event.title,
        )
        self.tickets.append(ticket)
        fm.save_events(self.events)
        fm.save_users(self.users)
        fm.save_tickets(self.tickets)
        return ticket

    def cancel_registration(self, user: User, event_id: str) -> bool:
        """Cancel a user's registration for an event."""
        event = self.events.get(event_id)
        if not event:
            return False
        if user.user_id not in event.attendees:
            return False

        event.attendees.remove(user.user_id)
        if event_id in user.registered_events:
            user.registered_events.remove(event_id)

        # cancel matching ticket
        for ticket in self.tickets:
            if ticket.user_id == user.user_id and ticket.event_id == event_id and ticket.status == "active":
                ticket.cancel()
                break

        fm.save_events(self.events)
        fm.save_users(self.users)
        fm.save_tickets(self.tickets)
        return True

    def get_my_tickets(self, user: User) -> List[Ticket]:
        """Return all tickets belonging to a user."""
        return [t for t in self.tickets if t.user_id == user.user_id]

    def get_my_active_events(self, user: User) -> List[Event]:
        """Return active events the user is registered for."""
        result = []
        for eid in user.registered_events:
            event = self.events.get(eid)
            if event:
                result.append(event)
        return sorted(result, key=lambda e: e.datetime_obj)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _has_schedule_conflict(self, user: User, new_event: Event) -> bool:
        """
        Check if the user already has an event that overlaps with new_event.
        Simple check: same date and time.
        """
        for eid in user.registered_events:
            existing = self.events.get(eid)
            if existing and existing.is_active:
                if existing.date == new_event.date and existing.time == new_event.time:
                    return True
        return False

    def search_events(self, query: str) -> List[Event]:
        """Search events by title, category, or location (case-insensitive)."""
        q = query.lower()
        return [
            e for e in self.events.values()
            if q in e.title.lower() or q in e.category.lower() or q in e.location.lower()
        ]

    def get_event_stats(self) -> dict:
        """Return summary statistics for admin dashboard."""
        total = len(self.events)
        active = sum(1 for e in self.events.values() if e.is_active)
        total_registrations = sum(len(e.attendees) for e in self.events.values())
        categories: dict = {}
        for e in self.events.values():
            categories[e.category] = categories.get(e.category, 0) + 1
        return {
            "total_events": total,
            "active_events": active,
            "total_users": len(self.users),
            "total_registrations": total_registrations,
            "categories": categories,
        }
