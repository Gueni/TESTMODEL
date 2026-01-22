#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
from functools import wraps
from rich.console import Console
from rich.panel import Panel
import traceback
from contextlib import contextmanager  # <-- Add this import

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
# ... existing code ...

# Add this context manager after the class definitions (before the decorators or at the end)
@contextmanager
def allow_exceptions():
    """Temporarily allow exceptions to propagate through the error handler."""
    original_flag = getattr(dp, 'flag', False)
    dp.flag = True
    try:
        yield
    finally:
        dp.flag = original_flag

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------