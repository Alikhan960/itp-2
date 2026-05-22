"""
menus/admin_menu.py
Admin-facing menu: create/edit/delete events, view attendees, dashboard.
"""

from utils.display import (
    clear, section, success, error, info, prompt, confirm,
    print_event_card, CYAN, BOLD, RESET, GREEN, YELLOW, RED, MAGENTA
)
from utils.validators import validate_date, validate_time, validate_capacity
from models.event import Event


def admin_menu(manager, admin):
    """Main loop for admin users."""
    while True:
        clear()
        _admin_header(admin)
        print("  [1]  Dashboard / Stats")
        print("  [2]  View All Events")
        print("  [3]  Create New Event")
        print("  [4]  Edit an Event")
        print("  [5]  Delete an Event")
        print("  [6]  View Event Attendees")
        print("  [7]  List All Users")
        print("  [0]  Logout\n")

        choice = prompt("Select option")

        if choice == "1":
            _dashboard(manager)
        elif choice == "2":
            _view_all_events(manager)
        elif choice == "3":
            _create_event(manager, admin)
        elif choice == "4":
            _edit_event(manager, admin)
        elif choice == "5":
            _delete_event(manager, admin)
        elif choice == "6":
            _view_attendees(manager, admin)
        elif choice == "7":
            _list_users(manager)
        elif choice == "0":
            break
        else:
            error("Invalid option.")
            input("\n  Press Enter to continue...")


# ── helpers ───────────────────────────────────────────────────────────────────

def _admin_header(admin):
    print(f"\n{MAGENTA}{'═'*56}{RESET}")
    print(f"{BOLD}{MAGENTA}   🔑  EventHub  │  Admin Panel{RESET}")
    print(f"{MAGENTA}{'─'*56}{RESET}")
    print(f"   Logged in as: {BOLD}{admin.full_name}{RESET}  ({admin.username})")
    print(f"{MAGENTA}{'═'*56}{RESET}\n")


def _dashboard(manager):
    section("DASHBOARD & STATISTICS")
    stats = manager.get_event_stats()
    print(f"\n  {BOLD}{'─'*40}{RESET}")
    print(f"  Total Events       :  {BOLD}{stats['total_events']}{RESET}")
    print(f"  Active Events      :  {GREEN}{stats['active_events']}{RESET}")
    print(f"  Total Users        :  {BOLD}{stats['total_users']}{RESET}")
    print(f"  Total Registrations:  {BOLD}{stats['total_registrations']}{RESET}")
    print(f"\n  {BOLD}Events by Category:{RESET}")
    for cat, count in stats["categories"].items():
        bar = "█" * count
        print(f"    {cat.upper():<12}  {bar} ({count})")
    print(f"\n  {BOLD}{'─'*40}{RESET}")
    input("\n  Press Enter to go back...")


def _view_all_events(manager):
    section("ALL EVENTS")
    events = manager.get_all_events()
    if not events:
        info("No events found.")
        input("\n  Press Enter to continue...")
        return
    for i, event in enumerate(events, 1):
        print_event_card(event, index=i)
    print()
    input("  Press Enter to go back...")


def _create_event(manager, admin):
    section("CREATE NEW EVENT")

    title = prompt("Event title")
    if not title:
        error("Title cannot be empty.")
        input("\n  Press Enter to continue...")
        return

    description = prompt("Description")

    date = prompt("Date (YYYY-MM-DD)")
    if not validate_date(date):
        error("Invalid date. Use YYYY-MM-DD format and ensure it's in the future.")
        input("\n  Press Enter to continue...")
        return

    time = prompt("Time (HH:MM, 24h format)")
    if not validate_time(time):
        error("Invalid time. Use HH:MM format.")
        input("\n  Press Enter to continue...")
        return

    location = prompt("Location")
    if not location:
        error("Location cannot be empty.")
        input("\n  Press Enter to continue...")
        return

    cap_str = prompt("Capacity (max number of attendees)")
    if not validate_capacity(cap_str):
        error("Capacity must be a positive number.")
        input("\n  Press Enter to continue...")
        return

    print(f"\n  Categories: {', '.join(Event.CATEGORIES)}")
    category = prompt("Category")

    print(f"\n  {BOLD}Preview:{RESET}")
    print(f"  Title      : {title}")
    print(f"  Date/Time  : {date} at {time}")
    print(f"  Location   : {location}")
    print(f"  Capacity   : {cap_str}")
    print(f"  Category   : {category}")

    if not confirm("\n  Create this event?"):
        info("Event creation cancelled.")
        input("\n  Press Enter to continue...")
        return

    event = manager.create_event(
        current_user=admin,
        title=title,
        description=description,
        date=date,
        time=time,
        location=location,
        capacity=int(cap_str),
        category=category,
    )

    if event:
        success(f"Event '{event.title}' created! ID: {event.event_id}")
    else:
        error("Failed to create event.")

    input("\n  Press Enter to continue...")


