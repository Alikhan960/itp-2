import uuid
from datetime import datetime

class Event:
    """Class representing a university event."""
    def __init__(self, title, description, date_str, capacity):
        # Using uuid to generate a unique ID for each event
        self.event_id = str(uuid.uuid4())[:8] 
        self.title = title
        self.description = description
        self.date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        self.capacity = capacity
        # Set to quickly verify unique user IDs and prevent duplicate registrations
        self.attendees = set() 

    def is_full(self):
        return len(self.attendees) >= self.capacity

    def __str__(self):
        return f"[{self.event_id}] {self.title} on {self.date.strftime('%b %d, %Y %H:%M')} (Capacity: {len(self.attendees)}/{self.capacity})"


class User:
    """Base class for all system users (Students)."""
    def __init__(self, name, email):
        self.user_id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.role = "Student"
        # List to track the chronological order of user's registered events
        self.registered_events = [] 

    def __str__(self):
        return f"{self.name} ({self.role}) - ID: {self.user_id}"


class Admin(User):
    """Admin class inheriting from User with elevated privileges."""
    def __init__(self, name, email):
        super().__init__(name, email)
        self.role = "Admin"

    # Placeholder for Week 3 logic
    def create_event(self, system_events_dict, title, description, date_str, capacity):
        new_event = Event(title, description, date_str, capacity)
        system_events_dict[new_event.event_id] = new_event
        print(f"Admin {self.name} created event: {title}")
        return new_event


class EventManager:
    """Main system class holding the core data structures."""
    def __init__(self):
        # Dictionaries map IDs to their respective objects for fast lookup
        self.users = {}  
        self.events = {} 

    def add_user(self, user):
        self.users[user.user_id] = user
        print(f"Added to system: {user}")


# WEEK 1 TEST RUN

if __name__ == "__main__":
    print("Initializing EventHub System...")
    app = EventManager()

    # 1. Create users
    student1 = User("Alikhan Yertaiuly", "alikhan@example.com")
    admin1 = Admin("Super Admin", "admin@example.com")

    # Add to system dictionary
    app.add_user(student1)
    app.add_user(admin1)

    # 2. Admin creates an event
    print("\nCreating Events...")
    event1 = admin1.create_event(
        system_events_dict=app.events,
        title="Intro to Python Hackathon",
        description="A competitive coding event for first-year students.",
        date_str="2026-05-15 14:00",
        capacity=50
    )

    # 3. Display current system state
    print("\n--- System Status ---")
    print("Total Users Registered:", len(app.users))
    print("Total Events Available:", len(app.events))
    
    for e_id, event_obj in app.events.items():
        print(event_obj)