from functools import wraps
from rich.console import Console
from rich.panel import Panel
import threading
import sys

# ----------------------------
# Global console + lock
# ----------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()
console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# Silent tracebacks
sys.excepthook = lambda *args: None

# ----------------------------
# ErrorHint
# ----------------------------
class ErrorHint:
    """Stores hints per function call."""
    def __init__(self):
        self.hints = []  # list of (message, force_skip)
        self.shown = set()

    def add(self, message, force_skip=False):
        self.hints.append((message, force_skip))

    def get_first_unshown(self):
        for msg, _ in self.hints:
            if msg not in self.shown:
                return msg
        return None

    def has_force_skip(self):
        return any(force for _, force in self.hints)

    def mark_shown(self):
        for msg, _ in self.hints:
            self.shown.add(msg)

# ----------------------------
# Recovery runner
# ----------------------------
def _run_recovery(obj, func_name):
    rules = getattr(obj.__class__, "_safe_rules", {})
    recovery_name = rules.get(func_name)
    if not recovery_name:
        return
    ran_flag = f"_{recovery_name}_ran"
    orig_name = f"__orig_{recovery_name}"
    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()
            setattr(obj, ran_flag, True)
        except Exception:
            msg = f"Recovery {recovery_name} failed"
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{msg}[/bold yellow]",
                        title="[bright_red]Recovery Error[/bright_red]",
                        border_style="red"
                    )
                )
            with obj._skip_lock:
                obj._skip_next_steps = True

# ----------------------------
# Safe function wrapper
# ----------------------------
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
        if not hasattr(self_obj, "_skip_next_steps"):
            self_obj._skip_next_steps = False

        # Create a new hint container per function call
        self_obj._current_hint = ErrorHint()

        with self_obj._skip_lock:
            if self_obj._skip_next_steps:
                return None

        try:
            return func(*args, **kwargs)
        except Exception:
            hint_msg = self_obj._current_hint.get_first_unshown()
            if not hint_msg:
                hint_msg = f"{func.__name__} failed"

            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{hint_msg}[/bold yellow]",
                        title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                        border_style="red"
                    )
                )

            self_obj._current_hint.mark_shown()

            if self_obj._current_hint.has_force_skip():
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            return None

    return wrapper

# ----------------------------
# Safe class decorator
# ----------------------------
def safe_class(skip_rules):
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