def _edit_event(manager, admin):
    section("EDIT AN EVENT")
    events = manager.get_all_events()
    if not events:
        info("No events to edit.")
        input("\n  Press Enter to continue...")
        return

    for i, event in enumerate(events, 1):
        print_event_card(event, index=i)

    print()
    choice = prompt("Enter event number to edit (or 0 to cancel)")
    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(events):
            raise ValueError
    except ValueError:
        error("Invalid selection.")
        input("\n  Press Enter to continue...")
        return

    selected = events[idx]
    print(f"\n  Editing: {BOLD}{selected.title}{RESET}")
    info("Leave blank to keep current value.")

    new_title       = prompt(f"Title [{selected.title}]")
    new_description = prompt(f"Description [{selected.description[:40]}...]")
    new_date        = prompt(f"Date [{selected.date}]")
    new_time        = prompt(f"Time [{selected.time}]")
    new_location    = prompt(f"Location [{selected.location}]")
    new_capacity    = prompt(f"Capacity [{selected.capacity}]")

    if new_date and not validate_date(new_date):
        error("Invalid date format.")
        input("\n  Press Enter to continue...")
        return
    if new_time and not validate_time(new_time):
        error("Invalid time format.")
        input("\n  Press Enter to continue...")
        return
    if new_capacity and not validate_capacity(new_capacity):
        error("Capacity must be a positive number.")
        input("\n  Press Enter to continue...")
        return

    updated = manager.edit_event(
        admin,
        selected.event_id,
        title=new_title,
        description=new_description,
        date=new_date,
        time=new_time,
        location=new_location,
        capacity=new_capacity,
    )

    if updated:
        success(f"Event '{updated.title}' updated successfully.")
    else:
        error("Update failed.")

    input("\n  Press Enter to continue...")


def _delete_event(manager, admin):
    section("DELETE AN EVENT")
    events = manager.get_all_events()
    active_events = [e for e in events if e.is_active]

    if not active_events:
        info("No active events to delete.")
        input("\n  Press Enter to continue...")
        return

    for i, event in enumerate(active_events, 1):
        print_event_card(event, index=i)

    print()
    choice = prompt("Enter event number to delete (or 0 to cancel)")
    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(active_events):
            raise ValueError
    except ValueError:
        error("Invalid selection.")
        input("\n  Press Enter to continue...")
        return

    selected = active_events[idx]

    print(f"\n  {RED}WARNING: This will deactivate '{selected.title}' and cancel all registrations!{RESET}")
    if not confirm("Are you sure you want to delete this event?"):
        info("Deletion cancelled.")
        input("\n  Press Enter to continue...")
        return

    ok = manager.delete_event(admin, selected.event_id)
    if ok:
        success(f"Event '{selected.title}' deleted and all tickets cancelled.")
    else:
        error("Deletion failed.")

    input("\n  Press Enter to continue...")


def _view_attendees(manager, admin):
    section("VIEW EVENT ATTENDEES")
    events = manager.get_all_events()
    if not events:
        info("No events found.")
        input("\n  Press Enter to continue...")
        return

    for i, event in enumerate(events, 1):
        print(f"  [{i}]  {event.title}  ({len(event.attendees)} registered)")

    print()
    choice = prompt("Enter event number (or 0 to cancel)")
    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(events):
            raise ValueError
    except ValueError:
        error("Invalid selection.")
        input("\n  Press Enter to continue...")
        return

    selected = events[idx]
    attendees = manager.get_attendee_list(admin, selected.event_id)

    section(f"ATTENDEES — {selected.title}")
    if not attendees:
        info("No attendees registered yet.")
    else:
        print(f"\n  {'#':<4} {'User ID':<12} {'Username':<20} {'Full Name'}")
        print(f"  {'─'*60}")
        for i, att in enumerate(attendees, 1):
            print(f"  {i:<4} {att['user_id']:<12} {att['username']:<20} {att['full_name']}")

    print()
    input("  Press Enter to go back...")


def _list_users(manager):
    section("ALL USERS")
    users = list(manager.users.values())
    if not users:
        info("No users found.")
        input("\n  Press Enter to continue...")
        return

    print(f"\n  {'#':<4} {'ID':<10} {'Username':<20} {'Full Name':<25} {'Role':<8} {'Events'}")
    print(f"  {'─'*75}")
    for i, user in enumerate(users, 1):
        role_color = MAGENTA if user.role == "admin" else CYAN
        print(
            f"  {i:<4} {user.user_id:<10} {user.username:<20} "
            f"{user.full_name:<25} {role_color}{user.role:<8}{RESET} "
            f"{len(user.registered_events)}"
        )

    print()
    input("  Press Enter to go back...")
