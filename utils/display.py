"""
utils/display.py
Console display helpers — banners, tables, and prompts for EventHub.
"""

import os

# ANSI color codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"
WHITE  = "\033[97m"
DIM    = "\033[2m"


def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    """Print the EventHub ASCII banner."""
    print(f"{CYAN}{BOLD}")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║                                                      ║")
    print("  ║    ███████╗██╗   ██╗███████╗███╗   ██╗████████╗     ║")
    print("  ║    ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝     ║")
    print("  ║    █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║        ║")
    print("  ║    ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║        ║")
    print("  ║    ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║        ║")
    print("  ║    ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝        ║")
    print("  ║                                                      ║")
    print("  ║         ██╗  ██╗██╗   ██╗██████╗                    ║")
    print("  ║         ██║  ██║██║   ██║██╔══██╗                   ║")
    print("  ║         ███████║██║   ██║██████╔╝                   ║")
    print("  ║         ██╔══██║██║   ██║██╔══██╗                   ║")
    print("  ║         ██║  ██║╚██████╔╝██████╔╝                   ║")
    print("  ║         ╚═╝  ╚═╝ ╚═════╝ ╚═════╝                    ║")
    print("  ║                                                      ║")
    print("  ║     University Event & Registration Manager          ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print(f"{RESET}")


def section(title: str):
    """Print a styled section header."""
    width = 56
    print(f"\n{CYAN}{'─' * width}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{CYAN}{'─' * width}{RESET}")


def success(msg: str):
    print(f"\n  {GREEN}✓  {msg}{RESET}")


def error(msg: str):
    print(f"\n  {RED}✗  {msg}{RESET}")


def info(msg: str):
    print(f"\n  {YELLOW}ℹ  {msg}{RESET}")


def prompt(msg: str) -> str:
    return input(f"  {BLUE}▶{RESET}  {msg}: ").strip()


def confirm(msg: str) -> bool:
    ans = input(f"  {YELLOW}?{RESET}  {msg} [y/n]: ").strip().lower()
    return ans == "y"


def print_event_card(event, index: int = None):
    """Pretty-print a single event."""
    prefix = f"  [{index}]" if index is not None else "  "
    status_color = GREEN if not event.is_full and event.is_active else RED
    status = "FULL" if event.is_full else ("INACTIVE" if not event.is_active else "OPEN")

    print(f"\n{BOLD}  {'─'*52}{RESET}")
    if index is not None:
        print(f"{BOLD}{CYAN}  [{index}] {event.title}{RESET}  {status_color}[{status}]{RESET}")
    else:
        print(f"{BOLD}{CYAN}  {event.title}{RESET}  {status_color}[{status}]{RESET}")
    print(f"      {DIM}ID: {event.event_id}  │  Category: {event.category.upper()}{RESET}")
    print(f"      📅  {event.date} at {event.time}")
    print(f"      📍  {event.location}")
    print(f"      👥  {len(event.attendees)}/{event.capacity} registered  ({event.spots_left} spots left)")
    print(f"      📝  {event.description[:80]}{'...' if len(event.description)>80 else ''}")


def print_ticket(ticket):
    """Pretty-print a ticket."""
    status_color = GREEN if ticket.status == "active" else RED
    print(f"\n  {BOLD}Ticket ID:{RESET}  {ticket.ticket_id[:8].upper()}")
    print(f"  {BOLD}Event:    {RESET}  {ticket.event_title}")
    print(f"  {BOLD}Booked:   {RESET}  {ticket.booked_at}")
    print(f"  {BOLD}Status:   {RESET}  {status_color}{ticket.status.upper()}{RESET}")


def paginate(items: list, page_size: int = 5):
    """Yield pages of items for console pagination."""
    for i in range(0, len(items), page_size):
        yield items[i : i + page_size]
