# ============================================================
# enhanced_error_handler.py — Silent error handling with hints and recovery
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading
import inspect

# ------------------------------------------------------------
# ✅ MULTITHREAD FLAG
# ------------------------------------------------------------
USE_MULTITHREAD = False

# ------------------------------------------------------------
# ✅ GLOBAL CONSOLE + LOCK
# ------------------------------------------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()

if "CONSOLE_LOCK" not in globals() and USE_MULTITHREAD:
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK if USE_MULTITHREAD else None

# ------------------------------------------------------------
# ✅ Global exception suppression
# ------------------------------------------------------------
def _silent_excepthook(exc_type, exc_value, exc_traceback):
    """Prevent Python from showing unwanted tracebacks globally."""
    pass

sys.excepthook = _silent_excepthook

# ------------------------------------------------------------
# ✅ Enhanced ErrorHint class
# ------------------------------------------------------------
class ErrorHint:
    """Stores variable hints for exceptions and warnings with context tracking."""
    def __init__(self):
        self.hints = []
        self.shown_hints = set()

    def add(self, var, message, force_skip=False):
        """
        Add a hint for a variable with automatic function context detection.
        """
        # Get calling function name for context
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back
            func_name = caller_frame.f_code.co_name
            self.hints.append((var, force_skip, message, func_name))
        finally:
            del frame

    def get_hint_for_function(self, func_name):
        """Get the most recent hint for a specific function."""
        for var, force_skip, message, hint_func in reversed(self.hints):
            if hint_func == func_name:
                return (var, force_skip, message)
        return None

    def get_last(self):
        """Return the last added hint."""
        return self.hints[-1] if self.hints else None

    def clear(self):
        """Clear all hints and printed records."""
        self.hints.clear()
        self.shown_hints.clear()

    def should_show(self, msg):
        """Prevent duplicate messages."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

# ------------------------------------------------------------
# ✅ Recovery System
# ------------------------------------------------------------
class RecoverySystem:
    """Manages recovery functions and execution flow."""
    
    @staticmethod
    def run_recovery(obj, triggering_func_name):
        """
        Execute recovery for a specific function failure.
        Returns True if recovery was successful, False otherwise.
        """
        if not hasattr(obj.__class__, "_safe_rules"):
            return False

        rules = obj.__class__._safe_rules
        recovery_func_name = rules.get(triggering_func_name)
        
        # If no specific recovery, check for global recovery
        if not recovery_func_name:
            recovery_func_name = rules.get("__global__")
        
        if not recovery_func_name or not hasattr(obj, recovery_func_name):
            RecoverySystem._show_info(f"No recovery function found for {triggering_func_name}")
            return False

        # Prevent infinite recursion
        ran_flag = f"_{recovery_func_name}_ran"
        if getattr(obj, ran_flag, False):
            RecoverySystem._show_info(f"Recovery {recovery_func_name} already ran")
            return True

        try:
            # RecoverySystem._show_info(f"🔄 Executing recovery: {recovery_func_name}")
            setattr(obj, ran_flag, True)
            recovery_func = getattr(obj, recovery_func_name)
            recovery_func()
            
            # Set global skip to jump over remaining functions
            if USE_MULTITHREAD:
                with getattr(obj, "_skip_lock", threading.Lock()):
                    obj._skip_next_steps = True
            else:
                obj._skip_next_steps = True
                
            # RecoverySystem._show_success(f"✅ Recovery {recovery_func_name} completed successfully")
            return True
            
        except Exception as e:
            # Recovery itself failed - show error and halt completely
            hint_msg = RecoverySystem._get_recovery_error_message(obj, e)
            RecoverySystem._show_recovery_failure(hint_msg)
            return False

    @staticmethod
    def _get_recovery_error_message(obj, exception):
        """Get meaningful message for recovery failure."""
        if hasattr(obj, "hint"):
            last_hint = obj.hint.get_last()
            if last_hint:
                return last_hint[2]  # Return the message part
        return f"Recovery failed: {type(exception).__name__}: {exception}"

    @staticmethod
    def _show_recovery_failure(message):
        """Display recovery failure panel."""
        panel = Panel.fit(
            f"[bold yellow]{message}[/bold yellow]",
            title="[bright_red]CRITICAL: Recovery Failed - Stopping Execution[/bright_red]",
            border_style="red",
        )
        
        if USE_MULTITHREAD and console_lock:
            with console_lock:
                console.print(panel)
        else:
            console.print(panel)

    @staticmethod
    def _show_info(message):
        """Show informational message."""
        if USE_MULTITHREAD and console_lock:
            with console_lock:
                console.print(f"[blue]ℹ️ {message}[/blue]")
        else:
            console.print(f"[blue]ℹ️ {message}[/blue]")

    @staticmethod
    def _show_success(message):
        """Show success message."""
        if USE_MULTITHREAD and console_lock:
            with console_lock:
                console.print(f"[green]{message}[/green]")
        else:
            console.print(f"[green]{message}[/green]")

# ------------------------------------------------------------
# ✅ Enhanced Safe Function Wrapper
# ------------------------------------------------------------
def safe_function(func):
    """Wraps a function with comprehensive error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args and hasattr(args[0], 'hint') else None

        # Handle non-class functions
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        # Initialize threading support if needed
        if USE_MULTITHREAD and not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        # Check if we should skip execution
        if getattr(self_obj, "_skip_next_steps", False):
            ErrorHandler._show_skipped(func.__name__)
            return None

        try:
            return func(*args, **kwargs)
            
        except Exception as e:
            return ErrorHandler.handle_exception(self_obj, func, e)

    return wrapper

