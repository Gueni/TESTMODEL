from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys

console = Console()

class ErrorHint:
    """Hint registry storing multiple variable hints per function."""
    def __init__(self):
        # Each entry is (var_name, force_skip, message)
        self.hints = []

    def add(self, hint_tuple):
        """Add a hint as (var_name, force_skip, message)."""
        if len(hint_tuple) != 3:
            raise ValueError("Hint must be a tuple: (variable, force_skip, message)")
        self.hints.append(hint_tuple)

    def get_last(self):
        """Return the last hint tuple (var_name, force_skip, message) or None."""
        return self.hints[-1] if self.hints else (None, False, None)

    def get_all(self):
        """Return all hints."""
        return self.hints[:]

    def clear(self):
        self.hints.clear()


def safe_function(func, recovery_func_name=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        try:
            # Skip everything if skip flag is set except recovery
            if getattr(self_obj, "_skip_next_steps", False):
                if recovery_func_name and func.__name__ == recovery_func_name:
                    pass
                else:
                    return None

            # Check if last hint has force_skip=True
            if self_obj and hasattr(self_obj, "hint"):
                _, force_skip, _ = self_obj.hint.get_last()
                if force_skip and recovery_func_name:
                    self_obj._skip_next_steps = True
                    getattr(self_obj, recovery_func_name)()
                    return None

            # Run function normally
            return func(*args, **kwargs)

        except Exception as e:
            # Get last hint tuple
            _, force_skip, message = (None, False, None)
            if self_obj and hasattr(self_obj, "hint"):
                _, force_skip, message = self_obj.hint.get_last()

            # Display hint or exception
            if not message:
                message = f"{type(e).__name__}: {str(e)}"

            console.print(
                Panel.fit(
                    f"[bold yellow]{message}[/bold yellow]",
                    title="[bright_red]Exception caught[/bright_red]",
                    border_style="red"
                )
            )

            # If force_skip or skip rule exists, call recovery
            if self_obj and recovery_func_name and (force_skip or recovery_func_name in getattr(self_obj, "_skip_rules", {})):
                self_obj._skip_next_steps = True
                try:
                    getattr(self_obj, recovery_func_name)()
                except Exception:
                    # Halt program if recovery itself fails
                    last_msg = self_obj.hint.get_last()[2]
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{last_msg}[/bold yellow]",
                            title="[bright_red]Recovery failed — halting[/bright_red]",
                            border_style="red"
                        )
                    )
                    sys.exit(1)

            return None

    return wrapper


def safe_class(skip_rules):
    """Wrap all methods of a class with safe_function."""
    def decorator(cls):
        cls._skip_rules = skip_rules.copy()
        for name, method in list(cls.__dict__.items()):
            if callable(method):
                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method, recovery_func_name))
        return cls
    return decorator
