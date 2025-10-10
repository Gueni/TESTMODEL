# ============================================================
# error_handler_improved.py - Enhanced version
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading
import inspect

# -------------------- GLOBAL CONSOLE ------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

# -------------------- ERROR HINT ----------------------------
class ErrorHint:
    """Stores hints for functions with force_skip flag."""
    def __init__(self):
        self.hints = {}  # func_name -> (force_skip, message)
        self.shown_hints = set()

    def add(self, message, force_skip=False):
        """Add a hint. Associated with the function calling this add()."""
        func_name = inspect.stack()[1].function
        self.hints[func_name] = (force_skip, message)

    def get_for_func(self, func_name):
        """Return hint for the given function."""
        if func_name in self.hints:
            force_skip, message = self.hints[func_name]
            return func_name, force_skip, message
        return None

    def should_show(self, msg):
        """Prevent duplicate hint panels."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

    def clear(self):
        self.hints.clear()
        self.shown_hints.clear()

# -------------------- RECOVERY RUNNER -----------------------
def _run_recovery(obj, current_func_name):
    """Call recovery function safely. Exit cleanly if recovery fails."""
    recovery_func_name = None
    
    # Get recovery function from skip rules
    if hasattr(obj.__class__, "_safe_rules"):
        rules = obj.__class__._safe_rules
        recovery_func_name = rules.get(current_func_name)
        
        # If no specific rule, try to find a default recovery
        if not recovery_func_name and rules:
            # Use the first recovery function as default
            recovery_func_name = next(iter(rules.values()), None)

    if not recovery_func_name:
        return

    # Check if recovery function exists and hasn't run
    recovery_func = getattr(obj, recovery_func_name, None)
    if not recovery_func:
        return

    ran_flag = f"_{recovery_func_name}_ran"
    
    if not getattr(obj, ran_flag, False):
        try:
            recovery_func()
            setattr(obj, ran_flag, True)
        except Exception:
            # Show panel for recovery failure
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_for_func(recovery_func_name)
                if last_hint:
                    _, _, suggestion = last_hint
            if not suggestion:
                suggestion = f"Exception in recovery function {recovery_func_name}"
            
            with console_lock:
                if obj.hint.should_show(suggestion):
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{suggestion}[/bold yellow]",
                            title="[bright_red]Exception in recovery — HALT[/bright_red]",
                            border_style="red",
                        )
                    )
            sys.exit(0)  # clean exit

# -------------------- SAFE FUNCTION WRAPPER -----------------
def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Handle both class methods and standalone functions
        self_obj = args[0] if args and hasattr(args[0], 'hint') else None
        
        # For standalone functions without class context
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                # For standalone functions, we can't show hints without ErrorHint instance
                return None

        # Initialize skip lock if not exists
        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        # Check skip flag - if set, skip this function
        with self_obj._skip_lock:
            if getattr(self_obj, "_skip_next_steps", False):
                return None

        # Check for function-specific hint
        force_skip = False
        func_hint = None
        hint_data = self_obj.hint.get_for_func(func.__name__)
        if hint_data:
            _, force_skip, func_hint = hint_data

        # If force_skip is True, jump immediately to recovery
        if force_skip:
            with self_obj._skip_lock:
                self_obj._skip_next_steps = True
            
            if func_hint and self_obj.hint.should_show(func_hint):
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{func_hint}[/bold yellow]",
                            title=f"[bright_red]Forced skip in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )
            _run_recovery(self_obj, func.__name__)
            return None

        # Run function normally
        try:
            return func(*args, **kwargs)
        except Exception:
            # Show panel for the hint (if any)
            if func_hint and self_obj.hint.should_show(func_hint):
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{func_hint}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )
            return None

    return wrapper

# -------------------- SAFE CLASS DECORATOR -----------------
def safe_class(skip_rules=None):
    """Wrap all class methods with safe_function."""
    if skip_rules is None:
        skip_rules = {}
    
    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls

        cls._safe_rules = skip_rules

        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                # Store original method
                setattr(cls, f"__orig_{name}", method)
                # Replace with wrapped version
                setattr(cls, name, safe_function(method))

        cls._already_wrapped = True
        return cls
    return decorator



