# ============================================================
# error_handler_2.py
# Safe error handler with skip/recovery + Rich panel display
# Supports multiple imports safely (no duplicate panels)
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys

# ------------------------------------------------------------
# ✅ Create ONE global console instance (no duplicate panels)
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
console = GLOBAL_CONSOLE


# ------------------------------------------------------------
# ✅ ErrorHint class
# Stores variable hints with optional force_skip flag
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints for variables, with optional force_skip flag."""

    def __init__(self):
        # Each hint is a tuple: (var_name, force_skip, message)
        self.hints = []

    def add(self, var, message, force_skip=False):
        """Add a hint for a variable. 
        If force_skip=True → jump to recovery immediately.
        """
        self.hints.append((var, force_skip, message))

    def get_for_var(self, var):
        """Return the most recent hint for a specific variable."""
        for v, force, msg in reversed(self.hints):
            if v == var:
                return v, force, msg
        return None

    def get_last(self):
        """Return the most recently added hint tuple (var, force_skip, msg)."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        """Remove all stored hints."""
        self.hints.clear()


# ------------------------------------------------------------
# ✅ Safe function wrapper
# Catches exceptions and optionally jumps to recovery
# ------------------------------------------------------------
def safe_function(func, recovery_func_name=None):
    """Wraps a method with safe error catching and skip/recovery handling."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        # Skip methods if _skip_next_steps flag is set (except recovery)
        if getattr(self_obj, "_skip_next_steps", False):
            if recovery_func_name and func.__name__ == recovery_func_name:
                pass  # always allow recovery
            else:
                return None

        try:
            # Execute the wrapped function normally
            return func(*args, **kwargs)

        except Exception as e:
            suggestion = None
            force_skip = False

            # Try to extract the most recent hint message
            if self_obj and hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last()
                if last_hint:
                    _, force_skip, msg = last_hint
                    suggestion = msg

            # Fallback if no hint message is available
            if not suggestion:
                suggestion = f"{type(e).__name__}: {str(e)}"

            # Print a Rich panel showing the issue
            console.print(
                Panel.fit(
                    f"[bold yellow]{suggestion}[/bold yellow]",
                    title="[bright_red]Exception caught[/bright_red]",
                    border_style="red",
                )
            )

            # Jump to recovery if hint had force_skip=True
            if self_obj and recovery_func_name and force_skip:
                self_obj._skip_next_steps = True
                _run_recovery(self_obj, recovery_func_name)
                return None

            # Otherwise, just continue normally (force_skip=False)
            return None

    return wrapper


# ------------------------------------------------------------
# ✅ Recovery runner
# Executes recovery function and halts program if it fails
# ------------------------------------------------------------
def _run_recovery(obj, recovery_func_name):
    """Run the recovery function safely, halting on fatal errors."""
    ran_flag = f"_{recovery_func_name}_ran"
    if hasattr(obj, f"__orig_{recovery_func_name}") and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, f"__orig_{recovery_func_name}")()
            setattr(obj, ran_flag, True)
        except Exception as e:
            # Try to show any available hint message
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
                    border_style="red",
                )
            )
            sys.exit(1)


# ------------------------------------------------------------
# ✅ safe_class decorator
# Wraps each class method once (prevents double wrapping)
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Decorate all class methods with safe_function (with skip/recovery)."""
    def decorator(cls):
        # Prevent multiple wrapping due to repeated imports
        if getattr(cls, "_already_wrapped", False):
            return cls

        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method, recovery_func_name))

        cls._already_wrapped = True
        return cls

    return decorator
