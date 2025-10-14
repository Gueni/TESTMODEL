# ============================================================
# enhanced_error_handler.py — Silent error handling with hints only
# ============================================================

from functools import wraps
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
    """Stores hints for functions."""
    def __init__(self):
        self._function_hints = {}  # function_name -> message
        self._shown_messages = set()

    def add(self, message):
        """Add hint for the current function."""
        import inspect
        # Get the calling function name
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back.f_back  # Go back through wrapper
            func_name = caller_frame.f_code.co_name
            self._function_hints[func_name] = message
        finally:
            del frame

    def get_hint(self, func_name):
        """Get hint for a function."""
        return self._function_hints.get(func_name, None)

    def mark_shown(self, func_name, message):
        """Mark a message as shown."""
        self._shown_messages.add(f"{func_name}:{message}")

    def was_shown(self, func_name, message):
        """Check if message was shown."""
        return f"{func_name}:{message}" in self._shown_messages

# ------------------------------------------------------------
# ✅ Safe Function Wrapper
# ------------------------------------------------------------
def safe_function(func):
    """Wraps a function with error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        
        if not self_obj or not hasattr(self_obj, 'hint'):
            # For non-class functions or classes without hint, behave normally
            return func(*args, **kwargs)

        try:
            # Call the function
            result = func(*args, **kwargs)
            return result
            
        except Exception as e:
            # Get any hint that was set for this function
            custom_message = self_obj.hint.get_hint(func.__name__)
            
            # Show custom hint panel if available
            if custom_message and not self_obj.hint.was_shown(func.__name__, custom_message):
                panel = Panel.fit(
                    f"[bold yellow]{custom_message}[/bold yellow]",
                    title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                    border_style="red",
                )
                console.print(panel)
                self_obj.hint.mark_shown(func.__name__, custom_message)
                # Return None to suppress the exception for functions with hints
                return None
            else:
                # If no custom hint, re-raise the exception so other try/except can catch it
                raise
            
    return wrapper

# ------------------------------------------------------------
# ✅ Safe Class Decorator (wraps only once)
# ------------------------------------------------------------
def safe_class(cls):
    """
    Decorator to make all class methods safe.
    Wraps only once to prevent multiple wrapping.
    """
    if getattr(cls, "_already_wrapped", False):
        return cls
    
    # Store original init
    original_init = getattr(cls, '__init__', lambda self: None)
    
    def new_init(self, *args, **kwargs):
        self.hint = ErrorHint()
        original_init(self, *args, **kwargs)
        
    cls.__init__ = new_init

    # Wrap all methods only once
    for attr_name in dir(cls):
        if attr_name.startswith('__'):
            continue
            
        attr_value = getattr(cls, attr_name)
        if callable(attr_value) and attr_name != '__init__':
            # Only wrap if not already wrapped
            if not hasattr(attr_value, '_wrapped'):
                wrapped = safe_function(attr_value)
                wrapped._wrapped = True  # Mark as wrapped
                setattr(cls, attr_name, wrapped)

    cls._already_wrapped = True
    return cls