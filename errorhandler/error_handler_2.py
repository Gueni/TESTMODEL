# ============================================================
# error_handler_final_func_hint.py — function-based hints only
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

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
# Suppress unwanted tracebacks globally
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    pass
sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ErrorHint class (function-based)
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints for functions, with optional force_skip flag."""
    def __init__(self):
        # Each hint: (function_name, force_skip, message)
        self.hints = []
        self.shown_hints = set()

    def add(self, message, force_skip=False):
        """Add a hint for the current function."""
        import inspect
        frame = inspect.currentframe()
        try:
            func_name = frame.f_back.f_code.co_name  # function calling add()
        finally:
            del frame
        self.hints.append((func_name, force_skip, message))

    def get_for_function(self, func_name):
        """Return the most recent hint for a given function."""
        for f, force, msg in reversed(self.hints):
            if f == func_name:
                return f, force, msg
        return None

    def get_last_for_function(self, func_name):
        """Alias for clarity."""
        return self.get_for_function(func_name)

    def should_show(self, msg):
        """Avoid duplicate panel prints."""
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
                last_hint = obj.hint.get_last_for_function(recovery_func_name)
                if last_hint:
                    _, _, suggestion = last_hint
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

        with self_obj._skip_lock:
            if getattr(self_obj, "_skip_next_steps", False):
                return None

        try:
            return func(*args, **kwargs)

        except Exception as e:
            force_skip = False
            suggestion = f"{type(e).__name__}: {e}"

            if hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last_for_function(func.__name__)
                if last_hint:
                    _, force_skip, suggestion = last_hint

            if hasattr(self_obj, "hint") and self_obj.hint.should_show(suggestion):
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{suggestion}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )

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
