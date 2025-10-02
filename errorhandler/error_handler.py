
#?------------------------------------------------------------------------------------------------
import sys
import traceback
from functools import wraps
from rich.console import Console
from rich.panel import Panel
import inspect
#?------------------------------------------------------------------------------------------------
console = Console()  # Rich console object for pretty printing panels
#?------------------------------------------------------------------------------------------------
class ErrorHint:
    """
    Stores custom suggestions per variable.Or add variable-specific hints which will be used by the
    error handler to provide custom suggestions when exceptions occur.
    """
    def __init__(self):
        # Dictionary to store variable as suggestion mapping
        self.hints      = {} 

    def add(self, var_name, suggestion):
        """
        Add a custom suggestion for a specific variable.

        Args:
            var_name    (str): Name of the variable.
            suggestion  (str): Suggestion message to display if this variable causes an error.
        """
        self.hints[var_name] = suggestion

    def get(self, var_name):
        """
        Retrieve the custom suggestion for a variable, if any.

        Args    :
                     var_name (str): Name of the variable.

        Returns :    str or None: The suggestion message, or None if not set.
        """
        return self.hints.get(var_name, None)
#?------------------------------------------------------------------------------------------------
def safe_class(cls):
    """
    Decorator to automatically wrap all methods of a class with the safe_function
    wrapper, providing automatic Rich error panels and hint handling.

    Args    :   cls (type)  : The class to wrap.

    Returns :   type        : The same class with all callable methods wrapped.
    """
    for attr_name, attr_value in cls.__dict__.items():
        # Wrap all callable methods, excluding dunder methods (methods with double underscores like __init__ ...) 
        if callable(attr_value) and not attr_name.startswith("__"): setattr(cls, attr_name, safe_function(attr_value))
    return cls
