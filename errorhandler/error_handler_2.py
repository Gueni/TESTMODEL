

from rich.console import Console
from rich.panel import Panel
from functools import wraps

# Initialize a Rich console object for pretty printing panels
console = Console()

class ErrorHint:
    """
    Stores custom suggestions per variable.
    These hints can be used to provide a clear message when exceptions occur.
    """
    def __init__(self):
        self.hints = {}  # Dictionary to store variable name -> suggestion mapping

    def add(self, var_name, suggestion):
        """Add a custom suggestion for a specific variable."""
        self.hints[var_name] = suggestion

    def get(self, var_name):
        """Retrieve the custom suggestion for a variable, if any."""
        return self.hints.get(var_name, None) 

def safe_class(skip_map: dict):
    """
    Class decorator that wraps all class methods with skip-on-error logic.

    Parameters:
    skip_map : dict
        Mapping of method name -> recovery method name.
        Example: {"step1": "step_end"} 
        If 'step1' fails, it will automatically call 'step_end' and skip all intermediate steps.
    """
    def decorator(cls):
    
        # Iterate over a list of class attributes to avoid RuntimeError 
        # if the dictionary changes size during iteration
        for name, func in list(cls.__dict__.items()):

            # Only wrap callable methods that are not special methods
            if callable(func) and not name.startswith("__"):

                # Determine the recovery function for this method, if any
                recovery_func = skip_map.get(name)

                # Store the original function so it can be called directly later
                setattr(cls, f"__orig_{name}", func)

                # Replace the method with the wrapped version
                setattr(cls, name, safe_function(func, recovery_func, cls))

        return cls
    
    return decorator

def safe_function(func, recovery_func_name=None, cls=None):
    """
    Function wrapper that implements skip-on-error logic.

    Parameters:
    func : callable
        Original method to wrap
    recovery_func_name : str or None
        Name of the recovery method to run if this method fails
    cls : type
        The class this function belongs to (not used in wrapper directly)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the 'self' object from the arguments
        self_obj = args[0] if args else None

        # If skip flag is set, skip all methods except the designated recovery function
        if getattr(self_obj, "_skip_next_steps", False):
            # Check if this is the recovery function
            if recovery_func_name and func.__name__ == recovery_func_name:
                # Allow recovery function to run even when skip flag is active
                pass
            else:
                # If this is not the recovery function, skip it entirely
                return None
        try:
            # Call the original function normally
            return func(*args, **kwargs)
        
        except Exception as e:
            # Only set skip flag if this method has a recovery function defined
            if self_obj and recovery_func_name:
                self_obj._skip_next_steps = True

            # Prepare a suggestion to show in the Rich panel
            suggestion = None
            # Check if the class has a custom hint dictionary
            if self_obj and hasattr(self_obj, "hint"):
                local_hint = self_obj.hint

                # Try to match the first argument of the function to a variable hint
                arg_name = func.__code__.co_varnames[1] if len(func.__code__.co_varnames) > 1 else None

                if arg_name:
                    suggestion = local_hint.get(arg_name)

            # If no custom hint exists, fallback to the exception type and message
            if not suggestion:
                suggestion = f"{type(e).__name__}: {str(e)}"

            # Display the exception/hint in a Rich panel
            console.print(Panel.fit(f"[white]{suggestion}[/white]",title="[red] Exception caught[/red]",border_style="red"))

            # Call the recovery function if defined and hasn't been run yet
            if self_obj and recovery_func_name:

                # Check if the recovery function has been run before
                ran_flag = f"_{recovery_func_name}_ran"

                # Check if the recovery function exists and hasn't been run yet
                if hasattr(self_obj, f"__orig_{recovery_func_name}") and not getattr(self_obj, ran_flag, False):

                    # Call the original unwrapped recovery function
                    orig_func = getattr(self_obj, f"__orig_{recovery_func_name}")

                    # Call the original unwrapped recovery function
                    orig_func()

                    # Mark recovery as run so it doesn't run multiple times
                    setattr(self_obj, ran_flag, True)

            return None  # Ensure wrapper always returns None on exception
    return wrapper
