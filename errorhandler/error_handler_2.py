# ============================================================
# error_handler_final_smart.py — full reliable version
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import threading
import sys

# ---------------- Global Console & Lock ----------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()
console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# ---------------- Silent Global Exception -------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    """Suppress Python traceback globally."""
    pass
sys.excepthook = _silent_excepthook

# ---------------- ErrorHint -------------------------------
class ErrorHint:
    """Store hints for a single function call."""
    def __init__(self):
        self.hints = []  # list of (force_skip, message)
        self.shown = set()

    def add(self, message, force_skip=False):
        self.hints.append((force_skip, message))

    def get_force_skip(self):
        """Return True if any hint forces skip."""
        return any(force for force, _ in self.hints)

    def get_messages(self):
        """Return all hint messages."""
        return [msg for _, msg in self.hints]

    def show_hints(self):
        """Show hints in panel, avoid duplicates."""
        for _, msg in self.hints:
            if msg not in self.shown:
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{msg}[/bold yellow]",
                            title="[bright_red]Hint[/bright_red]",
                            border_style="red",
                        )
                    )
                self.shown.add(msg)

# ---------------- Recovery runner --------------------------
def _run_recovery(obj, func_name):
    rules = getattr(obj.__class__, "_safe_rules", {})
    recovery_name = rules.get(func_name)
    if not recovery_name:
        return  # nothing to do

    ran_flag = f"_{recovery_name}_ran"
    orig_name = f"__orig_{recovery_name}"

    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()
            setattr(obj, ran_flag, True)
        except Exception as e:
            suggestion = f"Recovery {recovery_name} failed"
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red",
                    )
                )
            # stop everything
            with obj._skip_lock:
                obj._skip_next_steps = True

# ---------------- Safe function wrapper -------------------
def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()
        with self_obj._skip_lock:
            if getattr(self_obj, "_skip_next_steps", False):
                # skip all functions
                return None

        # Each function has its own hint container
        if not hasattr(self_obj, "_current_hint"):
            self_obj._current_hint = ErrorHint()
        self_obj._current_hint.clear()  # fresh hints for this call

        try:
            return func(*args, **kwargs)

        except Exception as e:
            # Show the panel only for this function
            self_obj._current_hint.show_hints()
            force_skip = self_obj._current_hint.get_force_skip()

            # If no hints, still show the exception
            if not self_obj._current_hint.hints:
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{type(e).__name__}: {e}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )

            # Force skip to recovery if requested
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            return None

    return wrapper

# ---------------- Safe class decorator --------------------
def safe_class(skip_rules):
    """Wrap all methods safely and store skip rules."""
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
