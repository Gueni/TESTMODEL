# ============================================================
# error_handler_4.py — Thread-safe, recovery-enforced handler
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# ✅ SINGLETON CONSOLE + LOCK
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK


# ------------------------------------------------------------
# ✅ ErrorHint
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
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True


# ------------------------------------------------------------
# ✅ Recovery Runner
# ------------------------------------------------------------
def _run_recovery(obj, recovery_func_name=None):
    """Run the recovery function; halt if recovery fails."""
    # If not given, find one defined in the class’ safe rules
    if recovery_func_name is None and hasattr(obj.__class__, "_safe_rules"):
        # pick the first recovery method in mapping
        recovery_func_name = next(iter(obj.__class__._safe_rules.values()), None)

    if not recovery_func_name:
        return  # No recovery function defined at all

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
# ✅ Safe Function Wrapper (thread-safe, recovery-aware)
# ------------------------------------------------------------
def safe_function(func, recovery_func_name=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        if not self_obj:
            return func(*args, **kwargs)

        # thread lock for this instance
        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        # atomic skip check
        with self_obj._skip_lock:
            skip_now = getattr(self_obj, "_skip_next_steps", False)

        # skip all except recovery
        if skip_now and not (recovery_func_name and func.__name__ == recovery_func_name):
            return None

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

            # prevent duplicate panel prints
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

            # enforce skip & recovery
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, recovery_func_name)
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

        cls._safe_rules = skip_rules  # store for dynamic recovery lookup

        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method, recovery_func_name))

        cls._already_wrapped = True
        return cls
    return decorator
