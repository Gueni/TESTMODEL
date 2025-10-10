# ============================================================
# error_handler_final.py — Clean, quiet version
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading
import traceback

# ------------------------------------------------------------
# ✅ GLOBAL SHARED CONSOLE + LOCK
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK


# ------------------------------------------------------------
# ✅ Suppress all tracebacks systemwide
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    """Suppress traceback printing — only Rich panels are shown."""
    pass  # Do nothing — handled by safe_function already

sys.excepthook = _silent_excepthook


# ------------------------------------------------------------
# ✅ ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores variable hints and force_skip flag."""
    def __init__(self):
        self.hints = []
        self.shown_hints = set()

    def add(self, var, message, force_skip=False):
        self.hints.append((var, force_skip, message))

    def get_last(self):
        return self.hints[-1] if self.hints else None

    def clear(self):
        self.hints.clear()
        self.shown_hints.clear()

    def should_show(self, msg):
        """Prevent duplicate printing for same message"""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True


# ------------------------------------------------------------
# ✅ Recovery runner
# ------------------------------------------------------------
def _run_recovery(obj, current_func_name):
    """Run the mapped recovery function based on skip_rules."""
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

            # ✅ Exit quietly — no tracebacks, no extra noise
            sys.exit(0)


# ------------------------------------------------------------
# ✅ Safe function wrapper
# ------------------------------------------------------------
def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                # swallow exceptions if used standalone
                return None

        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        with self_obj._skip_lock:
            skip_now = getattr(self_obj, "_skip_next_steps", False)

        if skip_now:
            return None  # skip execution if flagged

        try:
            return func(*args, **kwargs)

        except Exception as e:
            suggestion = f"{type(e).__name__}: {e}"
            force_skip = False

            if hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last()
                if last_hint:
                    _, force_skip, msg = last_hint
                    suggestion = msg

            # show panel once
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

            # if forced, skip all next + run mapped recovery
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            return None

    return wrapper


# ------------------------------------------------------------
# ✅ Safe Class Decorator
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Wraps all class methods with safe_function once."""
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
