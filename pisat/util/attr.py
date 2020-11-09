

from typing import Callable


def get_callable_name(obj: Callable) -> str:
    return obj.__name__
