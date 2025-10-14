def safe_function(allow_propagate=False):
    """Wraps a function with error handling and hint display.

    If allow_propagate=True, exceptions propagate to user try/except.
    If False, they are swallowed and panel is shown.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self_obj = args[0] if args else None

            try:
                return func(*args, **kwargs)

            except Exception as e:
                # Show panel
                if self_obj and hasattr(self_obj, 'hint'):
                    msg = self_obj.hint.get_hint(func.__name__)
                    if msg and not self_obj.hint.was_shown(func.__name__, msg):
                        console.print(Panel.fit(
                            f"[bold yellow]{msg}[/bold yellow]",
                            title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                            border_style="red"
                        ))
                        self_obj.hint.mark_shown(func.__name__, msg)
                    else:
                        console.print(Panel.fit(
                            f"[bold yellow]{type(e).__name__}: {e}[/bold yellow]",
                            title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                            border_style="red"
                        ))
                else:
                    console.print(Panel.fit(
                        f"[bold yellow]{type(e).__name__}: {e}[/bold yellow]",
                        title=f"[bright_red]Exception in {func.__name__}[/bright_red]",
                        border_style="red"
                    ))

                # Log quietly
                with open("error_log.log", "a", encoding="utf-8") as f:
                    traceback.print_exception(type(e), e, e.__traceback__, file=f)
                    f.write("\n")

                # Propagate if requested
                if allow_propagate:
                    raise

                return None

        return wrapper
    return decorator


critical_operation = safe_function(allow_propagate=True)(critical_operation)
