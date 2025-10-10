# ============================================================
# error_handler_final.py
# Fully working safe error handler with per-function hints
# Force-skip jumps to recovery, panels clean, no tracebacks
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# Global console and lock (prevents multiple panels)
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()
console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# ------------------------------------------------------------
# Global suppression of unwanted tracebacks
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ErrorHint class: per-function hints
# ------------------------------------------------------------
class ErrorHint:
    """Stores per-function hint messages with force_skip flag."""
    def __init__(self):
        # function_name -> (message, force_skip)
        self.hints = {}
        self.shown_hints = set()

    def add(self, func_name, message, force_skip=False):
        """Register a hint for a function."""
        self.hints[func_name] = (message, force_skip)

    def get_for_func(self, func_name):
        """Return hint tuple for a specific function."""
        return self.hints.get(func_name, None)

    def should_show(self, msg):
        """Avoid printing same hint multiple times."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

# ------------------------------------------------------------
# Recovery runner
# ------------------------------------------------------------
def _run_recovery(obj, recovery_func_name):
    """Run recovery function safely, exit cleanly on error."""
    ran_flag = f"_{recovery_func_name}_ran"
    orig_name = f"__orig_{recovery_func_name}"
    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()
            setattr(obj, ran_flag, True)
        except Exception:
            # Show panel with recovery function hint if exists
            suggestion = None
            if hasattr(obj, "hint"):
                hint = obj.hint.get_for_func(recovery_func_name)
                if hint:
                    suggestion = hint[0]
            if not suggestion:
                suggestion = f"Recovery {recovery_func_name} failed"
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red"
                    )
                )
            # Exit cleanly
            sys.exit(0)

# ------------------------------------------------------------
# Safe function wrapper
# ------------------------------------------------------------
def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        func_name = func.__name__

        if self_obj is None:
            # Standalone function: just catch exceptions
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        # Initialize skip lock if not present
        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()
        if not hasattr(self_obj, "_skip_next_steps"):
            self_obj._skip_next_steps = False

        # Skip this function if global skip is active
        with self_obj._skip_lock:
            if self_obj._skip_next_steps:
                return None

        # Check if hint exists for this function
        hint_tuple = None
        if hasattr(self_obj, "hint"):
            hint_tuple = self_obj.hint.get_for_func(func_name)
        message, force_skip = hint_tuple if hint_tuple else (None, False)

        # If hint has force_skip=True, skip to recovery immediately
        if force_skip and hasattr(self_obj, "_safe_rules"):
            recovery_func = self_obj._safe_rules.get(func_name)
            if recovery_func:
                if message and hasattr(self_obj, "hint") and self_obj.hint.should_show(message):
                    with console_lock:
                        console.print(
                            Panel.fit(
                                f"[bold yellow]{message}[/bold yellow]",
                                title=f"[bright_red]Force-skip in {func_name}[/bright_red]",
                                border_style="red"
                            )
                        )
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, recovery_func)
                return None

        # Try executing the function
        try:
            return func(*args, **kwargs)
        except Exception:
            # Show panel with hint if exists
            if message and hasattr(self_obj, "hint") and self_obj.hint.should_show(message):
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{message}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func_name}[/bright_red]",
                            border_style="red"
                        )
                    )
            # If hint is force_skip, trigger recovery
            if force_skip and hasattr(self_obj, "_safe_rules"):
                recovery_func = self_obj._safe_rules.get(func_name)
                if recovery_func:
                    with self_obj._skip_lock:
                        self_obj._skip_next_steps = True
                    _run_recovery(self_obj, recovery_func)
            return None

    return wrapper

# ------------------------------------------------------------
# safe_class decorator
# ------------------------------------------------------------
def safe_class(skip_rules=None):
    """Wrap all class methods with safe_function, only once."""
    skip_rules = skip_rules or {}
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
