# ============================================================
# error_handler_2.py
# Safe error handler with skip/recovery + Rich panel display
# Thread-safe, import-safe, loop-safe version
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# ------------------------------------------------------------
# ✅ GLOBAL SINGLETONS (one per process)
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK


# ------------------------------------------------------------
# ✅ ErrorHint class
# Stores variable hints with optional force_skip flag
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints for variables, with optional force_skip flag."""

    def __init__(self):
        self.hints = []  # [(var_name, force_skip, message)]
        self.shown_hints = set()  # to avoid repeated prints in loops

    def add(self, var, message, force_skip=False):
        """Add a hint for a variable."""
        self.hints.append((var, force_skip, message))

    def get_last(self):
        """Return the most recently added hint tuple (var, force_skip, msg)."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        """Clear stored hints."""
        self.hints.clear()
        self.shown_hints.clear()

    def should_show(self, msg):
        """Show each unique message once per run."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True


# ------------------------------------------------------------
# ✅ Recovery runner
# ------------------------------------------------------------
def _run_recovery(obj, recovery_func_name):
    """Run the recovery function safely, halting on fatal errors."""
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
# ✅ Safe function wrapper
# ------------------------------------------------------------
def safe_function(func, recovery_func_name=None):
    """Wraps class methods for safe execution with Rich panel output."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        # Handle skipping logic across threads and loops
        if getattr(self_obj, "_skip_next_steps", False):
            # Always allow recovery
            if recovery_func_name and func.__name__ == recovery_func_name:
                pass
            else:
                return None

        try:
            return func(*args, **kwargs)

        except Exception as e:
            suggestion = f"{type(e).__name__}: {e}"
            force_skip = False

            # Fetch the most recent hint if available
            if self_obj and hasattr(self_obj, "hint"):
                last_hint = self_obj.hint.get_last()
                if last_hint:
                    _, force_skip, msg = last_hint
                    suggestion = msg

            # Show panel only once per unique message
            if self_obj and hasattr(self_obj, "hint"):
                if not self_obj.hint.should_show(suggestion):
                    # already shown, skip duplicate
                    if force_skip:
                        self_obj._skip_next_steps = True
                        _run_recovery(self_obj, recovery_func_name)
                    return None

            # Thread-safe printing
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception caught[/bright_red]",
                        border_style="red",
                    )
                )

            # If force_skip=True → skip immediately and run recovery
            if self_obj and recovery_func_name and force_skip:
                self_obj._skip_next_steps = True
                _run_recovery(self_obj, recovery_func_name)

            return None

    return wrapper


# ------------------------------------------------------------
# ✅ Safe class decorator (prevents double wrapping)
# ------------------------------------------------------------
def safe_class(skip_rules):
    """Decorate all methods safely once per import."""
    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls  # prevent multiple wrapping

        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method, recovery_func_name))

        cls._already_wrapped = True
        return cls
    return decorator






from error_handler_2 import safe_class, ErrorHint

@safe_class({"step1": "step_end", "step5": "step_end"})
class MyClass:
    def __init__(self):
        self.hint = ErrorHint()

    def step1(self, a, b):
        self.hint.add("b", "b must not be zero — skip recovery", force_skip=True)
        print("Step1 executing")
        print(a / b)  # ZeroDivisionError

    def step2(self):
        print("Step2 normal")

    def step5(self):
        self.hint.add("custom", "Step5 failed — skip recovery", force_skip=True)
        raise ValueError("Intentional fail")

    def step_end(self):
        self.hint.add("recovery", "Recovery failed — halting", force_skip=False)
        print("Running recovery...")
        1 / 0

if __name__ == "__main__":
    import threading

    obj = MyClass()

    def run_loop():
        for _ in range(3):
            obj.step1(10, 0)  # triggers once
            obj.step2()
            obj.step5()

    # Run two threads to test concurrency
    t1 = threading.Thread(target=run_loop)
    t2 = threading.Thread(target=run_loop)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
