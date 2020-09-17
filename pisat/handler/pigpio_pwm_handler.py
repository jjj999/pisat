
from typing import Optional, Union
from enum import Enum

import pigpio

from pisat.handler.pwm_handler_base import PWMHandlerBase


class PigpioPWMHandler(PWMHandlerBase):
            
    class Range(Enum):
        MAX = 40000
        MIN = 25
        
        @classmethod
        def is_valid(cls, range: int) -> bool:
            if cls.MIN <= range <= cls.MAX:
                return True
            else:
                return False
    
    def __init__(self, 
                 pi: pigpio.pi,
                 pin: int,
                 freq: int,
                 duty: Union[int, float] = 0,
                 range: int = 255,
                 name: Optional[str] = None) -> None:
        super().__init__(pin, freq, duty, name=name)
        
        self._pi: pigpio.pi = pi
        self._range: int = range
        
        # NOTE
        #   PWM doesn't start in the constructor. If 'start' is called, 
        #   PWM get started with the current duty cycle.
        
    @property
    def range(self):
        return self._range
        
    def set_duty(self, duty: Union[int, float]) -> None:
        if self.Duty.is_valid(duty):
            # Calculate an appropriate value for the interface of pigpio.
            duty_real = int(duty * 0.01 * self._range)
            
            if duty_real > self._range:
                duty_real = self._range
            elif duty_real < 0:
                duty_real = 0
                
            self._pi.set_PWM_dutycycle(self._pin, duty_real)
        else:
            ValueError(
                "'duty' must be {} <= 'duty' <= {}"
                .format(self.Duty.MIN.value, self.Duty.MAX.value)
            )
    
    def set_freq(self, freq: int) -> None:
        result = self._pi.set_PWM_frequency(self._pin, freq)
        self._freq = result
        
    def set_range(self, range: int) -> None:
        if self.Range.is_valid(range):
            self._pi.set_PWM_range(self._pin, range)
            self._range = range
        else:
            ValueError(
                "'range' must be {} <= 'range' <= {}"
                .format(self.Duty.MIN.value, self.Duty.MAX.value)
            )
        
    def start(self, duty: Optional[Union[int, float]] = None) -> None:
        if duty is not None:
            self.set_duty(duty)
        else:
            self._pi.set_duty(self._duty)
            
    def stop(self) -> None:
        self._pi.set_PWM_dutycycle(self._pin, 0)
        