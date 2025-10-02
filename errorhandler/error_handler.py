import sys
import traceback
from functools import wraps
from rich.console import Console
from rich.panel import Panel
import inspect

console = Console()

class ErrorHint:
    """Store custom suggestions per variable."""
    def __init__(self):
        self.hints = {}
    def add(self, var_name, suggestion):
        self.hints[var_name] = suggestion
    def get(self, var_name):
        return self.hints.get(var_name, None)

# --- Class decorator to wrap all methods ---
def safe_class(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith("__"):
            setattr(cls, attr_name, safe_function(attr_value))
    return cls

# --- Function wrapper ---
def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, tb = sys.exc_info()
            exc_name = exc_type.__name__

            # Function arguments
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments

            # Look for hint: function-level or self.hint
            local_hint = None
            frame = tb.tb_frame
            local_vars = frame.f_locals
            # function-level hint
            if "hint" in local_vars and isinstance(local_vars["hint"], ErrorHint):
                local_hint = local_vars["hint"]
            # self.hint if exists
            elif args:
                first_arg = args[0]
                if hasattr(first_arg, "hint") and isinstance(first_arg.hint, ErrorHint):
                    local_hint = first_arg.hint

            # Default cause & suggestion
            cause_msg = "Could not automatically determine the cause."
            suggestion_msg = "Check variable values and types."

            # --- Smart analysis ---
            if exc_name == "ZeroDivisionError":
                for name, val in arguments.items():
                    if isinstance(val, (int, float)) and val == 0:
                        cause_msg = f"The variable '{name}' is zero."
                        if local_hint and local_hint.get(name):
                            suggestion_msg = local_hint.get(name)
                        else:
                            suggestion_msg = f"Ensure '{name}' is not zero before division."
                        break

            elif exc_name == "FileNotFoundError":
                filename = getattr(exc_value, 'filename', None)
                if filename:
                    cause_msg = f"The file '{filename}' does not exist."
                    if local_hint and local_hint.get("filename"):
                        suggestion_msg = local_hint.get("filename")
                    else:
                        suggestion_msg = f"Ensure the file '{filename}' exists in the correct path."

            elif exc_name in ["TypeError", "ValueError"]:
                cause_msg = "Check the values of your function arguments."
                suggestion_msg = "Ensure they have correct types/values."

            # Stack trace
            stack_str = "".join(traceback.format_tb(tb))

            # Define label width for alignment
            label_width = 15

            panel_text = (
                f"[bold red]{'Error         :'.ljust(label_width)}[/bold red] {exc_name}: {exc_value}\n"
                f"[yellow]{'Cause         :'.ljust(label_width)}[/yellow] {cause_msg}\n"
                f"[green]{'Suggested fix :'.ljust(label_width)}[/green] {suggestion_msg}\n"
                f"[magenta]{'Stack trace   :'.ljust(label_width)}[/magenta]\n{stack_str}"
            )

            console.print(Panel.fit(
                panel_text,
                title="[bright_red]🚨 Exception caught[/bright_red]",
                border_style="red"
            ))

            return None
    return wrapper
