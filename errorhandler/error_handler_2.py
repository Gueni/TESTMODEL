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

# Silent global exceptions
sys.excepthook = lambda *args: None

# ------------------------------------------------------------
# ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    def __init__(self):
        self.hints = []  # list of (message, force_skip)
        self.shown = set()

    def add(self, message, force_skip=False):
        self.hints.append((message, force_skip))

    def get_panel_hint(self):
        """Return first hint that hasn’t been shown yet."""
        for msg, _ in self.hints:
            if msg not in self.shown:
                return msg
        return None

    def has_force_skip(self):
        return any(force for _, force in self.hints)

    def mark_shown(self):
        for msg, _ in self.hints:
            self.shown.add(msg)

# ------------------------------------------------------------
# Recovery runner
# ------------------------------------------------------------
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
            suggestion = f"Recovery {recovery_name} failed"
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Recovery Error[/bright_red]",
                        border_style="red"
                    )
                )
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
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()
        if not hasattr(self_obj, "_skip_next_steps"):
            self_obj._skip_next_steps = False
        if not hasattr(self_obj, "_current_hint"):
            self_obj._current_hint = ErrorHint()

        with self_obj._skip_lock:
            if self_obj._skip_next_steps:
                return None  # skip everything if flagged

        try:
            return func(*args, **kwargs)
        except Exception:
            # Show panel with hint if exists
            msg = self_obj._current_hint.get_panel_hint()
            if not msg:
                msg = f"{func.__name__} failed"

            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{msg}[/bold yellow]",
                        title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                        border_style="red"
                    )
                )

            self_obj._current_hint.mark_shown()

            # If any hint is force_skip → skip rest and run recovery
            if self_obj._current_hint.has_force_skip():
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            return None

    return wrapper

# ------------------------------------------------------------
# safe_class decorator
# ------------------------------------------------------------
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
