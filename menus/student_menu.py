"""
menus/student_menu.py
Student-facing menu: browse events, register, cancel, view tickets.
"""

from utils.display import (
    clear, section, success, error, info, prompt, confirm,
    print_event_card, print_ticket, CYAN, BOLD, RESET, YELLOW, GREEN
)


def student_menu(manager, user):
    """Main loop for student users."""
    while True:
        clear()
        _student_header(user)
        print("  [1]  Browse Available Events")
        print("  [2]  Register for an Event")
        print("  [3]  My Registrations")
        print("  [4]  Cancel a Registration")
        print("  [5]  My Tickets")
        print("  [6]  Search Events")
        print("  [0]  Logout\n")

        choice = prompt("Select option")

        if choice == "1":
            _browse_events(manager)
        elif choice == "2":
            _register_for_event(manager, user)
        elif choice == "3":
            _my_registrations(manager, user)
        elif choice == "4":
            _cancel_registration(manager, user)
        elif choice == "5":
            _my_tickets(manager, user)
        elif choice == "6":
            _search_events(manager)
        elif choice == "0":
            break
        else:
            error("Invalid option.")
            input("\n  Press Enter to continue...")


# ── helpers ───────────────────────────────────────────────────────────────────

def _student_header(user):
    print(f"\n{CYAN}{'═'*56}{RESET}")
    print(f"{BOLD}{CYAN}   🎓  EventHub  │  Student Portal{RESET}")
    print(f"{CYAN}{'─'*56}{RESET}")
    print(f"   Logged in as: {BOLD}{user.full_name}{RESET}  ({user.username})")
    print(f"{CYAN}{'═'*56}{RESET}\n")


def _browse_events(manager):
    section("AVAILABLE EVENTS")
    events = manager.get_available_events()
    if not events:
        info("No upcoming events available at the moment.")
        input("\n  Press Enter to continue...")
        return

    for i, event in enumerate(events, 1):
        print_event_card(event, index=i)

    print()
    input("  Press Enter to go back...")


def _register_for_event(manager, user):
    section("REGISTER FOR AN EVENT")
    events = manager.get_available_events()
    if not events:
        info("No upcoming events available.")
        input("\n  Press Enter to continue...")
        return

    for i, event in enumerate(events, 1):
        print_event_card(event, index=i)

    print()
    choice = prompt("Enter event number to register (or 0 to cancel)")
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
    print_event_card(selected)

    if not confirm(f"\n  Confirm registration for '{selected.title}'?"):
        info("Registration cancelled.")
        input("\n  Press Enter to continue...")
        return

    ticket = manager.register_for_event(user, selected.event_id)
    if ticket:
        success(f"Registered successfully! 🎉")
        print(f"\n  {BOLD}Your Ticket:{RESET}")
        print_ticket(ticket)
    else:
        error(manager.last_error or "Registration failed.")

    input("\n  Press Enter to continue...")


def _my_registrations(manager, user):
    section("MY REGISTERED EVENTS")
    events = manager.get_my_active_events(user)
    if not events:
        info("You have no active registrations.")
        input("\n  Press Enter to continue...")
        return
    for i, event in enumerate(events, 1):
        print_event_card(event, index=i)
    print()
    input("  Press Enter to go back...")


def _cancel_registration(manager, user):
    section("CANCEL A REGISTRATION")
    events = manager.get_my_active_events(user)
    if not events:
        info("You have no active registrations to cancel.")
        input("\n  Press Enter to continue...")
        return

    for i, event in enumerate(events, 1):
        print_event_card(event, index=i)

    print()
    choice = prompt("Enter event number to cancel (or 0 to go back)")
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
    if not confirm(f"Cancel your registration for '{selected.title}'?"):
        info("Action cancelled.")
        input("\n  Press Enter to continue...")
        return

    ok = manager.cancel_registration(user, selected.event_id)
    if ok:
        success("Registration cancelled successfully.")
    else:
        error("Could not cancel registration.")

    input("\n  Press Enter to continue...")


def _my_tickets(manager, user):
    section("MY TICKETS")
    tickets = manager.get_my_tickets(user)
    if not tickets:
        info("You have no tickets yet.")
        input("\n  Press Enter to continue...")
        return

    for ticket in tickets:
        print_ticket(ticket)
        print()

    input("  Press Enter to go back...")


def _search_events(manager):
    section("SEARCH EVENTS")
    query = prompt("Enter search term (title, category, or location)")
    if not query:
        return

    results = manager.search_events(query)
    if not results:
        info(f"No events found matching '{query}'.")
    else:
        print(f"\n  Found {len(results)} result(s):\n")
        for i, event in enumerate(results, 1):
            print_event_card(event, index=i)

    print()
    input("  Press Enter to go back...")
