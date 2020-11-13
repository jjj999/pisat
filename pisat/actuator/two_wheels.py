
from typing import Optional, Union
from enum import Enum

from pisat.actuator.rotate_motor_driver_base import RotateMotorDriverBase


class TwoWheels(RotateMotorDriverBase):
    
    class Param(Enum):
        MAX = 100.
        MIN = -100.
        ORIGIN = 0.
    
    class DecelerationRate(Enum):
        MAX = 100.
        MIN = 0.
        
        @classmethod
        def is_valid(cls, rate: Union[int, float]) -> bool:
            if cls.MIN.value <= rate <= cls.MAX.value:
                return True
            else:
                return False
    
    def __init__(self,
                 driver_L: RotateMotorDriverBase,
                 driver_R: RotateMotorDriverBase,
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        if not isinstance(driver_L, RotateMotorDriverBase):
            raise TypeError(
                "'driver_L' must be RotateMotorDriverBase."
            )
        if not isinstance(driver_R, RotateMotorDriverBase):
            raise TypeError(
                "'driver_R' must be RotateMotorDriverBase."
            )
        if driver_L.__class__ is not driver_R.__class__:
            raise TypeError(
                "'driver_L' and 'driver_R' must be objects of same type."
            )
        
        self._driver_L: RotateMotorDriverBase = driver_L
        self._driver_R: RotateMotorDriverBase = driver_R
        self._current_param: Union[int, float] = 0.
        
        self._decode_rate: float = self._calc_decode_rate(driver_L.Param.MAX.value,
                                                          driver_L.Param.MIN.value)
    
    @classmethod
    def _calc_decode_rate(cls, max, min) -> float:
        width_driver_param = max - min
        width_this_class = cls.Param.MAX.value - cls.Param.ORIGIN.value
        
        if width_driver_param == 0:
            raise ValueError(
                "Given driver's Param has same values of MAX and MIN."
            )
            
        return width_driver_param / width_this_class
        
    def _decode_param(self, param: Union[int, float]) -> float:
        return abs(param) * self._decode_rate + self.driver_param_min
        
    @property
    def driver_param_max(self):
        return self._driver_L.Param.MAX.value
        
    @property
    def driver_param_min(self):
        return self._driver_L.Param.MIN.value
        
    @property
    def current_param(self):
        return self._current_param
        
    def standby(self) -> None:
        self._driver_L.standby()
        self._driver_R.standby()
    
    def brake(self) -> None:
        self._driver_L.brake()
        self._driver_R.brake()
        self._current_param = 0.
        
    def straight(self, param: Optional[Union[int, float]] = None) -> None:
        if param is None:
            param = self._current_param
        value = self._decode_param(param)
        
        if param >= 0:
            self._driver_L.cw(value)
            self._driver_R.ccw(value)
        else:
            self._driver_L.ccw(value)
            self._driver_R.cw(value)
            
        self._current_param = param
            
    def cw(self, param: Union[int, float]) -> None:
        value = self._decode_param(param)
        
        if param >= 0:
            self._driver_L.cw(value)
            self._driver_R.brake()
        else:
            self._driver_L.brake()
            self._driver_R.cw(value)
    
    def ccw(self, param: Union[int, float]) -> None:
        value = self._decode_param(param)
        
        if param >= 0:
            self._driver_L.brake()
            self._driver_R.ccw(value)
        else:
            self._driver_L.ccw(value)
            self._driver_R.brake()
    
    def curve_cw(self, 
                 dec: Union[int, float],
                 base: Optional[Union[int, float]] = None) -> None:
        
        if not self.DecelerationRate.is_valid(dec):
            raise ValueError(
                "'dec' must be {} <= 'dec' <= {}"
                .format(self.DecelerationRate.MIN.value,
                        self.DecelerationRate.MAX.value)
            )
            
        if base is not None:
            self._current_param = base
            
        value = self._decode_param(self._current_param)
        value_decelerated = value * (1 - dec / 100)
        
        if self._current_param >= 0:
            self._driver_L.cw(value_decelerated)
            self._driver_R.ccw(value)
        else:
            self._driver_L.ccw(value)
            self._driver_R.cw(value_decelerated)
    
    def curve_ccw(self, 
                  dec: Union[int, float], 
                  base: Optional[Union[int, float]] = None) -> None:
        
        if not self.DecelerationRate.is_valid(dec):
            raise ValueError(
                "'dec' must be {} <= 'dec' <= {}"
                .format(self.DecelerationRate.MIN.value,
                        self.DecelerationRate.MAX.value)
            )
            
        value = self._decode_param(self._current_param)
        value_decelerated = value * (1 - dec / 100)
        
        if self._current_param >= 0:
            self._driver_L.cw(value)
            self._driver_R.ccw(value_decelerated)
        else:
            self._driver_L.ccw(value_decelerated)
            self._driver_R.cw(value)
