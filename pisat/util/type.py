

from typing import Callable, Optional, Sequence, TypeVar, Union


T = TypeVar("T")


def is_all_None(*args) -> bool:
    for arg in args:
        if arg is not None:
            return False
    else:
        return True


def empty_None(seq: Sequence, f: Optional[Callable[[Sequence], T]] = None) -> Union[Sequence, T, None]:
    if len(seq):
        if f is None:
            return seq
        else:
            return f(seq)
    else:
        return None
