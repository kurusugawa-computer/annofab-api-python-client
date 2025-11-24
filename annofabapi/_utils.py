import enum
import warnings
from functools import wraps


def _issue_deprecated_warning_with_class(cls, stacklevel: int, deprecated_date: str, new_class_name: str | None = None):  # noqa: ANN001, ANN202
    """非推奨なクラスに対する警告メッセージを出力する。"""
    old_class_name = f"{cls.__module__}.{cls.__name__}"
    message = f"deprecated: '{old_class_name}'は{deprecated_date}以降に廃止します。"
    if new_class_name is not None:
        message += f"替わりに'{new_class_name}'を使用してください。"
    warnings.warn(message, FutureWarning, stacklevel=stacklevel)


def _process_class(cls, deprecated_date: str, new_class_name: str | None = None):  # noqa: ANN001, ANN202
    def decorator(function):  # noqa: ANN001, ANN202
        @wraps(function)
        def wrapped(*args, **kwargs):  # noqa: ANN202
            _issue_deprecated_warning_with_class(cls, stacklevel=3, deprecated_date=deprecated_date, new_class_name=new_class_name)
            return function(*args, **kwargs)

        return wrapped

    cls.__init__ = decorator(cls.__init__)
    return cls


def _process_enum_class(cls, deprecated_date: str, new_class_name: str | None = None):  # noqa: ANN001, ANN202
    def getattribute(self, name):  # noqa: ANN001, ANN202
        _issue_deprecated_warning_with_class(cls, stacklevel=4, deprecated_date=deprecated_date, new_class_name=new_class_name)
        return super(type(self), self).__getattribute__(name)

    cls.__getattribute__ = getattribute
    return cls


def deprecated_class(_cls=None, *, deprecated_date: str, new_class_name: str | None = None):  # noqa: ANN001, ANN202
    """クラスを非推奨にします。"""

    def wrap(cls):  # noqa: ANN001, ANN202
        if issubclass(cls, enum.Enum):
            return _process_enum_class(cls, deprecated_date=deprecated_date, new_class_name=new_class_name)
        else:
            return _process_class(cls, deprecated_date=deprecated_date, new_class_name=new_class_name)

    if _cls is None:
        return wrap
    return wrap(_cls)
