
from typing import Optional, Union
from enum import Enum

from pisat.actuator.rotate_motor_driver_base import RotateMotorDriverBase


class TwoWheels(RotateMotorDriverBase):
    
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
        
    def standby(self) -> None:
        self._driver_L.standby()
        self._driver_R.standby()
    
    def brake(self) -> None:
        self._driver_L.brake()
        self._driver_R.brake()
        self._current_param = 0.
        
    # TODO
    # 
        
    def straight(self, param: Optional[Union[int, float]] = None) -> None:
        if param >= 0:
            self._driver_L.cw(param)
            self._driver_R.ccw(param)
        else:
            self._driver_L.ccw(param)
            self._driver_R.cw(param)
            
        self._current_param = param
            
    def cw(self, param: Union[int, float]) -> None:
        self.brake()
        if param >= 0:
            self._driver_L.cw(param)
        else:
            self._driver_R.cw(abs(param))
    
    def ccw(self, param: Union[int, float]) -> None:
        self.brake()
        if param >= 0:
            self._driver_R.ccw(param)
        else:
            self._driver_L.ccw(abs(param))

    def curve_cw(self, 
                 dec: Union[int, float],
                 base: Optional[Union[int, float]] = None) -> None:
        if base is not None:
            self._current_param = base
            
        value_decelerated = self._current_param * (1 - dec / 100)
        if value_decelerated < 0:
            value_decelerated = 0
        
        if self._current_param >= 0:
            self._driver_L.cw(value_decelerated)
            self._driver_R.ccw(self._current_param)
        else:
            self._driver_L.ccw(self._current_param)
            self._driver_R.cw(value_decelerated)
    
    def curve_ccw(self, 
                  dec: Union[int, float], 
                  base: Optional[Union[int, float]] = None) -> None:
        if base is not None:
            self._current_param = base

        value_decelerated = self._current_param * (1 - dec / 100)
        if value_decelerated < 0:
            value_decelerated = 0
        
        if self._current_param >= 0:
            self._driver_L.cw(self._current_param)
            self._driver_R.ccw(value_decelerated)
        else:
            self._driver_L.ccw(value_decelerated)
            self._driver_R.cw(self._current_param)
