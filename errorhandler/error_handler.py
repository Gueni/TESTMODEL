# ============================================================
# enhanced_error_handler.py — Silent error handling with hints and recovery
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys

# ------------------------------------------------------------
# ✅ GLOBAL CONSOLE
# ------------------------------------------------------------
console = Console()

# ------------------------------------------------------------
# ✅ Global exception suppression
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    """Prevent Python from showing unwanted tracebacks globally."""
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ✅ Simple ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores hints for functions."""
    def __init__(self):
        self._function_hints = {}  # function_name -> (message, force_skip)
        self._shown_messages = set()

    def add_hint(self, func_name, message, force_skip=False):
        """Add hint for a function."""
        self._function_hints[func_name] = (message, force_skip)

    def get_hint(self, func_name):
        """Get hint for a function."""
        return self._function_hints.get(func_name, (None, False))

    def mark_shown(self, func_name, message):
        """Mark a message as shown."""
        self._shown_messages.add(f"{func_name}:{message}")

    def was_shown(self, func_name, message):
        """Check if message was shown."""
        return f"{func_name}:{message}" in self._shown_messages

# ------------------------------------------------------------
# ✅ Hint Decorator for Individual Functions
# ------------------------------------------------------------
def hint(message, force_skip=False):
    """Decorator to add hints to individual functions."""
    def decorator(func):
        # Store the hint information in the function itself
        func._hint_message = message
        func._hint_force_skip = force_skip
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Store hint in instance for this execution
            self_obj = args[0] if args else None
            if self_obj and hasattr(self_obj, 'hint'):
                self_obj.hint.add_hint(func.__name__, message, force_skip)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ------------------------------------------------------------
# ✅ Safe Function Wrapper
# ------------------------------------------------------------
def safe_function(func):
    """Wraps a function with error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        
        if not self_obj or not hasattr(self_obj, 'hint'):
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        # Check if we should skip execution
        if getattr(self_obj, "_skip_next_steps", False):
            return None

        try:
            # Call the function (which sets hints via decorator)
            result = func(*args, **kwargs)
            return result
            
        except Exception as e:
            # Get any hint that was set for this function
            custom_message, force_skip = self_obj.hint.get_hint(func.__name__)
            
            # Show appropriate panel
            if custom_message and not self_obj.hint.was_shown(func.__name__, custom_message):
                panel = Panel.fit(
                    f"[bold yellow]{custom_message}[/bold yellow]",
                    title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                    border_style="red",
                )
                console.print(panel)
                self_obj.hint.mark_shown(func.__name__, custom_message)
            else:
                panel = Panel.fit(
                    f"[bold yellow]{type(e).__name__}: {e}[/bold yellow]",
                    title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                    border_style="red",
                )
                console.print(panel)

            # Handle force_skip and recovery
            if force_skip:
                self_obj._skip_next_steps = True
                _run_recovery(self_obj, func.__name__)
            
            return None

    return wrapper

def _run_recovery(obj, func_name):
    """Run recovery function if defined."""
    if not hasattr(obj.__class__, "_safe_rules"):
        return

    rules = obj.__class__._safe_rules
    recovery_func_name = rules.get(func_name)
    
    if recovery_func_name and hasattr(obj, recovery_func_name):
        # Get the original unwrapped recovery function
        original_recovery_name = f"__orig_{recovery_func_name}"
        if hasattr(obj, original_recovery_name):
            recovery_func = getattr(obj, original_recovery_name)
        else:
            recovery_func = getattr(obj, recovery_func_name)
        
        try:
            # Call the recovery function directly (bypassing safe wrapper)
            # so we can handle the exception ourselves
            recovery_func()
        except Exception as e:
            # Show recovery error panel and exit
            panel = Panel.fit(
                f"[bold yellow]Recovery failed: {e}[/bold yellow]",
                title="[bright_red]Recovery Error - Exiting[/bright_red]",
                border_style="red",
            )
            console.print(panel)
            sys.exit(1)

# ------------------------------------------------------------
# ✅ Safe Class Decorator
# ------------------------------------------------------------
def safe_class(recovery_rules=None):
    """
    Decorator to make all class methods safe.
    """
    if recovery_rules is None:
        recovery_rules = {}

    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls

        cls._safe_rules = recovery_rules
        
        # Store original init
        original_init = getattr(cls, '__init__', lambda self: None)
        
        def new_init(self, *args, **kwargs):
            self.hint = ErrorHint()
            self._skip_next_steps = False
            original_init(self, *args, **kwargs)
            
        cls.__init__ = new_init

        # Wrap all methods except recovery functions
        for attr_name in dir(cls):
            if attr_name.startswith('__'):
                continue
                
            attr_value = getattr(cls, attr_name)
            if callable(attr_value) and attr_name != '__init__':
                # Store original method
                setattr(cls, f"__orig_{attr_name}", attr_value)
                # Wrap with safe function
                wrapped = safe_function(attr_value)
                setattr(cls, attr_name, wrapped)

        cls._already_wrapped = True
        return cls
    
    return decorator

# ------------------------------------------------------------
# ✅ DEMONSTRATION
# ------------------------------------------------------------
if __name__ == "__main__":
    
    @safe_class({
        "critical_operation": "emergency_recovery"
    })
    class TestSystem:
        def __init__(self):
            self.data = []
            self.counter = 0

        @hint("Database connection issue - will retry", force_skip=False)
        def database_operation(self):
            self.counter += 1
            raise ConnectionError("Database connection failed")

        @hint("Network timeout - will continue", force_skip=False)
        def network_operation(self):
            self.counter += 1
            raise TimeoutError("Network request timed out")

        @hint("CRITICAL: System failure! Entering recovery mode.", force_skip=True)
        def critical_operation(self):
            self.counter += 1
            raise RuntimeError("Critical system failure!")

        @hint("File not found - will use defaults", force_skip=False)
        def file_operation(self):
            self.counter += 1
            raise FileNotFoundError("Config file missing")

        def should_be_skipped(self):
            self.counter += 1

        def emergency_recovery(self):
            # This will be called directly and show its error
            raise ValueError("Recovery database is unavailable!")

    # Clean execution
    system = TestSystem()
    
    system.database_operation()
    system.network_operation()
    system.critical_operation()  # This should trigger recovery and exit
    
    # These should not execute
    system.file_operation()
    system.should_be_skipped()