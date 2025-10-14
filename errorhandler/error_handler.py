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
# ✅ Hint Decorator
# ------------------------------------------------------------
def hint(message):
    """Decorator to add hints to functions."""
    def decorator(func):
        func._hint_message = message
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            self_obj = args[0] if args else None
            
            if not self_obj or not hasattr(self_obj, 'hint'):
                # For non-class functions, behave normally
                return func(*args, **kwargs)
                
            try:
                # Store the hint for this function
                self_obj.hint._current_hint = message
                self_obj.hint._current_function = func.__name__
                
                # Call the function
                result = func(*args, **kwargs)
                return result
                
            except Exception as e:
                # Check if this function has a hint
                if hasattr(self_obj.hint, '_current_hint') and self_obj.hint._current_function == func.__name__:
                    custom_message = self_obj.hint._current_hint
                    
                    # Show panel for functions with hints
                    panel = Panel.fit(
                        f"[bold yellow]{custom_message}[/bold yellow]",
                        title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                        border_style="red",
                    )
                    console.print(panel)
                    
                    # Clear the current hint
                    self_obj.hint._current_hint = None
                    self_obj.hint._current_function = None
                    
                    # Return None to suppress exception
                    return None
                else:
                    # No hint - re-raise for other try/except blocks
                    raise
                    
        return wrapper
    return decorator

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
    
    # Add hint attribute to class
    original_init = getattr(cls, '__init__', lambda self: None)
    
    def new_init(self, *args, **kwargs):
        # Create simple hint storage
        self.hint = type('SimpleHint', (), {
            '_current_hint': None,
            '_current_function': None
        })()
        original_init(self, *args, **kwargs)
        
    cls.__init__ = new_init

    # Apply hint decorator to methods that have it
    for attr_name in dir(cls):
        if attr_name.startswith('__'):
            continue
            
        attr_value = getattr(cls, attr_name)
        if callable(attr_value) and attr_name != '__init__':
            # If method has _hint_message, it already has @hint decorator
            if hasattr(attr_value, '_hint_message'):
                # Only wrap if not already wrapped
                if not hasattr(attr_value, '_wrapped'):
                    # Re-apply the hint decorator to ensure it's wrapped
                    hinted_func = hint(attr_value._hint_message)(attr_value)
                    hinted_func._wrapped = True
                    setattr(cls, attr_name, hinted_func)

    cls._already_wrapped = True
    return cls