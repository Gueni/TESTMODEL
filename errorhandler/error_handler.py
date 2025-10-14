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
        self._function_hints = {}  # function_name -> (message, force_skip)
        self._shown_messages = set()

    def add_hint(self, func_name, message):
        """Add hint for a function."""
        self._function_hints[func_name] = message

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
# ✅ Hint Decorator for Individual Functions
# ------------------------------------------------------------
def hint(message):
    """Decorator to add hints to individual functions."""
    def decorator(func):
        # Store the hint information in the function itself
        func._hint_message = message
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Store hint in instance for this execution
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
    """Wraps a function with error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        
        if not self_obj or not hasattr(self_obj, 'hint'):
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        try:
            # Call the function (which sets hints via decorator)
            result = func(*args, **kwargs)
            return result
            
        except Exception as e:
            # Get any hint that was set for this function
            custom_message = self_obj.hint.get_hint(func.__name__)
            
            # Show custom hint panel if available, otherwise show nothing
            if custom_message and not self_obj.hint.was_shown(func.__name__, custom_message):
                panel = Panel.fit(
                    f"[bold yellow]{custom_message}[/bold yellow]",
                    title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                    border_style="red",
                )
                console.print(panel)
                self_obj.hint.mark_shown(func.__name__, custom_message)
            # If no custom hint, do nothing (no Python traceback)
            
            return None

    return wrapper

# ------------------------------------------------------------
# ✅ Safe Class Decorator
# ------------------------------------------------------------
def safe_class(cls):
    """
    Decorator to make all class methods safe.
    """
    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls
        
        # Store original init
        original_init = getattr(cls, '__init__', lambda self: None)
        
        def new_init(self, *args, **kwargs):
            self.hint = ErrorHint()
            original_init(self, *args, **kwargs)
            
        cls.__init__ = new_init

        # Wrap all methods
        for attr_name in dir(cls):
            if attr_name.startswith('__'):
                continue
                
            attr_value = getattr(cls, attr_name)
            if callable(attr_value) and attr_name != '__init__':
                # Wrap with safe function
                wrapped = safe_function(attr_value)
                setattr(cls, attr_name, wrapped)

        cls._already_wrapped = True
        return cls
    
    return decorator(cls)

# ------------------------------------------------------------
# ✅ DEMONSTRATION
# ------------------------------------------------------------

@safe_class
class TestSystem:
    def __init__(self):
        self.data = []
        self.counter = 0
        print("🚀 TestSystem initialized")

    @hint("Database connection issue - will retry")
    def database_operation(self):
        print("🗄️  Database operation running...")
        self.counter += 1
        raise ConnectionError("Database connection failed")

    @hint("Network timeout - will continue")
    def network_operation(self):
        print("🌐 Network operation running...")
        self.counter += 1
        raise TimeoutError("Network request timed out")

    @hint("File not found - will use defaults")
    def file_operation(self):
        print("📁 File operation running...")
        self.counter += 1
        raise FileNotFoundError("Config file missing")

    def normal_operation(self):
        print("✅ Normal operation running...")
        self.counter += 1
        # This will show no panel since no hint is defined
        raise ValueError("This error has no custom hint")

    def successful_operation(self):
        print("🎉 Successful operation completed!")
        self.counter += 1
        return "Success"
    




def main():
    print("Starting main program...")
    
    system = TestSystem()
    
    print("\n1. Calling database_operation (has custom hint)...")
    system.database_operation()
    
    print("\n2. Calling network_operation (has custom hint)...") 
    system.network_operation()
    
    print("\n3. Calling file_operation (has custom hint)...")
    system.file_operation()
    
    print("\n4. Calling normal_operation (no custom hint)...")
    system.normal_operation()  # No panel shown
    
    print("\n5. Calling successful_operation (no error)...")
    result = system.successful_operation()
    print(f"   Result: {result}")
    
    print(f"\nFinal counter: {system.counter}")
    print("Program completed!")

if __name__ == "__main__":
    main()