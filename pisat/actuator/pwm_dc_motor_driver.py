

from typing import Optional, Union

from pisat.actuator.rotate_motor_driver_base import RotateMotorDriverBase
from pisat.handler.pwm_handler_base import PWMHandlerBase


class PWMDCMotorDriver(RotateMotorDriverBase):
    
    DUTY_MAX = PWMHandlerBase.DUTY_MAX
    DUTY_MIN = PWMHandlerBase.DUTY_MIN
    
    def __init__(self,
                 fin: PWMHandlerBase,
                 rin: PWMHandlerBase,
                 fix_high: bool = False,
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
        self._fix_high: bool = fix_high
        
        if fin.freq != rin.freq:
            raise ValueError(
                "Frequency of 'fin' and 'rin' both must be same."
            )
            
        self._fin.start(duty=0)
        self._rin.start(duty=0)
            
    def brake(self) -> None:
        self._fin.set_duty(self.DUTY_MAX)
        self._rin.set_duty(self.DUTY_MAX)
        
    def ccw(self, duty: Union[int, float]) -> None:
        if self._fix_high:
            self._fin.set_duty(self.DUTY_MAX)
            self._rin.set_duty(duty)
        else:
            self._fin.set_duty(duty)
            self._rin.set_duty(self.DUTY_MIN)
        
    def cw(self, duty: Union[int, float]) -> None:
        if self._fix_high:
            self._fin.set_duty(duty)
            self._rin.set_duty(self.DUTY_MAX)
        else:
            self._fin.set_duty(self.DUTY_MIN)
            self._rin.set_duty(duty)
            
    @property
    def fin(self):
        return self._fin
    
    @property
    def rin(self):
        return self._rin
        
    def standby(self) -> None:
        self._fin.set_duty(self.DUTY_MIN)
        self._rin.set_duty(self.DUTY_MIN)
    