class ErrorHandler:
    """Centralized exception handling logic."""
    
    @staticmethod
    def handle_exception(obj, func, exception):
        """Process an exception and determine the appropriate response."""
        func_name = func.__name__
        hint_info = ErrorHandler._get_hint_info(obj, func_name, exception)
        message, force_skip = hint_info

        # Show error panel if appropriate
        if ErrorHandler._should_show_panel(obj, message):
            ErrorHandler._show_error_panel(func_name, message)

        # Handle recovery if needed
        if force_skip:
            ErrorHandler._trigger_recovery(obj, func_name)
            
        return None

    @staticmethod
    def _get_hint_info(obj, func_name, exception):
        """Extract hint information for the current context."""
        default_msg = f"{type(exception).__name__}: {exception}"
        force_skip = False

        if hasattr(obj, "hint"):
            # Try to get hint for current function
            specific_hint = obj.hint.get_hint_for_function(func_name)
            if specific_hint:
                _, force_skip, msg = specific_hint
                return msg, force_skip
            
            # Fall back to last hint
            last_hint = obj.hint.get_last()
            if last_hint:
                _, force_skip, msg, _ = last_hint
                return msg, force_skip

        return default_msg, force_skip

    @staticmethod
    def _should_show_panel(obj, message):
        """Determine if we should display an error panel."""
        return hasattr(obj, "hint") and obj.hint.should_show(message)

    @staticmethod
    def _show_error_panel(func_name, message):
        """Display the error panel."""
        panel = Panel.fit(
            f"[bold yellow]{message}[/bold yellow]",
            title=f"[bright_red]Exception in {func_name}[/bright_red]",
            border_style="red",
        )
        
        if USE_MULTITHREAD and console_lock:
            with console_lock:
                console.print(panel)
        else:
            console.print(panel)

    @staticmethod
    def _show_skipped(func_name):
        """Show that a function was skipped."""
        if USE_MULTITHREAD and console_lock:
            with console_lock:
                # console.print(f"[yellow]⏭️ {func_name} skipped due to recovery mode[/yellow]")
                pass
        else:
            # console.print(f"[yellow]⏭️ {func_name} skipped due to recovery mode[/yellow]")
            pass

    @staticmethod
    def _trigger_recovery(obj, func_name):
        """Initiate recovery process for critical errors."""
        if USE_MULTITHREAD:
            with getattr(obj, "_skip_lock", threading.Lock()):
                obj._skip_next_steps = True
        else:
            obj._skip_next_steps = True
            
        RecoverySystem.run_recovery(obj, func_name)

# ------------------------------------------------------------
# ✅ Enhanced Safe Class Decorator
# ------------------------------------------------------------
def safe_class(recovery_rules=None):
    """
    Decorator to make all class methods safe.
    
    Args:
        recovery_rules: Dict mapping {method_name: recovery_method}
                        Use "__global__" for a catch-all recovery
    """
    if recovery_rules is None:
        recovery_rules = {}

    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls

        cls._safe_rules = recovery_rules
        
        # Add ErrorHint instance to class
        original_init = cls.__init__ if hasattr(cls, '__init__') else lambda self: None
        
        def new_init(self, *args, **kwargs):
            self.hint = ErrorHint()
            if USE_MULTITHREAD and not hasattr(self, "_skip_lock"):
                self._skip_lock = threading.Lock()
            self._skip_next_steps = False
            original_init(self, *args, **kwargs)
            
        cls.__init__ = new_init

        # Wrap all callable methods
        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__") and name != "__init__":
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method))

        cls._already_wrapped = True
        return cls
    return decorator

# ------------------------------------------------------------
# ✅ DEMONSTRATION - Fixed to show the complete flow
# ------------------------------------------------------------
if __name__ == "__main__":
    
    @safe_class({"func_1": "func_5"})
    class ExampleSystem:
        def __init__(self):
            self.hint = ErrorHint()

        def func_1(self):
            self.hint.add("data", "This is a normal hint - will show panel but continue", force_skip=True)
            print("✅ func_1")
            raise ValueError("Something went terribly wrong in func_2!")
            
        def func_2(self):
            self.hint.add("critical_var", "This will trigger recovery")
            print("🔥 func_2")
            
        def func_3(self):
            print("📝 func_3")
            
        def func_4(self):
            print("❌ func_4")
            
        def func_5(self):
            print("🛡️ func_5")
            
    
    system = ExampleSystem()
    
    system.func_1()
    system.func_2()
    system.func_3()
    system.func_4()
    system.func_5()
    
   