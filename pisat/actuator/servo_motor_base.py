
from enum import Enum
from typing import Union

from pisat.base.component import Component


class ServoMotorBase(Component):
    
    # TODO to be overrided
    class Angle(Enum):
        MAX = 0.
        MIN = 0.
        
    @classmethod
    def is_valid_angle(cls, angle: Union[int, float]) -> bool:
        if cls.Angle.MIN.value <= angle <= cls.Angle.MAX.value:
            return True
        else:
            return False
        
    # TODO to be overrided
    def to_angle(self, angle: Union[int, float]) -> None:
        pass
        