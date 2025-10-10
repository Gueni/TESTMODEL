# ============================================================
# error_handler_3.py
# Safe error handler with skip/recovery + Rich panel display
# Fully thread-safe and skip-enforced version
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# ✅ GLOBAL SINGLETONS
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK


# ------------------------------------------------------------
# ✅ ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints for variables, with optional force_skip flag."""

    def __init__(self):
        self.hints = []          # [(var_name, force_skip, message)]
        self.shown_hints = set() # to prevent repeated panels

    def add(self, var, message, force_skip=False):
        """Add a hint. If force_skip=True, skip all following steps."""
        self.hints.append((var, force_skip, message))

    def get_last(self):
        """Return (var, force_skip, msg) of the last hint."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        """Reset all hints and shown panels."""
        self.hints.clear()
        self.shown_hints.clear()

    def should_show(self, msg):
        """Show each hint message only once."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True


# ------------------------------------------------------------
# ✅ Recovery function runner
# ------------------------------------------------------------
def _run_recovery(obj, recovery_func_name):
    """Run recovery safely; halt program if it fails."""
    ran_flag = f"_{recovery_func_name}_ran"
    if hasattr(obj, f"__orig_{recovery_func_name}") and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, f"__orig_{recovery_func_name}")()
            setattr(obj, ran_flag, True)
        except Exception as e:
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_last()
                if last_hint:
                    _, _, msg = last_hint
                    suggestion = msg
            if not suggestion:
                suggestion = str(e)
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red",
                    )
                )
            sys.exit(1)


# ------------------------------------------------------------
# ✅ Safe function wrapper (thread + skip safe)
# ------------------------------------------------------------
def safe_function(func, recovery_func_name=None):
    """Decorator for function safety, with skip & recovery logic."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        if not self_obj:
            return func(*args, **kwargs)

        # Ensure skip flag has a thread lock on read/write
        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        # 🔒 Atomic check for skip flag
        with self_obj._skip_lock:
            skip_now = getattr(self_obj, "_skip_next_steps", False)

        # Skip logic: recovery always allowed, others are blocked
        if skip_now:
            if not (recovery_func_name and func.__name__ == recovery_func_name):
                return None

        try:
            return func(*args, **kwargs)

        except Exception as e:
            suggestion = f"{type(e).__name__}: {e}"
            force_skip = False

            # Extract the latest hint
            if hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last()
                if last_hint:
                    _, force_skip, msg = last_hint
                    suggestion = msg

            # Avoid duplicate panels
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

            # 🔒 Atomic set skip flag (thread-safe)
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, recovery_func_name)

            return None

    return wrapper


# ------------------------------------------------------------
# ✅ Safe class decorator
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Decorate all methods with safe_function; no double wrapping."""
    def decorator(cls):
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
