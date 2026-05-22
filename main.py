"""
main.py
EventHub — University Event & Registration Manager
Entry point: initializes the system, seeds defaults, and starts the UI.

Author : Alikhan Yertaiuly
Group  : SE-2504
"""

import sys
import os

# E  path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from event_manager import EventManager
from utils.file_manager import seed_defaults
from utils.display import clear, banner, success, info, CYAN, RESET, BOLD
from menus.auth_menu import auth_menu
from menus.student_menu import student_menu
from menus.admin_menu import admin_menu


def main():
    """Application bootstrap and main event loop."""
    clear()
    banner()

    # initialise 
    print(f"  {CYAN}Initializing EventHub...{RESET}\n")
    seed_defaults()

    manager = EventManager()
    manager.load_all()

    success("System ready!")
    input("\n  Press Enter to continue to login...")

    #main loop 
    while True:
        current_user = auth_menu(manager)

        if current_user is None:
            # user chose to exit
            clear()
            print(f"\n{BOLD}{CYAN}  Thank you for using EventHub. Goodbye! 👋{RESET}\n")
            break

        # route
        if current_user.role == "admin":
            admin_menu(manager, current_user)
        else:
            student_menu(manager, current_user)

        # save everything on logout, just in case
        manager.save_all()
        info("Session ended. Returning to login screen...")
        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()