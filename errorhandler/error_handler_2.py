from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys

console = Console()

class ErrorHint:
    """Stores variable-specific hints with optional force_skip flags."""
    def __init__(self):
        # list of tuples: (variable_name, force_skip, message)
        self.hints = []

    def add(self, hint_tuple):
        """Add a hint as (variable, force_skip, message)."""
        self.hints.append(hint_tuple)

    def get_for_variable(self, variable):
        """Return the most recent hint for a given variable."""
        for var, force, msg in reversed(self.hints):
            if var == variable:
                return var, force, msg
        return None, None, None

    def clear(self):
        self.hints.clear()


def safe_function(func, recovery_func_name=None, cls=None):
    """Wrap a method with skip-on-error logic and per-variable hints."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None

        # Skip logic: skip all methods except the designated recovery
        if getattr(self_obj, "_skip_next_steps", False):
            if recovery_func_name and func.__name__ == recovery_func_name:
                pass
            else:
                return None

        try:
            return func(*args, **kwargs)

        except Exception as e:
            variable_name = getattr(e, "args", (None,))[0]  # optional: you can set variable name in exception
            if self_obj and hasattr(self_obj, "hint"):
                var, force, msg = self_obj.hint.get_for_variable(variable_name)
            else:
                var, force, msg = None, None, None

            if msg is None:
                msg = f"{type(e).__name__}: {str(e)}"

            console.print(
                Panel.fit(
                    f"[bold yellow]{msg}[/bold yellow]",
                    title="[bright_red]Exception caught[/bright_red]",
                    border_style="red"
                )
            )

            # Determine if we should skip to recovery
            if force:
                self_obj._skip_next_steps = True

            # Call recovery function if skip_rules define it
            if self_obj and recovery_func_name:
                ran_flag = f"_{recovery_func_name}_ran"
                if hasattr(self_obj, f"__orig_{recovery_func_name}") and not getattr(self_obj, ran_flag, False):
                    try:
                        getattr(self_obj, f"__orig_{recovery_func_name}")()
                        setattr(self_obj, ran_flag, True)
                    except Exception as e2:
                        # Show hint from recovery if exists
                        var2, force2, msg2 = self_obj.hint.get_for_variable(None)
                        msg2 = msg2 or f"Error in recovery: {type(e2).__name__}: {e2}"
                        console.print(
                            Panel.fit(f"[bold yellow]{msg2}[/bold yellow]",
                                      title="[bright_red]Recovery failed[/bright_red]",
                                      border_style="red")
                        )
                        sys.exit(1)  # halt program if recovery fails

            return None
    return wrapper


def safe_class(skip_rules):
    """Applies safe_function to all class methods."""
    def decorator(cls):
        for name, method in list(cls.__dict__.items()):
            if callable(method):
                recovery_func_name = skip_rules.get(name)
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method, recovery_func_name, cls))
        return cls
    return decorator
