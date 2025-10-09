#?------------------------------------------------------------------------------------------------
import sys
import traceback
import inspect
from functools import wraps
from rich.console import Console
from rich.panel import Panel
#?------------------------------------------------------------------------------------------------
console = Console()
#?------------------------------------------------------------------------------------------------
class ErrorHint:
    """
    Stores custom suggestions per variable.
    Add variable-specific hints that are used by the error handler
    to provide suggestions when exceptions occur.
    """
    def __init__(self):
        self.hints = {}

    def add(self, var_name, suggestion):
        """Add a custom suggestion for a variable."""
        self.hints[var_name] = suggestion

    def get(self, var_name):
        """Retrieve a suggestion for a variable, if available."""
        return self.hints.get(var_name, None)
#?------------------------------------------------------------------------------------------------
def safe(target):
    """
    Universal decorator — works on both functions and classes.
    - If applied to a function, wraps it with safe_function.
    - If applied to a class, wraps all non-dunder methods.
    """
    if inspect.isclass(target):
        # Wrap all callable methods in the class
        for attr_name, attr_value in target.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(target, attr_name, safe_function(attr_value))
        return target
    else:
        # Normal function
        return safe_function(target)
#?------------------------------------------------------------------------------------------------
def safe_function(func):
    """
    Wraps a function to display Rich error panels with
    cause and hint suggestions when exceptions occur.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, tb = sys.exc_info()
            exc_name = exc_type.__name__

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments

            local_hint = None
            frame = tb.tb_frame
            local_vars = frame.f_locals

            # detect ErrorHint in local scope or in self
            if "hint" in local_vars and isinstance(local_vars["hint"], ErrorHint):
                local_hint = local_vars["hint"]
            elif args:
                first_arg = args[0]
                if hasattr(first_arg, "hint") and isinstance(first_arg.hint, ErrorHint):
                    local_hint = first_arg.hint

            cause_msg = "Could not automatically determine the cause."
            suggestion_msg = "Check variable values and types."

            arg_items = list(arguments.items())
            if args and hasattr(args[0], "__class__"):
                arg_items_to_check = arg_items[1:]  # skip self
            else:
                arg_items_to_check = arg_items

            # --- Common error detection ---
            if exc_name == "ZeroDivisionError":
                for name, val in arg_items_to_check:
                    if isinstance(val, (int, float)) and val == 0:
                        cause_msg = f"The variable '{name}' is zero."
                        suggestion_msg = local_hint.get(name) if local_hint and local_hint.get(name) \
                                         else f"Ensure '{name}' is not zero before division."
                        break

            elif exc_name == "FileNotFoundError":
                filename = getattr(exc_value, 'filename', None)
                cause_msg = f"The file '{filename}' does not exist."
                suggestion_msg = local_hint.get("filename") if local_hint and local_hint.get("filename") \
                                 else f"Ensure the file '{filename}' exists."

            elif exc_name == "TypeError":
                for name, val in arg_items_to_check:
                    cause_msg = f"Variable '{name}' has wrong type: {type(val).__name__}."
                    suggestion_msg = local_hint.get(name) if local_hint and local_hint.get(name) \
                                     else f"Ensure '{name}' has the correct type."
                    break

            elif exc_name == "ValueError":
                for name, val in arg_items_to_check:
                    cause_msg = f"Variable '{name}' has invalid value: {val}."
                    suggestion_msg = local_hint.get(name) if local_hint and local_hint.get(name) \
                                     else f"Ensure '{name}' has a valid value."
                    break

            elif exc_name == "IndexError":
                cause_msg = "Index out of range."
                suggestion_msg = local_hint.get("index") if local_hint and local_hint.get("index") \
                                 else "Check list index range."

            elif exc_name == "KeyError":
                key = getattr(exc_value, 'args', [None])[0]
                cause_msg = f"Dictionary key '{key}' not found."
                suggestion_msg = local_hint.get(str(key)) if local_hint and local_hint.get(str(key)) \
                                 else f"Ensure key '{key}' exists in the dictionary."

            elif exc_name == "AttributeError":
                cause_msg = str(exc_value)
                suggestion_msg = "Ensure the object has the required attribute."

            elif exc_name == "NameError":
                var_name = getattr(exc_value, 'name', None)
                cause_msg = f"The variable '{var_name}' is not defined."
                suggestion_msg = local_hint.get(var_name) if local_hint and local_hint.get(var_name) \
                                 else f"Define '{var_name}' before using it."

            # Filter trace (exclude this file)
            stack_list = traceback.extract_tb(tb)
            stack_list = [frame for frame in stack_list if "error_handler" not in frame.filename]
            stack_str = "".join(traceback.format_list(stack_list))

            label_width = 15
            panel_text = (
                f"[bold red]{'Error         :'.ljust(label_width)}[/bold red] {exc_name}: {exc_value}\n"
                f"[yellow]{'Cause         :'.ljust(label_width)}[/yellow] {cause_msg}\n"
                f"[green]{'Suggested fix :'.ljust(label_width)}[/green] {suggestion_msg}\n"
                f"[magenta]{'Stack trace   :'.ljust(label_width)}[/magenta]\n{stack_str}"
            )

            console.print(Panel.fit(panel_text, title="[bright_red]Exception caught[/bright_red]", border_style="red"))
            return None
    return wrapper
#?------------------------------------------------------------------------------------------------
# ✅ EXAMPLE USAGE
#?------------------------------------------------------------------------------------------------
@safe
class Calculator:
    def __init__(self):
        self.hint = ErrorHint()

    def divide(self, a, b):
        self.hint.add('b', "You cannot divide by zero! Provide a non-zero 'b'")
        return a / b

    def open_file(self, filename):
        self.hint.add('filename', "Make sure the file exists or create it before opening.")
        with open(filename) as f:
            return f.read()

    def process_list_dict(self, lst, dct, index, key):
        self.hint.add('index', "Index should be within the bounds of the list.")
        self.hint.add('key', "Key must exist in the dictionary before accessing.")
        return lst[index] + dct[key]  # could raise IndexError or KeyError


# Works on classes
calc = Calculator()
calc.divide(10, 0)
calc.open_file("missing.txt")
calc.process_list_dict([1, 2, 3], {"a": 10}, 5, "b")


# Works on standalone functions
hint = ErrorHint()
hint.add("b", "You cannot divide by zero! Provide a non-zero 'b'")

@safe
def divide(a, b):
    return a / b

divide(10, 0)
