#?------------------------------------------------------------------------------------------------
import sys
import traceback
import threading
from functools import wraps
from rich.console import Console
from rich.panel import Panel
#?------------------------------------------------------------------------------------------------
console = Console()
console_lock = threading.Lock()
_ALREADY_DECORATED = set()
#?------------------------------------------------------------------------------------------------
class ErrorHint:
    """
    Stores per-variable hints and skip behavior.
    Each hint shows only once per variable name.
    """
    def __init__(self):
        self.hints = {}        # {var_name: (hint, force_skip)}
        self.displayed = set() # Tracks displayed variable names

    def add(self, var_name, hint, force_skip=False):
        self.hints[var_name] = (hint, force_skip)

    def get(self, var_name):
        return self.hints.get(var_name, (None, False))

    def show_hint(self, var_name):
        """Show the hint panel for the given variable only once."""
        hint, force_skip = self.get(var_name)
        if hint and var_name not in self.displayed:
            with console_lock:
                console.print(Panel(hint, title="Exception caught", style="bold red"))
            self.displayed.add(var_name)
        return force_skip
#?------------------------------------------------------------------------------------------------
def safe_class(skip_rules):
    """
    Decorator for a class to handle errors in methods based on skip_rules.
    Ensures:
      - Only decorated once per class
      - Thread-safe printing
      - Shows hint only once per variable
    """
    def decorator(cls):
        if cls.__name__ in _ALREADY_DECORATED:
            return cls
        _ALREADY_DECORATED.add(cls.__name__)

        for name, func in cls.__dict__.items():
            if not callable(func) or name.startswith("__"):
                continue

            @wraps(func)
            def wrapper(self, *args, __func=func, __name=name, **kwargs):
                try:
                    return __func(self, *args, **kwargs)
                except Exception as e:
                    # Try to find a relevant variable hint
                    force_skip = False
                    for var_name in getattr(self, "hint", ErrorHint()).hints:
                        hint, fskip = self.hint.get(var_name)
                        if var_name in traceback.format_exc():
                            force_skip = self.hint.show_hint(var_name) or force_skip
                            break
                    else:
                        # fallback if no matching variable found
                        with console_lock:
                            console.print(
                                Panel(
                                    f"{type(e).__name__}: {e}",
                                    title="Unhandled Exception",
                                    style="bold yellow"
                                )
                            )

                    # Handle skipping logic
                    if __name in skip_rules:
                        next_func = skip_rules[__name]
                        if force_skip:
                            # Skip and call next recovery method
                            recovery = getattr(self, next_func, None)
                            if recovery:
                                with console_lock:
                                    console.print(
                                        Panel(
                                            f"⚠️  Skipping {__name} → Running recovery {next_func}",
                                            style="bold yellow"
                                        )
                                    )
                                try:
                                    recovery()
                                except Exception as e2:
                                    with console_lock:
                                        console.print(
                                            Panel(
                                                f"{next_func} failed: {e2}",
                                                title="Exception in recovery — HALT",
                                                style="bold red"
                                            )
                                        )
                            return
                    raise
            setattr(cls, name, wrapper)
        return cls
    return decorator
#?------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # ✅ Example usage
    @safe_class({"step1": "step_end", "step5": "step_end"})
    class MyClass:
        def __init__(self):
            self.hint = ErrorHint()

        def step1(self, a, b):
            self.hint.add("b", "b must not be zero — warning only", force_skip=True)
            print("Step1 executing")
            print(a / b)

        def step2(self):
            self.hint.add("none", "Step2 runs fine", force_skip=False)
            print("Step2 runs normally")

        def step5(self):
            self.hint.add("custom", "Step5 failed — jumping to recovery", force_skip=False)
            raise ValueError("Step5 triggers recovery")

        def step_end(self):
            self.hint.add("recovery", "Step_end recovery running — program will halt if fails", force_skip=False)
            print("Step_end recovery running...")
            1 / 0  # fatal in recovery

    # ✅ Demo
    obj = MyClass()
    obj.step1(10, 0)  # Skips next due to force_skip=True
    obj.step2()
    obj.step5()
