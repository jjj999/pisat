
from typing import Optional
from enum import Enum

from RPi import GPIO

from pisat.handler.pwm_handler_base import PWMHandlerBase
from pisat.handler.rpigpio_digital_output_handler import RpiGpioDigitalOutputHandler


class RpiGpioPWMHandler(PWMHandlerBase):            
    
    def __init__(self, 
                 out: RpiGpioDigitalOutputHandler, 
                 freq: float,
                 duty: float = 0., 
                 name: Optional[str] = None) -> None:
        if not isinstance(out, RpiGpioDigitalOutputHandler):
            raise TypeError(
                "'out' must be {}."
                .format(RpiGpioDigitalOutputHandler.__name__)
            )
            
        super().__init__(out.pin, freq, duty, name=name)
        
        self._pwm = GPIO.PWM(out.pin, freq)
        
        # NOTE
        #   PWM doesn't start in the constructor. If 'start' is called, 
        #   PWM get started with the current duty cycle.
        
    def close(self) -> None:
        GPIO.cleanup(self._pin)
        
    def set_duty(self, duty: float) -> None:
        if self.Duty.is_valid(duty):
            self._pwm.ChangeDutyCycle(duty)
            self._duty = duty
        else:
            ValueError(
                "'duty' must be {} <= 'duty' <= {}."
                .format(self.Duty.MIN.value, self.Duty.MAX.value)
            )
        
    def set_freq(self, freq: float) -> None:
        if freq >= 0.:
            self._pwm.ChangeFrequency(freq)
            self._freq = freq
        else:
            ValueError(
                "'freq' must be no less than 0."
            )
            
    def start(self, duty: Optional[float] = None) -> None:
        if duty is not None:
            self.set_duty(duty)    
        self._pwm.start(self._duty)
        
    def stop(self) -> None:
        self._pwm.stop()
            