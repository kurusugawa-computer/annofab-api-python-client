import warnings
from functools import wraps


def moved_class(new_class, old_class_name: str, deprecated_date: str):
    """Deprecates a class that was moved to another location."""

    def decorator(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            warnings.warn(
                f"deprecated: {deprecated_date}以降に廃止します。替わりに'{new_class.__module__}.{new_class.__name__}'を使用してください。",
                DeprecationWarning,
            )

        return wrapped

    old_class = type(old_class_name, (new_class,), {})
    old_class.__init__ = decorator(old_class.__init__)  # type: ignore
    old_class.__doc__ = "[deprecation]\n{new_class.__doc__}"
    return old_class
