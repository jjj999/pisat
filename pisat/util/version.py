
from typing import Tuple, Union
from enum import Enum


TYPE_VERSION = Tuple[Union[int, str]]

class VersionState(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"
    STABLE = "stable"
    AVAILABLES = (ALPHA, BETA, GAMMA, STABLE)

    @classmethod
    def is_valid(cls, state: str) -> bool:
        if state in cls.AVAILABLES.value:
            return True
        else:
            return False


def resolve_version(version: TYPE_VERSION):
    if not isinstance(version, tuple):
        TypeError(
            "'version' must be tuple."
        )
    if len(version) != 3:
        ValueError(
            "Length of 'version' must be 3."
        )
        
    for i, param in enumerate(version):
        if i in (0, 1):
            if not isinstance(param, int):
                TypeError(
                    "index {} of 'version' must be int."
                    .format(i)
                )
        elif i == 2:
            if isinstance(param, str):
                if not VersionState.is_valid(param):
                    ValueError(
                        "value of index {} of 'version' must be one of {}"
                        .format(i, VersionState.AVAILABLES.value)
                    )
            else:
                TypeError(
                    "index {} of 'version' must be str."
                    .format(i)
                )     
    return "{}.{}-{}".format(version[0], version[1], version[2])
                