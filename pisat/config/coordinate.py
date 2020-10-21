

from enum import Enum, auto

from pisat.config.type import Logable


class CoordinateComponent(Enum):
    REAL = auto()
    COMPLEX = auto()
    QUATERNION = auto()


class CoordinateSystem(Enum):
    CARTESIAN = auto()
    POLAR = auto()
    EULER = auto()
    GEOGRAPHIC = auto()
    

class CoordinateBase:
    SYSTEM_AVAILABLE = ()


class Scalar(CoordinateBase):
    
    def __init__(self, val: Logable) -> None:
        self.val = val
    

class Vector2(CoordinateBase):
    pass


class Vector3(CoordinateBase):
    pass
