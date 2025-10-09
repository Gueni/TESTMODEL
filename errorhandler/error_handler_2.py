

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
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            self_obj = args[0] if args else None

            # Skip logic
            if getattr(self_obj, "_skip_next_steps", False):
                if recovery_func_name and func.__name__ == recovery_func_name:
                    pass
                else:
                    return None

            return func(*args, **kwargs)

        except Exception as e:
            try:
                # Only set skip flag if recovery function exists
                if self_obj and recovery_func_name:
                    self_obj._skip_next_steps = True

                # Prepare hint: check all arguments
                suggestion = None
                if self_obj and hasattr(self_obj, "hint"):
                    local_hint = self_obj.hint
                    for i, arg_name in enumerate(func.__code__.co_varnames[1:]):  # skip self
                        hint = local_hint.get(arg_name)
                        if hint:
                            suggestion = hint
                            break  # use the first hint found

                # Fallback to exception message
                if not suggestion:
                    suggestion = f"{type(e).__name__}: {str(e)}"

                # Print Rich panel
                console.print(
                    Panel.fit(f"[white]{suggestion}[/white]",
                              title="[red] Exception caught[/red]",
                              border_style="red")
                )

                # Call recovery function if defined
                if self_obj and recovery_func_name:
                    ran_flag = f"_{recovery_func_name}_ran"
                    if hasattr(self_obj, f"__orig_{recovery_func_name}") and not getattr(self_obj, ran_flag, False):
                        orig_func = getattr(self_obj, f"__orig_{recovery_func_name}")
                        orig_func()
                        setattr(self_obj, ran_flag, True)

                return None

            except Exception as inner_e:
                # Suppress any errors inside the error handler
                console.print(
                    Panel.fit(f"[white]Internal error in error handler: {inner_e}[/white]",
                              title="[red] Exception caught[/red]",
                              border_style="red")
                )
                return None

    return wrapper
