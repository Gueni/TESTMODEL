# ============================================================
# error_handler_final_true_skip.py
# Fully silent, true skipping, safe recovery + hints
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# ✅ GLOBAL CONSOLE + LOCK
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# ------------------------------------------------------------
# ✅ Global exception suppression
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    """Prevent Python from showing unwanted tracebacks globally."""
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ✅ ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints for variables with optional force_skip flag."""
    def __init__(self):
        self.hints = []  # list of tuples: (var, force_skip, message)
        self.shown_hints = set()

    def add(self, var, message, force_skip=False):
        """Add a hint. If force_skip=True → jump to recovery immediately."""
        self.hints.append((var, force_skip, message))

    def get_last(self):
        """Return the last hint tuple."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        self.hints.clear()
        self.shown_hints.clear()

    def should_show(self, msg):
        """Avoid printing the same hint multiple times."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

# ------------------------------------------------------------
# ✅ Recovery runner
# ------------------------------------------------------------
def _run_recovery(obj, current_func_name):
    """Run recovery function safely, halting any further operations silently."""
    recovery_func_name = None
    if hasattr(obj.__class__, "_safe_rules"):
        rules = obj.__class__._safe_rules
        recovery_func_name = rules.get(current_func_name)
        if not recovery_func_name and rules:
            recovery_func_name = next(iter(rules.values()), None)

    if not recovery_func_name:
        return

    ran_flag = f"_{recovery_func_name}_ran"
    orig_name = f"__orig_{recovery_func_name}"

    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()
            setattr(obj, ran_flag, True)
        except Exception as e:
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_last()
                if last_hint:
                    _, _, msg = last_hint
                    suggestion = msg
            if not suggestion:
                suggestion = f"{type(e).__name__}: {e}"

            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red",
                    )
                )
            # Stop all further function executions
            if hasattr(obj, "_skip_lock"):
                with obj._skip_lock:
                    obj._skip_next_steps = True

# ------------------------------------------------------------
# ✅ Safe function wrapper
# ------------------------------------------------------------
def safe_function(func):
    """Wrap a function to silently catch exceptions, skip, and call recovery."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        # If standalone function, just try/except
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        # Initialize lock and skip flag if missing
        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()
        if not hasattr(self_obj, "_skip_next_steps"):
            self_obj._skip_next_steps = False

        # ---------------------------
        # Skip immediately if flagged
        # ---------------------------
        with self_obj._skip_lock:
            if self_obj._skip_next_steps:
                return None

        # ---------------------------
        # Run the function safely
        # ---------------------------
        try:
            return func(*args, **kwargs)

        except Exception as e:
            # Extract last hint info
            suggestion = f"{type(e).__name__}: {e}"
            force_skip = False
            if hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last()
                if last_hint:
                    _, force_skip, msg = last_hint
                    suggestion = msg

            # Print hint panel (once)
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

            # ---------------------------
            # Force skip and recovery
            # ---------------------------
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            # Otherwise, continue silently (skip=False)
            return None

    return wrapper

# ------------------------------------------------------------
# ✅ Safe class decorator
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Decorate all class methods safely, only once."""
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