#?------------------------------------------------------------------------------------------------
def safe_function(func):
    """
    Wrap a function to catch exceptions, analyze them, and display
    a clean Rich panel with error information, cause, and suggestions.
    Excludes the error handler's own frames from the stack trace.

    Args    :   func (callable) : The function to wrap.

    Returns :   callable        : The wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Call the original function
            return func(*args, **kwargs)
        
        except Exception as e:

            # Capture exception info and extract exception name
            exc_type, exc_value, tb = sys.exc_info()
            exc_name                = exc_type.__name__

            # Inspect function signature and arguments
            sig         = inspect.signature(func)
            bound_args  = sig.bind(*args, **kwargs)

            # Inspect function signature if self is used or not.
            sig             = inspect.signature(func)
            bound_args      = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments       = bound_args.arguments

            # Determine if there is a custom hint: function-level
            local_hint  = None
            frame       = tb.tb_frame
            local_vars  = frame.f_locals

            # Check function-level hint first
            if "hint" in local_vars and isinstance(local_vars["hint"], ErrorHint):          local_hint  = local_vars["hint"]

            # If method, check self.hint
            elif args:
                first_arg   = args[0]
                if hasattr(first_arg, "hint") and isinstance(first_arg.hint, ErrorHint):    local_hint = first_arg.hint

            # Default fall back cause & suggestion
            cause_msg       = "Could not automatically determine the cause."
            suggestion_msg  = "Check variable values and types."

            # Determine if this is a method with self
            arg_items = list(arguments.items())
            if args and hasattr(args[0], "__class__"):  # first arg looks like 'self'
                arg_items_to_check = arg_items[1:]      # skip 'self'
            else:
                arg_items_to_check = arg_items           # normal function

            # --- Basic automatic analysis for common errors (max 15 cases) ---
            # Handle ZeroDivisionError: Occurs when dividing by zero
            if exc_name == "ZeroDivisionError":
                for name, val in arg_items_to_check:
                    if isinstance(val, (int, float)) and val == 0:
                        cause_msg = f"The variable '{name}' is zero."
                        if local_hint and local_hint.get(name):
                            suggestion_msg = local_hint.get(name)
                        else:
                            suggestion_msg = f"Ensure '{name}' is not zero before division."
                        break

            # Handle FileNotFoundError: Occurs when trying to access a file that doesn't exist
            elif exc_name == "FileNotFoundError":
                filename = getattr(exc_value, 'filename', None)
                if filename:
                    cause_msg = f"The file '{filename}' does not exist."
                    if local_hint and local_hint.get("filename"):
                        suggestion_msg = local_hint.get("filename")
                    else:
                        suggestion_msg = f"Ensure the file '{filename}' exists in the correct path."

            # Handle TypeError: Occurs when an operation uses wrong data type
            elif exc_name == "TypeError":
                for name, val in arg_items_to_check:
                    cause_msg = f"Variable '{name}' has wrong type: {type(val).__name__}."
                    if local_hint and local_hint.get(name):
                        suggestion_msg = local_hint.get(name)
                    else:
                        suggestion_msg = f"Ensure '{name}' has the correct type for this operation."
                    break

            # Handle ValueError: Occurs when a function receives argument of right type but inappropriate value
            elif exc_name == "ValueError":
                for name, val in arg_items_to_check:
                    cause_msg = f"Variable '{name}' has invalid value: {val}."
                    if local_hint and local_hint.get(name):
                        suggestion_msg = local_hint.get(name)
                    else:
                        suggestion_msg = f"Ensure '{name}' has a valid value."
                    break

            # Handle IndexError: Occurs when trying to access list/sequence with invalid index
            elif exc_name == "IndexError":
                for name, val in arg_items_to_check:
                    cause_msg = f"Index used in '{name}' is out of range."
                    if local_hint and local_hint.get(name):
                        suggestion_msg = local_hint.get(name)
                    else:
                        suggestion_msg = f"Check that the index for '{name}' is within valid range."
                    break

            # Handle KeyError: Occurs when dictionary key is not found
            elif exc_name == "KeyError":
                key = getattr(exc_value, 'args', [None])[0]
                cause_msg = f"Dictionary key '{key}' not found."
                if local_hint and local_hint.get(str(key)):
                    suggestion_msg = local_hint.get(str(key))
                else:
                    suggestion_msg = f"Check that the key '{key}' exists before accessing."

            # Handle AttributeError: Occurs when object doesn't have the requested attribute
            elif exc_name == "AttributeError":
                attr = getattr(exc_value, 'args', [None])[0]
                cause_msg = f"Attribute error: {attr}."
                if local_hint and local_hint.get(str(attr)):
                    suggestion_msg = local_hint.get(str(attr))
                else:
                    suggestion_msg = f"Ensure the object has the required attribute."

            # Handle NameError: Occurs when variable is not defined in current scope
            elif exc_name == "NameError":
                var_name = getattr(exc_value, 'name', None)
                cause_msg = f"The variable '{var_name}' is not defined."
                if local_hint and local_hint.get(var_name):
                    suggestion_msg = local_hint.get(var_name)
                else:
                    suggestion_msg = f"Define '{var_name}' before using it."

            # Handle ImportError: Occurs when import statement fails to find module
            elif exc_name == "ImportError":
                module = getattr(exc_value, 'name', None)
                cause_msg = f"Cannot import module '{module}'."
                if local_hint and local_hint.get(module):
                    suggestion_msg = local_hint.get(module)
                else:
                    suggestion_msg = f"Install or check the module '{module}'."

            # Handle ModuleNotFoundError: Specific case of ImportError for missing modules
            elif exc_name == "ModuleNotFoundError":
                module = getattr(exc_value, 'name', None)
                cause_msg = f"Module '{module}' not found."
                if local_hint and local_hint.get(module):
                    suggestion_msg = local_hint.get(module)
                else:
                    suggestion_msg = f"Ensure '{module}' is installed and importable."

            # Handle OverflowError: Occurs when numeric calculation exceeds maximum representable value
            elif exc_name == "OverflowError":
                cause_msg = "A numeric calculation exceeded the maximum limit."
                if local_hint:
                    suggestion_msg = local_hint.get("overflow") or "Check numeric ranges and calculations."
                else:
                    suggestion_msg = "Check numeric ranges and calculations."

            # Handle MemoryError: Occurs when operation runs out of memory
            elif exc_name == "MemoryError":
                cause_msg = "Memory insufficient for this operation."
                if local_hint:
                    suggestion_msg = local_hint.get("memory") or "Reduce data size or optimize memory usage."
                else:
                    suggestion_msg = "Reduce data size or optimize memory usage."

            # Handle IOError: Occurs when input/output operation fails (file operations, etc.)
            elif exc_name == "IOError":
                cause_msg = f"Input/output operation failed: {exc_value}."
                if local_hint:
                    suggestion_msg = local_hint.get("io") or "Check file paths, permissions, and availability."
                else:
                    suggestion_msg = "Check file paths, permissions, and availability."

            # Handle ArithmeticError: Base class for various arithmetic-related errors
            elif exc_name == "ArithmeticError":
                cause_msg = "Generic arithmetic error."
                if local_hint:
                    suggestion_msg = local_hint.get("arithmetic") or "Check math operations and variable values."
                else:
                    suggestion_msg = "Check math operations and variable values."

            # Filter stack trace to exclude frames from error_handler.py
            stack_list  = traceback.extract_tb(tb)
            stack_list  = [frame for frame in stack_list if "error_handler.py" not in frame.filename]
            stack_str   = "".join(traceback.format_list(stack_list))

            # Define label width to align colons vertically
            label_width = 15

            # Create the Rich panel text with aligned labels
            panel_text  = (
                            f"[bold red]{'Error         :'.ljust(label_width)}[/bold red] {exc_name}: {exc_value}\n"
                            f"[yellow]{'Cause         :'.ljust(label_width)}[/yellow] {cause_msg}\n"
                            f"[green]{'Suggested fix :'.ljust(label_width)}[/green] {suggestion_msg}\n"
                            f"[magenta]{'Stack trace   :'.ljust(label_width)}[/magenta]\n{stack_str}"
                        )

            # Create a Rich panel with the formatted text and title
            Panel_title = "[bright_red] Exception caught[/bright_red]"
            console.print(Panel.fit(panel_text, title=Panel_title,border_style="red"))

            # Return None to avoid breaking the program flow
            return None
            
    return wrapper
#?------------------------------------------------------------------------------------------------