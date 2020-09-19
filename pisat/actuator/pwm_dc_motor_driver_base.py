

from typing import Optional, Union
from enum import Enum

from pisat.handler.pwm_handler_base import PWMHandlerBase
from pisat.actuator.rotate_motor_driver_base import RotateMotorDriverBase


class PWMDCMotorDriverBase(RotateMotorDriverBase):
    
    class Param(Enum):
        MAX = PWMHandlerBase.Duty.MAX.value
        MIN = PWMHandlerBase.Duty.MIN.value
    
    def __init__(self, 
                 fin: PWMHandlerBase,
                 rin: PWMHandlerBase,
                 freq: Optional[int] = None,
                 fix_high: bool = True,
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        if not isinstance(fin, PWMHandlerBase):
            raise TypeError(
                "'fin' must be PWMHandlerBase."
            )
            
        if not isinstance(rin, PWMHandlerBase):
            raise TypeError(
                "'rin' must be PWMHandlerBase."
            )
        
        self._fin: PWMHandlerBase = fin
        self._rin: PWMHandlerBase = rin
        self._freq: Optional[int] = freq
        self._fix_high: bool = fix_high    
        
        if self._freq is None:
            if fin.freq != rin.freq:
                raise ValueError(
                    "Frequency of 'fin' and 'rin' both must be same."
                )
        else:
            self._fin.set_freq(self._freq)
            self._rin.set_freq(self._freq)
        
    @property
    def fin(self):
        return self._fin
    
    @property
    def rin(self):
        return self._rin
    
    @property
    def freq(self):
        return self._freq
    
    def set_freq(self, freq: Union[int, float]) -> None:
        self._fin.set_freq(freq)
        self._rin.set_freq(freq)
    