from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys

console = Console()


class ErrorHint:
    """Stores variable-specific hints and allows retrieval by key or last hint."""
    def __init__(self):
        self.hints = {}  # key -> message
        self.last_key = None

    def add(self, key, message):
        """Add a hint for a given variable or context key."""
        self.hints[key] = message
        self.last_key = key  # keep track of most recently added

    def get(self, key=None):
        """Get a hint by key, or fallback to the last one if no key given."""
        if key and key in self.hints:
            return self.hints[key]
        if self.last_key:
            return self.hints[self.last_key]
        return None

    def clear(self):
        """Clear all hints."""
        self.hints.clear()
        self.last_key = None


def safe_function(func, recovery_func_name=None, cls=None):
    """Wrap a function with error catching, skipping, and hint display logic."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        try:
            # Skip logic — if skip flag is set, only allow recovery function to run
            if getattr(self_obj, "_skip_next_steps", False):
                if recovery_func_name and func.__name__ == recovery_func_name:
                    pass  # allow recovery to run
                else:
                    return None

            return func(*args, **kwargs)

        except Exception as e:
            # Mark skip flag if a recovery is defined
            if self_obj and recovery_func_name:
                self_obj._skip_next_steps = True

            # === Hint handling ===
            suggestion = None
            if self_obj and hasattr(self_obj, "hint"):
                hint_obj = self_obj.hint
                suggestion = hint_obj.get()  # always get last hint, no fallback to exception text

            # If no hint exists, fallback to exception type/message
            if not suggestion:
                suggestion = f"{type(e).__name__}: {str(e)}"

            # Display a single red bordered error panel
            console.print(
                Panel.fit(
                    f"[bold yellow]{suggestion}[/bold yellow]",
                    title="[bright_red]Exception caught[/bright_red]",
                    border_style="red"
                )
            )

            # === Recovery logic ===
            if self_obj and recovery_func_name:
                ran_flag = f"_{recovery_func_name}_ran"
                recovery_func = getattr(self_obj, f"__orig_{recovery_func_name}", None)

                if recovery_func and not getattr(self_obj, ran_flag, False):
                    try:
                        recovery_func()
                        setattr(self_obj, ran_flag, True)
                    except Exception as fatal:
                        # Show the hint or exception of the recovery function and then exit
                        suggestion = None
                        if self_obj and hasattr(self_obj, "hint"):
                            suggestion = self_obj.hint.get()
                        if not suggestion:
                            suggestion = f"{type(fatal).__name__}: {str(fatal)}"

                        console.print(
                            Panel.fit(
                                f"[bold yellow]{suggestion}[/bold yellow]",
                                title="[bright_red]Exception caught[/bright_red]",
                                border_style="red"
                            )
                        )
                        sys.exit(1)

            return None
    return wrapper


def safe_class(skip_rules):
    """Applies safe_function wrapper to all methods in a class."""
    def decorator(cls):
        for name, method in list(cls.__dict__.items()):
            if callable(method):
                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method, recovery_func_name, cls))
        return cls
    return decorator
