"""
menus/auth_menu.py
Authentication menu: login and student registration.
"""

from utils.display import (
    clear, banner, section, success, error, info, prompt, confirm,
)
from utils.validators import validate_username, validate_password


def auth_menu(manager) -> object:
    """
    Display the main auth screen.
    Returns the logged-in user object, or None to exit.
    """
    while True:
        clear()
        banner()
        print("  [1]  Login")
        print("  [2]  Register as Student")
        print("  [0]  Exit\n")

        choice = prompt("Select option")

        if choice == "1":
            user = _login(manager)
            if user:
                return user
        elif choice == "2":
            _register(manager)
        elif choice == "0":
            return None
        else:
            error("Invalid option. Please try again.")
            input("\n  Press Enter to continue...")


def _login(manager) -> object:
    section("LOGIN")
    username = prompt("Username")
    password = prompt("Password")

    user = manager.login(username, password)
    if user:
        success(f"Welcome back, {user.full_name}!")
        input("\n  Press Enter to continue...")
        return user
    else:
        error("Invalid username or password.")
        input("\n  Press Enter to continue...")
        return None


def _register(manager):
    section("STUDENT REGISTRATION")

    username = prompt("Choose a username (3-20 chars, letters/numbers/_)")
    if not validate_username(username):
        error("Invalid username format.")
        input("\n  Press Enter to continue...")
        return

    if manager.users.get(username):
        error("Username already taken. Please choose another.")
        input("\n  Press Enter to continue...")
        return

    full_name = prompt("Full name")
    if not full_name:
        error("Full name cannot be empty.")
        input("\n  Press Enter to continue...")
        return

    password = prompt("Password (min 6 chars)")
    if not validate_password(password):
        error("Password must be at least 6 characters.")
        input("\n  Press Enter to continue...")
        return

    confirm_pass = prompt("Confirm password")
    if password != confirm_pass:
        error("Passwords do not match.")
        input("\n  Press Enter to continue...")
        return

    user = manager.register_user(username, password, full_name)
    if user:
        success(f"Account created! Welcome, {full_name}!")
        info(f"Your user ID: {user.user_id}")
    else:
        error("Registration failed. Username may already exist.")

    input("\n  Press Enter to continue...")
