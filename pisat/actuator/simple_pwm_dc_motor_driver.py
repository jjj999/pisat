

from typing import Optional, Union

from pisat.handler.pwm_handler_base import PWMHandlerBase
from pisat.actuator.pwm_dc_motor_driver_base import PWMDCMotorDriverBase


class SimplePWMDCMotorDriver(PWMDCMotorDriverBase):
    
    def __init__(self,
                 fin: PWMHandlerBase,
                 rin: PWMHandlerBase,
                 freq: int = 50000,
                 fix_high: bool = True,
                 name: Optional[str] = None) -> None:
        super().__init__(fin, rin, freq=freq, fix_high=fix_high, name=name)
        
    def brake(self) -> None:
        self._fin.set_duty(self.Param.MAX.value)
        self._rin.set_duty(self.Param.MAX.value)
    
    def standby(self) -> None:
        self._fin.set_duty(self.Param.MIN.value)
        self._rin.set_duty(self.Param.MIN.value)
    
    def cw(self, duty: Union[int, float]) -> None:
        if self._fix_high:
            self._fin.set_duty(self.Param.MAX.value)
            self._rin.set_duty(duty)
        else:
            self._fin.set_duty(duty)
            self._rin.set_duty(self.Param.MIN.value)
    
    def ccw(self, duty: Union[int, float]) -> None:
        if self._fix_high:
            self._fin.set_duty(duty)
            self._rin.set_duty(self.Param.MAX.value)
        else:
            self._fin.set_duty(self.Param.MIN.value)
            self._rin.set_duty(duty)