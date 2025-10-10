from functools import wraps
from rich.console import Console
from rich.panel import Panel
import sys
import threading

if "GLOBAL_CONSOLE" not in globals():
    GLOBAL_CONSOLE = Console()
if "CONSOLE_LOCK" not in globals():
    CONSOLE_LOCK = threading.Lock()
console = GLOBAL_CONSOLE
console_lock = CONSOLE_LOCK

sys.excepthook = lambda *args: None  # suppress tracebacks

class ErrorHint:
    """Per-function hint messages with optional force_skip."""
    def __init__(self):
        self.hints = {}
        self.shown_hints = set()

    def add(self, func_name, message, force_skip=False):
        self.hints[func_name] = (message, force_skip)

    def get_for_func(self, func_name):
        return self.hints.get(func_name, None)

    def should_show(self, msg):
        if msg in self.shown_hints:
            return False
        self.shown_hints.add(msg)
        return True

def _run_recovery(obj, recovery_func_name):
    ran_flag = f"_{recovery_func_name}_ran"
    orig_name = f"__orig_{recovery_func_name}"
    if hasattr(obj, orig_name) and not getattr(obj, ran_flag, False):
        try:
            getattr(obj, orig_name)()
            setattr(obj, ran_flag, True)
        except Exception:
            # show panel on recovery failure
            suggestion = None
            if hasattr(obj, "hint"):
                hint = obj.hint.get_for_func(recovery_func_name)
                if hint:
                    suggestion = hint[0]
            if not suggestion:
                suggestion = f"Recovery {recovery_func_name} failed"
            with console_lock:
                console.print(
                    Panel.fit(
                        f"[bold yellow]{suggestion}[/bold yellow]",
                        title="[bright_red]Exception in recovery — HALT[/bright_red]",
                        border_style="red"
                    )
                )
            sys.exit(0)

def safe_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_obj = args[0] if args else None
        func_name = func.__name__

        if self_obj is None:
            try:
                return func(*args, **kwargs)
            except Exception:
                return None

        if not hasattr(self_obj, "_skip_lock"):
            self_obj._skip_lock = threading.Lock()
        if not hasattr(self_obj, "_skip_next_steps"):
            self_obj._skip_next_steps = False

        with self_obj._skip_lock:
            if self_obj._skip_next_steps:
                return None

        try:
            return func(*args, **kwargs)
        except Exception:
            # Exception caught — get hint for this function
            message, force_skip = None, False
            if hasattr(self_obj, "hint"):
                hint = self_obj.hint.get_for_func(func_name)
                if hint:
                    message, force_skip = hint

            if message and hasattr(self_obj, "hint") and self_obj.hint.should_show(message):
                with console_lock:
                    console.print(
                        Panel.fit(
                            f"[bold yellow]{message}[/bold yellow]",
                            title=f"[bright_red]Exception caught in {func_name}[/bright_red]",
                            border_style="red"
                        )
                    )

            # Force skip triggers immediate jump to recovery
            if force_skip and hasattr(self_obj, "_safe_rules"):
                recovery_func = self_obj._safe_rules.get(func_name)
                if recovery_func:
                    with self_obj._skip_lock:
                        self_obj._skip_next_steps = True
                    _run_recovery(self_obj, recovery_func)

            return None
    return wrapper

def safe_class(skip_rules=None):
    skip_rules = skip_rules or {}
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
