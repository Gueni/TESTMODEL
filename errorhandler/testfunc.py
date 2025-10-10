# ============================================================
# error_handler_final_silent.py — fully silent + non-crashing
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# ✅ MULTITHREAD FLAG
# Set this to True if your code will run in multithreaded context.
# If False, skips locks but works normally in single-threaded mode.
# This flag can be toggled manually at the start of your program.
# ------------------------------------------------------------
USE_MULTITHREAD = True

# ------------------------------------------------------------
# ✅ GLOBAL CONSOLE + LOCK
# Only create one Rich Console object and lock to prevent
# multiple prints from interleaving in threads
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()

# Only create one global lock if multithreading is enabled
if "CONSOLE_LOCK" not in globals() and USE_MULTITHREAD:
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK if USE_MULTITHREAD else None  # use lock only if multithread

# ------------------------------------------------------------
# ✅ Global exception suppression
# Overrides Python's default exception handler to prevent
# tracebacks from being printed to console. Only our panels
# will be printed.
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    """Prevent Python from showing unwanted tracebacks globally."""
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ✅ ErrorHint class
# Stores hints for variables with optional force_skip flag
# ------------------------------------------------------------
class ErrorHint:
    """Stores variable hints for exceptions and warnings."""
    def __init__(self):
        # List of tuples: (variable_name, force_skip_flag, message)
        self.hints = []
        # Keeps track of printed messages to prevent duplicate panels
        self.shown_hints = set()

    def add(self, var, message, force_skip=False):
        """
        Add a hint for a variable.
        If force_skip=True, triggers immediate jump to recovery.
        """
        self.hints.append((var, force_skip, message))

    def get_last(self):
        """Return the last added hint tuple (var, force_skip, message)."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        """Clear all hints and printed records."""
        self.hints.clear()
        self.shown_hints.clear()

    def should_show(self, msg):
        """
        Determine if a panel should be shown.
        Prevents the same hint from being printed multiple times.
        """
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

# ------------------------------------------------------------
# ✅ Recovery runner
# Handles execution of recovery functions safely
# Does not crash, does not print Python tracebacks
# ------------------------------------------------------------
def _run_recovery(obj, current_func_name):
    """
    Run the recovery method mapped for the current function.
    If recovery itself fails, prints panel and silently stops
    further work without crashing.
    """
    recovery_func_name = None

    # Get recovery mapping from class rules
    if hasattr(obj.__class__, "_safe_rules"):
        rules = obj.__class__._safe_rules
        recovery_func_name = rules.get(current_func_name)
        # fallback: pick first recovery if current function not mapped
        if not recovery_func_name and rules:
            recovery_func_name = next(iter(rules.values()), None)

    if not recovery_func_name:
        return  # no recovery defined

    ran_flag = f"_{recovery_func_name}_ran"   # flag to prevent running recovery twice
    orig_name = f"__orig_{recovery_func_name}"

    # Only run if original exists and not yet ran
    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()      # run recovery
            setattr(obj, ran_flag, True)   # mark as ran
        except Exception as e:
            # get last hint if exists
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_last()
                if last_hint:
                    _, _, msg = last_hint
                    suggestion = msg
            if not suggestion:
                suggestion = f"{type(e).__name__}: {e}"

            # Show panel for recovery failure (silent, no traceback)
            if USE_MULTITHREAD:
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{suggestion}[/bold yellow]",
                            title="[bright_red]Exception in recovery — HALT[/bright_red]",
                            border_style="red",
                        )
                    )
            else:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red",
                    )
                )

            # Mark skip to prevent further work
            if hasattr(obj, "_skip_lock") and USE_MULTITHREAD:
                with obj._skip_lock:
                    obj._skip_next_steps = True
            elif not USE_MULTITHREAD:
                obj._skip_next_steps = True

# ------------------------------------------------------------
# ✅ Safe function wrapper
# Wraps any method, catches exceptions, shows panels,
# optionally triggers recovery
# ------------------------------------------------------------
def safe_function(func):
    """Wraps a function with silent error handling and optional recovery."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        # Handle standalone functions (not methods)
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        # Initialize per-object skip lock if multithread
        if not hasattr(self_obj, "_skip_lock") and USE_MULTITHREAD:
            self_obj._skip_lock = threading.Lock()

        # Check skip flag
        skip_now = getattr(self_obj, "_skip_next_steps", False)
        if skip_now:
            return None

        try:
            return func(*args, **kwargs)
        except Exception as e:
            suggestion = f"{type(e).__name__}: {e}"
            force_skip = False

            # Get last hint if exists
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
                if USE_MULTITHREAD:
                    with self_obj._skip_lock:
                        console.print(
                            Panel.fit(
                                f"[bold yellow]{suggestion}[/bold yellow]",
                                title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                                border_style="red",
                            )
                        )
                else:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{suggestion}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )

            # Trigger recovery if force_skip=True
            if force_skip:
                if USE_MULTITHREAD:
                    with self_obj._skip_lock:
                        self_obj._skip_next_steps = True
                else:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            return None

    return wrapper

# ------------------------------------------------------------
# ✅ safe_class decorator
# Automatically wraps all class methods safely
# Ensures single wrap even with multiple imports
# ------------------------------------------------------------
def safe_class(skip_rules):
    """
    Decorate all methods in a class with safe_function.
    skip_rules: dict {method_name: recovery_method_name}
    """
    def decorator(cls):
        # Prevent double wrapping if class imported multiple times
        if getattr(cls, "_already_wrapped", False):
            return cls

        cls._safe_rules = skip_rules

        # Wrap every callable method (except __dunder__ methods)
        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method))

        cls._already_wrapped = True
        return cls
    return decorator
