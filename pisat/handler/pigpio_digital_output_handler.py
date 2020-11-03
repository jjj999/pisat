
from typing import Optional

import pigpio

from pisat.handler.digital_output_handler_base import DigitalOutputHandlerBase


class PigpioDigitalOutputHandler(DigitalOutputHandlerBase):
    
    def __init__(self,
                 pi: pigpio.pi,
                 pin: int,
                 name: Optional[str] = None) -> None:
        super().__init__(pin, name=name)
        
        self._pi: pigpio.pi = pi
        self._pi.set_mode(pin, pigpio.OUTPUT)
        
    def set_high(self) -> None:
        self._pi.write(self._pin, pigpio.HIGH)
        
    def set_low(self) -> None:
        self._pi.write(self._pin, pigpio.LOW)
        