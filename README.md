# 🎓 EventHub — University Event & Registration Manager

**Author:** Alikhan Yertaiuly  
**Group:** SE-2504  
**Course:** Python Programming  

---

## 📋 Project Overview

EventHub is a Python-based console application that streamlines the management of university campus events. It supports two types of users:

- **Students** — browse events, register, cancel registrations, and view tickets.
- **Administrators** — create, edit, delete events; view attendee lists; monitor statistics.

All data is persisted locally using JSON files, so nothing is lost between sessions.

---

## 🗂 Project Structure

```
EventHub/
├── main.py                  # Application entry point
├── event_manager.py         # Core business logic class
├── README.md
│
├── models/                  # OOP data models
│   ├── __init__.py
│   ├── user.py              # User and Admin classes
│   ├── event.py             # Event class
│   └── ticket.py            # Ticket class
│
├── menus/                   # Console UI menus
│   ├── __init__.py
│   ├── auth_menu.py         # Login & registration screen
│   ├── student_menu.py      # Student interface
│   └── admin_menu.py        # Admin interface
│
├── utils/                   # Utilities & helpers
│   ├── __init__.py
│   ├── decorators.py        # @admin_required, @time_logger, @validate_input
│   ├── file_manager.py      # JSON I/O (load/save users, events, tickets)
│   ├── display.py           # Console formatting helpers
│   └── validators.py        # Input validation functions
│
└── data/                    # Auto-generated JSON storage
    ├── users.json
    ├── events.json
    └── tickets.json
```

---

## 🚀 How to Run

**Requirements:** Python 3.8+  
No external libraries needed — only the Python standard library.

```bash
cd EventHub
python main.py
```

### Default Admin Credentials
| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

---

## ✨ Features

### Student
- Register a new account
- Browse all upcoming, available events
- Register for events (with validation — no double-booking, capacity checks, schedule conflict detection)
- Cancel a registration
- View personal tickets
- Search events by title, category, or location

### Admin
- Full dashboard with event statistics and category breakdown
- View all events (including past/inactive)
- Create new events with date/time/capacity validation
- Edit event details
- Soft-delete events (cancels all attendee tickets automatically)
- View attendee list per event
- List all registered users

---

## 🐍 Python Concepts Used

| Concept | Where Used |
|---|---|
| **Data Structures** | `dict` for users/events, `list` for attendees/tickets, `set` for unique username checks |
| **File I/O** | `json` module in `utils/file_manager.py` to read/write all `.json` data files |
| **OOP** | `User`, `Admin` (inherits `User`), `Event`, `Ticket`, `EventManager` classes |
| **External Modules** | `uuid`, `datetime`, `os`, `json`, `re`, `time`, `functools` |
| **Decorators** | `@admin_required`, `@time_logger`, `@validate_input` in `utils/decorators.py` |
| **Properties** | `@property` on `Event` for `spots_left`, `is_full`, `is_past`, `datetime_obj` |
| **Class Methods** | `from_dict()` classmethods on all model classes |

---

## 📊 Data Persistence

Three JSON files in `data/`:

- **users.json** — all user/admin accounts
- **events.json** — all events with attendee lists
- **tickets.json** — all booking records

Files are created automatically on first run. The app seeds a default admin account and 3 sample events if no data exists.

---

## 🔐 Validations & Safety

- **Double-booking prevention** — users cannot register for the same event twice
- **Capacity enforcement** — registration blocked when event is full
- **Schedule conflict detection** — blocks registration if user already has an event at the same date/time
- **Input validation** — dates, times, usernames, and passwords are all validated before saving
- **Admin-only restriction** — `@admin_required` decorator blocks non-admins from admin functions

---

## 📅 Development Timeline (5 Weeks)

| Week | Task |
|------|------|
| 1 | GitHub repo setup, OOP architecture (User, Admin, Event classes), basic data structures |
| 2 | File I/O system — JSON serialization/deserialization, data loading on startup |
| 3 | Core business logic — registration system, capacity checks, admin tools |
| 4 | Advanced Python — datetime, decorators, interactive console menus |
| 5 | Testing, bug fixes, refactoring, README, presentation prep |
