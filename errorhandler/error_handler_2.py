# ============================================================
# error_handler_final_func_only.py — reliable, multithread + loops
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import threading
import sys

# ------------------------------------------------------------
# Global console + lock
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()
console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# ------------------------------------------------------------
# Silent global exception handler
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ErrorHint class — now per-function only
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints per function with optional force_skip."""
    def __init__(self):
        # {func_name: [(force_skip, message), ...]}
        self.hints = {}
        self.shown_hints = set()

    def add(self, func_name, message, force_skip=False):
        """Add a hint for a specific function."""
        if func_name not in self.hints:
            self.hints[func_name] = []
        self.hints[func_name].append((force_skip, message))

    def get_last(self, func_name):
        """Return the last hint tuple for a function."""
        if func_name in self.hints and self.hints[func_name]:
            return self.hints[func_name][-1]
        return None

    def should_show(self, msg):
        """Prevent duplicate panels."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

    def clear(self):
        self.hints.clear()
        self.shown_hints.clear()

# ------------------------------------------------------------
# Recovery runner
# ------------------------------------------------------------
def _run_recovery(obj, current_func_name):
    """Run the mapped recovery function once and halt silently on failure."""
    recovery_func_name = getattr(obj.__class__, "_safe_rules", {}).get(current_func_name)
    if not recovery_func_name:
        return

    ran_flag = f"_{recovery_func_name}_ran"
    orig_name = f"__orig_{recovery_func_name}"

    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()
            setattr(obj, ran_flag, True)
        except Exception:
            # Show recovery hint if exists
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_last(recovery_func_name)
                if last_hint:
                    _, suggestion = last_hint
            if not suggestion:
                suggestion = f"Error in recovery"

            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red",
                    )
                )

            # Stop further execution immediately
            with obj._skip_lock:
                obj._skip_next_steps = True

# ------------------------------------------------------------
# Safe function wrapper
# ------------------------------------------------------------
def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        if not self_obj:
            # Standalone function
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        # Skip flagged functions
        with self_obj._skip_lock:
            if getattr(self_obj, "_skip_next_steps", False):
                return None

        try:
            return func(*args, **kwargs)

        except Exception:
            # Get last hint for this function
            force_skip, suggestion = False, f"{func.__name__} error"
            if hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last(func.__name__)
                if last_hint:
                    force_skip, suggestion = last_hint

            # Show panel once
            show_panel = True
            if hasattr(self_obj, "hint"):
                show_panel = self_obj.hint.should_show(suggestion)

            if show_panel:
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{suggestion}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )

            # Skip further calls and run recovery if forced
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            return None

    return wrapper

# ------------------------------------------------------------
# Safe class decorator
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Wrap all class methods safely and store skip rules."""
    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls

        cls._safe_rules = skip_rules

        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method))

        cls._already_wrapped = True
        return cls

    return decorator
