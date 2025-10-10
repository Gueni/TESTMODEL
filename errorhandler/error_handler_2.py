# ============================================================
# error_handler_final_fixed.py — reliable, multi-thread + loops
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# Global console + lock (avoid duplicate panels)
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# ------------------------------------------------------------
# Global exception suppression to prevent tracebacks
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    """Prevent Python from printing unwanted tracebacks."""
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores variable hints with optional force_skip flag."""
    def __init__(self):
        self.hints = []  # list of (var, force_skip, message)
        self.shown_hints = set()

    def add(self, var, message, force_skip=False):
        """Add a hint. If force_skip=True → jump to recovery immediately."""
        self.hints.append((var, force_skip, message))

    def get_for_var(self, var):
        """Return the most recent hint for a specific variable."""
        for v, force, msg in reversed(self.hints):
            if v == var:
                return v, force, msg
        return None

    def get_last(self):
        """Return the last added hint tuple."""
        return self.hints[-1] if self.hints else None

    def should_show(self, msg):
        """Ensure same hint is not printed multiple times."""
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
    """Run the recovery function once, silently halt on error."""
    recovery_func_name = None
    if hasattr(obj.__class__, "_safe_rules"):
        rules = obj.__class__._safe_rules
        recovery_func_name = rules.get(current_func_name)
        if not recovery_func_name and rules:
            recovery_func_name = next(iter(rules.values()), None)

    if not recovery_func_name:
        return  # no recovery defined

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
                    _, _, suggestion = last_hint
            if not suggestion:
                suggestion = f"{type(e).__name__}: {e}"

            # Display recovery failure panel
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red",
                    )
                )
            # Stop further execution silently
            with obj._skip_lock:
                obj._skip_next_steps = True

# ------------------------------------------------------------
# Safe function wrapper
# ------------------------------------------------------------
def safe_function(func):
    """Wrap a function with try/except, controlled recovery and skip."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        if not self_obj:
            # standalone function
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        # skip flagged methods
        with self_obj._skip_lock:
            if getattr(self_obj, "_skip_next_steps", False):
                return None

        try:
            return func(*args, **kwargs)

        except Exception as e:
            force_skip = False
            suggestion = f"{type(e).__name__}: {e}"

            # Try to match hint by variable from exception args
            var_name = getattr(e, "args", [None])[0]
            hint_for_var = None
            if hasattr(self_obj, "hint"):
                if var_name is not None:
                    hint_for_var = self_obj.hint.get_for_var(var_name)
                if not hint_for_var:
                    hint_for_var = self_obj.hint.get_last()

            if hint_for_var:
                _, force_skip, suggestion = hint_for_var

            # Show panel if not already shown
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

            # Force skip and recovery if requested
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            return None

    return wrapper

# ------------------------------------------------------------
# safe_class decorator
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Wrap all class methods safely, only once per class."""
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
