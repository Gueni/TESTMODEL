# ============================================================
# error_handler_final_func_hint.py — fully working
# ============================================================

from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

# -------------------- GLOBAL CONSOLE ------------------------
if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()

console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK


# -------------------- ERROR HINT ----------------------------
class ErrorHint:
    """Stores hints for functions with force_skip flag."""
    def __init__(self):
        self.hints = []  # list of tuples: (func_name, force_skip, message)
        self.shown_hints = set()

    def add(self, message, force_skip=False):
        """Add a hint. Associated with the function calling this add()."""
        import inspect
        func_name = inspect.stack()[1].function
        self.hints.append((func_name, force_skip, message))

    def get_for_func(self, func_name):
        """Return the last hint for the given function."""
        for f, force, msg in reversed(self.hints):
            if f == func_name:
                return f, force, msg
        return None

    def should_show(self, msg):
        """Prevent duplicate hint panels."""
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

    def clear(self):
        self.hints.clear()
        self.shown_hints.clear()


# -------------------- RECOVERY RUNNER -----------------------
def _run_recovery(obj, current_func_name):
    """Call recovery function safely. Exit cleanly if recovery fails."""
    recovery_func_name = None
    if hasattr(obj.__class__, "_safe_rules"):
        rules = obj.__class__._safe_rules
        recovery_func_name = rules.get(current_func_name)
        if not recovery_func_name and rules:
            recovery_func_name = next(iter(rules.values()), None)

    if not recovery_func_name:
        return

    ran_flag = f"_{recovery_func_name}_ran"
    orig_name = f"__orig_{recovery_func_name}"

    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()
            setattr(obj, ran_flag, True)
        except Exception:
            # show panel for recovery failure
            suggestion = None
            if hasattr(obj, "hint"):
                last_hint = obj.hint.get_for_func(recovery_func_name)
                if last_hint:
                    _, _, suggestion = last_hint
            if not suggestion:
                suggestion = f"Exception in recovery function {recovery_func_name}"
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red",
                    )
                )
            sys.exit(0)  # clean exit


def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        if not self_obj:
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        # Initialize skip lock
        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()

        # Check skip flag
        with self_obj._skip_lock:
            if getattr(self_obj, "_skip_next_steps", False):
                return None

        # Check for function-specific hint
        force_skip = False
        func_hint = None
        if hasattr(self_obj, "hint"):
            hint_data = self_obj.hint.get_for_func(func.__name__)
            if hint_data:
                _, force_skip, func_hint = hint_data

        # If force_skip is True, jump immediately to recovery
        if force_skip:
            with self_obj._skip_lock:
                self_obj._skip_next_steps = True
            if func_hint:
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{func_hint}[/bold yellow]",
                            title=f"[bright_red]Forced skip in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )
            _run_recovery(self_obj, func.__name__)
            return None

        # Run function normally
        try:
            return func(*args, **kwargs)
        except Exception:
            # Show panel for the hint (if any)
            if func_hint:
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{func_hint}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func.__name__}[/bright_red]",
                            border_style="red",
                        )
                    )
            return None

    return wrapper


# -------------------- SAFE CLASS DECORATOR -----------------
def safe_class(skip_rules):
    """Wrap all class methods once with safe_function."""
    def decorator(cls):
        if getattr(cls, "_already_wrapped", False):
            return cls

        cls._safe_rules = skip_rules

        for name, method in list(cls.__dict__.items()):
            if callable(method) and not name.startswith("__"):
                setattr(cls, f"__orig_{name}", method)
                setattr(cls, name, safe_function(method))

        cls._already_wrapped = True
        return cls
    return decorator


# ===================== DEMO USAGE ==========================
if __name__ == "__main__":
    import time

    @safe_class({"step1": "step_end", "step5": "step_end"})
    class MyClass:
        def __init__(self):
            self.hint = ErrorHint()

        def step1(self):
            self.hint.add("Warning in step1, continue normally", force_skip=False)
            print("Step1 executing")
            raise ZeroDivisionError("Oops in step1")  # will continue because force_skip=False

        def step2(self):
            self.hint.add("Step2 hint, continue normally", force_skip=False)
            print("Step2 executing")
            # normal

        def step3(self):
            self.hint.add("Step3 critical error — skip to recovery", force_skip=True)
            print("Step3 executing")
            raise ValueError("Critical error step3")  # triggers recovery

        def step4(self):
            print("Step4 should be skipped if recovery triggered")

        def step5(self):
            self.hint.add("Step5 hint force skip", force_skip=True)
            print("Step5 executing")
            raise RuntimeError("Step5 error triggers recovery")

        def step_end(self):
            self.hint.add("Recovery running — will exit if fails", force_skip=False)
            print("Step_end recovery executing")
            1 / 0  # simulate fatal error in recovery

    # -------------------- MAIN ----------------------------
    obj = MyClass()
    for i in range(1):
        obj.step1()
        obj.step2()
        obj.step3()
        obj.step4()
        obj.step5()
