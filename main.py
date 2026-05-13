import os
import json
import uuid
import time
from datetime import datetime
from functools import wraps

# --- DECORATORS  ---

def time_logger(func):
    """Tracks system performance for file operations and heavy logic."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n[LOG] {func.__name__} executed in {end_time - start_time:.4f}s")
        return result
    return wrapper

def admin_required(func):
    """Restricts access to administrative methods."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'current_user') and self.current_user.get('role') == 'admin':
            return func(self, *args, **kwargs)
        print("\n[ERROR] Access Denied: Administrator privileges required.")
        return None
    return wrapper

# --- CORE CLASSES [cite: 23] ---

class EventHub:
    def __init__(self):
        self.events_file = "events.json"
        self.users_file = "users.json"
        self.events = self.load_data(self.events_file) 
        self.current_user = None

    @time_logger
    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return {}

    def clear_screen(self):
        """Improves UI by clearing the console[cite: 24]."""
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- ADVANCED LOGIC (Week 4 Focus)  ---

    def validate_date(self, date_str):
        """Uses datetime to ensure event dates are valid and in the future[cite: 24, 16]."""
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            if event_date < datetime.now():
                print("[ERROR] Cannot schedule events in the past.")
                return None
            return event_date.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            print("[ERROR] Invalid format. Use YYYY-MM-DD HH:MM")
            return None

    @admin_required
    def create_event(self):
        """Admin tool to add new events[cite: 13]."""
        self.clear_screen()
        print("--- Create New Event ---")
        name = input("Event Name: ")
        date_str = input("Date/Time (YYYY-MM-DD HH:MM): ")
        
        valid_date = self.validate_date(date_str)
        if not valid_date: return

        capacity = int(input("Max Capacity: "))
        event_id = str(uuid.uuid4())[:8] 
        
        self.events[event_id] = {
            "name": name,
            "date": valid_date,
            "capacity": capacity,
            "attendees": []
        }
        print(f"\n[SUCCESS] Event '{name}' created with ID: {event_id}")

    # --- INTERACTIVE MENUS  ---

    def student_menu(self):
        while True:
            self.clear_screen()
            print(f"--- Student Portal | Welcome, {self.current_user['name']} ---")
            print("1. Browse Events")
            print("2. Book a Ticket")
            print("3. Cancel Reservation")
            print("4. Logout")
            
            choice = input("\nSelect an option: ")
            
            if choice == '1':
                self.view_events()
            elif choice == '2':
                self.book_event() 
            elif choice == '4':
                break
            input("\nPress Enter to continue...")

    def admin_menu(self):
        while True:
            self.clear_screen()
            print(f"--- Admin Dashboard | System Control ---")
            print("1. View All Events")
            print("2. Create New Event")
            print("3. Delete Event")
            print("4. Logout")
            
            choice = input("\nSelect an option: ")
            
            if choice == '1':
                self.view_events()
            elif choice == '2':
                self.create_event() 
            elif choice == '4':
                break
            input("\nPress Enter to continue...")

    def view_events(self):
        """Displays formatted event list[cite: 9, 32]."""
        print(f"\n{'ID':<10} {'Event Name':<20} {'Date':<20} {'Capacity'}")
        print("-" * 60)
        for eid, details in self.events.items():
            spots = f"{len(details['attendees'])}/{details['capacity']}"
            print(f"{eid:<10} {details['name']:<20} {details['date']:<20} {spots}")

# --- MAIN EXECUTION LOOP ---
if __name__ == "__main__":
    hub = EventHub()
    # Mock login for Week 4 testing [cite: 12]
    print("Welcome to EventHub")
    role_check = input("Login as (1) Student or (2) Admin: ")
    
    if role_check == '2':
        hub.current_user = {"name": "Admin_User", "role": "admin"}
        hub.admin_menu()
    else:
        hub.current_user = {"name": "Student_User", "role": "student"}
        hub.student_menu()