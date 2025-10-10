# ============================================================
# error_handler_final_variable_hint.py
# Fully silent, true skipping, recovery + variable-specific hints
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# ✅ GLOBAL CONSOLE + LOCK (thread-safe)
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# ------------------------------------------------------------
# ✅ Suppress all unwanted tracebacks globally
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ✅ ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints for variables with optional force_skip flag."""
    def __init__(self):
        # hints: list of tuples (var_name/object, force_skip, message)
        self.hints = []
        self.shown_hints = set()

    def add(self, var, message, force_skip=False):
        """Add a hint for a variable or object."""
        self.hints.append((var, force_skip, message))

    def get_hint_for_var(self, var):
        """Return the last hint for a specific variable/object."""
        for v, fs, msg in reversed(self.hints):
            if v == var or v is None:
                return fs, msg
        return None, None

    def should_show(self, msg):
        """Avoid printing the same panel multiple times."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

    def clear(self):
        self.hints.clear()
        self.shown_hints.clear()

# ------------------------------------------------------------
# ✅ Recovery runner
# ------------------------------------------------------------
def _run_recovery(obj, current_func_name):
    """Call the mapped recovery function safely."""
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
            # Use hint if available, otherwise exception message
            suggestion = None
            if hasattr(obj, "hint"):
                _, msg = obj.hint.get_hint_for_var(getattr(e, "var", None))
                suggestion = msg
            if not suggestion:
                suggestion = f"{type(e).__name__}: {e}"

            # Thread-safe panel display
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red"
                    )
                )
            # Stop all further function execution silently
            if hasattr(obj, "_skip_lock"):
                with obj._skip_lock:
                    obj._skip_next_steps = True

# ------------------------------------------------------------
# ✅ Safe function wrapper
# ------------------------------------------------------------
def safe_function(func):
    """Wrap a function to catch exceptions silently, skip, and call recovery."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        # Standalone function
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        # Initialize skip lock/flag
        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()
        if not hasattr(self_obj, "_skip_next_steps"):
            self_obj._skip_next_steps = False

        # ---------------------------
        # Skip immediately if flagged
        # ---------------------------
        with self_obj._skip_lock:
            if self_obj._skip_next_steps:
                return None

        # ---------------------------
        # Run function safely
        # ---------------------------
        try:
            return func(*args, **kwargs)

        except Exception as e:
            # Determine which variable/object caused the exception
            exception_var = getattr(e, "var", None)

            suggestion = f"{type(e).__name__}: {e}"
            force_skip = False

            # Check for a matching hint for this variable/object
            if hasattr(self_obj, "hint"):
                fs, msg = self_obj.hint.get_hint_for_var(exception_var)
                if msg:
                    suggestion = msg
                    force_skip = fs

            # Show the panel only once per hint
            show_panel = True
            if hasattr(self_obj, "hint"):
                show_panel = self_obj.hint.should_show(suggestion)

            if show_panel:
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{suggestion}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                            border_style="red"
                        )
                    )

            # Force skip and trigger recovery if requested
            if force_skip:
                with self_obj._skip_lock:
                    self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)

            # Continue silently if force_skip=False
            return None

    return wrapper

# ------------------------------------------------------------
# ✅ Safe class decorator
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Decorate all class methods safely, only once."""
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
