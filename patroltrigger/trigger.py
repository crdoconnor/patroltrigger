from functools import wraps


def trigger(include, exclude=None):
    """Annotate the patrol methods."""
    def decorator(method):
        method.includes = include
        method.excludes = exclude
        method.is_trigger = True
        method.is_running = False

        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper
    return decorator
