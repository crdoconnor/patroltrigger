from functools import wraps


def trigger(include, exclude=None, priority=0, waitfor=0.0, drop=True):
    """Annotate the patrol methods."""
    def decorator(method):
        method.includes = include
        method.excludes = exclude
        #method.priority = priority
        #method.waitfor = waitfor
        #method.drop = drop
        method.is_trigger = True
        method.is_running = False

        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper
    return decorator
