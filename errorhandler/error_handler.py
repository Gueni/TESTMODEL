# ============================================================ 
# enhanced_error_handler.py — Simple error handling with hints
# ============================================================
import sys, traceback
falg = False
def suppress_tracebacks_to_file(exc_type, exc_value, exc_traceback):
    """Redirect unhandled (not user-caught) exceptions to file, not console."""
    with open("error_log.log", "w", encoding="utf-8") as f:
        f.write("=== Unhandled Exception ===\n")
        f.write("*" * 80 + "\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        f.write("*" * 80 + "\n")
        f.write("\n")

sys.excepthook = suppress_tracebacks_to_file

from functools import wraps
import sys
from rich.console import Console
from rich.panel import Panel

# ------------------------------------------------------------
# ✅ GLOBAL CONSOLE
# ------------------------------------------------------------
console = Console()

# ------------------------------------------------------------
# ✅ Simple ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores and manages hint messages for functions."""
    def __init__(self):
        self._function_hints = {}  # function_name -> message
        self._shown_messages = set()

    def add_hint(self, func_name, message):
        """Add hint for a function."""
        self._function_hints[func_name] = message

    def get_hint(self, func_name):
        """Get hint message for a function."""
        return self._function_hints.get(func_name)

    def mark_shown(self, func_name, message):
        """Mark a message as shown."""
        self._shown_messages.add(f"{func_name}:{message}")

    def was_shown(self, func_name, message):
        """Check if message was already shown."""
        return f"{func_name}:{message}" in self._shown_messages


# ------------------------------------------------------------
# ✅ Hint Decorator for Individual Functions
# ------------------------------------------------------------
def hint(message):
    """Decorator to attach a user-friendly hint to a function."""
    def decorator(func):
        func._hint_message = message

        @wraps(func)
        def wrapper(*args, **kwargs):
            self_obj = args[0] if args else None
            if self_obj and hasattr(self_obj, 'hint'):
                self_obj.hint.add_hint(func.__name__, message)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ------------------------------------------------------------
# ✅ Safe Function Wrapper
# ------------------------------------------------------------
def safe_function(func):
    """Wraps a function with error handling and hint display."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        
        self.flag =flag

        if not self_obj or not hasattr(self_obj, 'hint'):
            return func(*args, **kwargs)

        try:
            return func(*args, **kwargs)

        except Exception as e:
            custom_message = self_obj.hint.get_hint(func.__name__)

            # Always show Rich panel for user clarity
            if custom_message and not self_obj.hint.was_shown(func.__name__, custom_message):
                console.print(Panel.fit(
                    f"[bold yellow]{custom_message}[/bold yellow]",
                    title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                    border_style="red",
                ))
                self_obj.hint.mark_shown(func.__name__, custom_message)
            else:
                console.print(Panel.fit(
                    f"[bold yellow]{type(e).__name__}: {e}[/bold yellow]",
                    title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                    border_style="red",
                ))

            # 🔹 Always log the error quietly
            with open("error_log.log", "a", encoding="utf-8") as f:
                traceback.print_exception(type(e), e, e.__traceback__, file=f)
                f.write("\n")

            # 🔹 If we’re inside a user try/except, re-raise
            # otherwise, swallow it to keep program running
            exc_type, _, _ = sys.exc_info()
            if exc_type and flag :
                # inside a user try/except, re-raise normally
                raise
            else:
                # outside try/except -> swallow safely
                return None

    return wrapper


# ------------------------------------------------------------
# ✅ Safe Class Decorator
# ------------------------------------------------------------
def safe_class():
    """Decorator to make all methods in a class safe with hint/error display."""
    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls

        # Patch __init__ to include the hint manager
        original_init = getattr(cls, '__init__', lambda self: None)
        def new_init(self, *args, **kwargs):
            self.hint = ErrorHint()
            original_init(self, *args, **kwargs)
        cls.__init__ = new_init

        # Wrap all methods (except __init__)
        for attr_name in dir(cls):
            if attr_name.startswith('__'):
                continue

            attr_value = getattr(cls, attr_name)
            if callable(attr_value):
                setattr(cls, f"__orig_{attr_name}", attr_value)
                setattr(cls, attr_name, safe_function(attr_value))

        cls._already_wrapped = True
        return cls
    return decorator


# ============================================================
@safe_class()
class TestSystem:
    def __init__(self):
        self.data = []
        self.counter = 0
        print("🚀 TestSystem initialized")

    @hint("Database connection issue - will retry")
    def database_operation(self):
        self.counter += 1
        raise ConnectionError("Database connection failed")

    @hint("Network timeout - will continue")
    def network_operation(self):
        self.counter += 1
        raise TimeoutError("Network request timed out")

    @hint("CRITICAL: System failure! Entering recovery mode.")
    def critical_operation(self):
        self.counter += 1
        raise RuntimeError("Critical system failure!")

    @hint("File not found - will use defaults")
    def file_operation(self):
        self.counter += 1
        raise FileNotFoundError("Config file missing")

    def should_be_skipped(self):
        self.counter += 1
        print("✅ This runs normally now (no skip logic).")

    def emergency_recovery(self):
        raise ValueError("Recovery database is unavailable!")


def main():
    system = TestSystem()

    try:
        system.critical_operation()

    except Exception as e:
        print("\n--- Emergency Recovery Triggered ---")
        system.emergency_recovery()
        sys.exit(1)

    for i in range(2):
        print(f"\n--- Iteration {i+1} ---")
        system.database_operation()

        system.network_operation()

        system.critical_operation()

        system.file_operation()

        system.should_be_skipped()


if __name__ == "__main__":
    main()
