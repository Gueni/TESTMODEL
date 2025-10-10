from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys

console = Console()


class ErrorHint:
    """Stores hints for variables, with optional force_skip flag."""
    def __init__(self):
        self.hints = []  # list of tuples: (var, force_skip, message)

    def add(self, var, message, force_skip=False):
        """Add a hint. If force_skip=True, jumps to recovery immediately."""
        self.hints.append((var, force_skip, message))

    def get_for_var(self, var):
        """Return the last hint for a specific variable."""
        for v, force, msg in reversed(self.hints):
            if v == var:
                return v, force, msg
        return None

    def get_last(self):
        """Return the last added hint tuple."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        self.hints.clear()


def safe_function(func, recovery_func_name=None):
    """Wrap a function with skip-on-error and recovery logic."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        # Skip logic if flag is already set
        if getattr(self_obj, "_skip_next_steps", False):
            if recovery_func_name and func.__name__ == recovery_func_name:
                pass  # always allow recovery function
            else:
                return None

        try:
            return func(*args, **kwargs)

        except Exception as e:
            # Check for the last hint
            suggestion = None
            force_skip = False
            if self_obj and hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last()
                if last_hint:
                    _, force_skip, msg = last_hint
                    suggestion = msg

            # Always print the panel for either hint or exception
            if not suggestion:
                suggestion = f"{type(e).__name__}: {str(e)}"

            console.print(
                Panel.fit(
                    f"[bold yellow]{suggestion}[/bold yellow]",
                    title="[bright_red]Exception caught[/bright_red]",
                    border_style="red"
                )
            )

            # Only jump to recovery if hint has force_skip=True
            if self_obj and recovery_func_name and force_skip:
                self_obj._skip_next_steps = True
                _run_recovery(self_obj, recovery_func_name)
                return None

            # Otherwise, continue normally (force_skip=False)
            return None

    return wrapper


def _run_recovery(obj, recovery_func_name):
    """Call recovery function and halt if it fails."""
    ran_flag = f"_{recovery_func_name}_ran"
    if hasattr(obj, f"__orig_{recovery_func_name}") and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, f"__orig_{recovery_func_name}")()
            setattr(obj, ran_flag, True)
        except Exception as e:
            # Show hint if exists
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_last()
                if last_hint:
                    _, _, msg = last_hint
                    suggestion = msg
            if not suggestion:
                suggestion = str(e)
            console.print(
                Panel.fit(
                    f"[bold yellow]{suggestion}[/bold yellow]",
                    title="[bright_red]Exception in recovery — HALT[/bright_red]",
                    border_style="red"
                )
            )
            sys.exit(1)


def safe_class(skip_rules):
    """Wrap all class methods with safe_function."""
    def decorator(cls):
        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method, recovery_func_name))
        return cls
    return decorator
