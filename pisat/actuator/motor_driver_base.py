#! python3

"""

pisat.actuator.motor.motor_base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
    
"""

from typing import Union
from enum import Enum

from pisat.base.component import Component


class MotorDriverBase(Component):
    
    # TODO to be overrided
    class Param(Enum):
        MAX = 0
        MIN = 0
        
    @classmethod
    def is_valid_param(cls, param: Union[int, float]) -> bool:
        if cls.Param.MIN.value <= param <= cls.Param.MAX.value:
            return True
        else:
            return False
    
    # TODO to be overrided
    def brake(self) -> None:
        pass
    
    # TODO to be overrided
    def standby(self) -> None:
        pass
