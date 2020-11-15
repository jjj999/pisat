
import math
from typing import Union

from pisat.handler.pwm_handler_base import PWMHandlerBase


class ParamCushion:
    
    VALUE_MAX = 0
    VALUE_MIN = 0
    VALUE_WIDTH = VALUE_MAX - VALUE_MIN
    
    def __init__(self, min: Union[int, float], max: Union[int, float]) -> None:
        if min >= max:
            raise ValueError("'min' must be less than 'max'")
        
        self._min = min
        self._max = max
        self._width = max - min
        
    def is_valid_value(self, value: Union[int, float]) -> bool:
        return self._min <= value <= self._max
        
    def convert(self, value: Union[int, float]) -> float:
        if self.is_valid_value(value):
            return self.VALUE_WIDTH / self._width * (value - self._min)
        else:
            ValueError(
                f"'value' is out of range. 'value' must be {self._min} <= 'value' <= {self._max}."
            )
            
            
class PWMCushion(ParamCushion):
    
    VALUE_MAX = PWMHandlerBase.DUTY_MAX
    VALUE_MIN = PWMHandlerBase.DUTY_MIN
    

class DegreeCushion(ParamCushion):        

    VALUE_MAX = 180.
    VALUE_MIN = -180.
    
    
class RadianCushion(ParamCushion):
    
    VALUE_MAX = math.pi
    VALUE_MIN = - math.pi
    