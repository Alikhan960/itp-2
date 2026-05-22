"""
utils/decorators.py
Custom decorators used throughout EventHub.
"""

import time
import functools


def admin_required(func):
    """
    Decorator that restricts access to admin-only functions.
    The decorated function must receive 'current_user' as first argument.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # EventManager methods receive 'current_user' as first positional arg
        if args and hasattr(args[0], "role"):
            user = args[0]
        else:
            user = kwargs.get("current_user")

        if user is None or user.role != "admin":
            print("\n  [!] Access Denied: Administrator privileges required.")
            return None
        return func(self, *args, **kwargs)
    return wrapper


def time_logger(func):
    """
    Decorator that logs the execution time of a function.
    Useful for tracking performance of file I/O operations.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  [⏱] {func.__name__} completed in {elapsed:.2f} ms")
        return result
    return wrapper


def validate_input(func):
    """
    Decorator that catches common input errors gracefully.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError) as exc:
            print(f"\n  [!] Input error: {exc}")
            return None
        except KeyboardInterrupt:
            print("\n\n  [!] Operation cancelled by user.")
            return None
    return wrapper
