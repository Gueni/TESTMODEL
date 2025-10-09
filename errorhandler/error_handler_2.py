from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys

console = Console()  # Rich console for colored output panels


class ErrorHint:
    """Stores hints for variables, each hint optionally marked with force_skip."""

    def __init__(self):
        # List of tuples: (variable/object, force_skip flag, message string)
        self.hints = []

    def add(self, var, message, force_skip=False):
        """
        Add a hint for a variable or object.
        - var: variable or object related to the hint
        - message: string describing the hint
        - force_skip: if True, triggers skip to recovery immediately
        """
        self.hints.append((var, force_skip, message))

    def get_for_var(self, var):
        """
        Return the last hint tuple for a specific variable/object.
        Searches hints in reverse so the most recent relevant hint is returned.
        Returns None if no matching hint is found.
        """
        for v, force, msg in reversed(self.hints):
            if v == var:
                return v, force, msg
        return None

    def get_last(self):
        """Return the last added hint tuple (var, force_skip, message) or None if empty."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        """Clear all stored hints."""
        self.hints.clear()


def safe_function(func, recovery_func_name=None):
    """
    Decorator to wrap a method with error handling, skip, and recovery logic.
    
    - func: original method to wrap
    - recovery_func_name: optional name of recovery function to call on forced skip
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None  # Get the instance from method arguments

        # --- Skip logic: skip execution if _skip_next_steps is True ---
        if getattr(self_obj, "_skip_next_steps", False):
            # Always allow the recovery function to run even if skipping
            if recovery_func_name and func.__name__ == recovery_func_name:
                pass
            else:
                return None  # Skip this method entirely

        try:
            # Call the original function normally
            return func(*args, **kwargs)

        except Exception as e:
            # --- Exception handling ---
            suggestion = None
            force_skip = False

            # If hints exist, get the last one
            if self_obj and hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last()
                if last_hint:
                    _, force_skip, msg = last_hint
                    suggestion = msg

            # Fallback to exception message if no hint found
            if not suggestion:
                suggestion = f"{type(e).__name__}: {str(e)}"

            # Display the hint/exception in a rich panel
            console.print(
                Panel.fit(
                    f"[bold yellow]{suggestion}[/bold yellow]",
                    title="[bright_red]Exception caught[/bright_red]",
                    border_style="red"
                )
            )

            # --- Force skip: if last hint has force_skip=True, jump to recovery ---
            if self_obj and recovery_func_name and force_skip:
                self_obj._skip_next_steps = True
                _run_recovery(self_obj, recovery_func_name)
                return None  # Stop further execution of this function

            # Otherwise, continue execution (no skip)
            return None

    return wrapper


def _run_recovery(obj, recovery_func_name):
    """
    Call the recovery function and handle exceptions in it.
    Halts the program if the recovery function itself raises an error.
    """
    ran_flag = f"_{recovery_func_name}_ran"  # flag to prevent multiple calls
    if hasattr(obj, f"__orig_{recovery_func_name}") and not getattr(obj, ran_flag, False):
        try:
            # Call the original unwrapped recovery function
            getattr(obj, f"__orig_{recovery_func_name}")()
            setattr(obj, ran_flag, True)
        except Exception as e:
            # Show last hint in recovery if available
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_last()
                if last_hint:
                    _, _, msg = last_hint
                    suggestion = msg
            if not suggestion:
                suggestion = str(e)

            # Print panel for fatal recovery error and exit
            console.print(
                Panel.fit(
                    f"[bold yellow]{suggestion}[/bold yellow]",
                    title="[bright_red]Exception in recovery — HALT[/bright_red]",
                    border_style="red"
                )
            )
            sys.exit(1)  # halt program immediately


def safe_class(skip_rules):
    """Wrap all class methods with safe_function."""
    def decorator(cls):
        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                # --- Only wrap if not already wrapped ---
                if getattr(method, "_is_safe_wrapped", False):
                    continue

                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                wrapped = safe_function(method, recovery_func_name)
                wrapped._is_safe_wrapped = True  # mark it as wrapped
                setattr(cls, name, wrapped)
        return cls
    return decorator
