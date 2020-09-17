
from typing import Optional

from RPi import GPIO

from pisat.handler.digital_output_handler_base import DigitalOutputHandlerBase


class RpiGpioDigitalOutputHandler(DigitalOutputHandlerBase):
    
    def __init__(self,
                 pin: int,
                 name: Optional[str] = None) -> None:
        super().__init__(pin, name=name)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.OUTPUT)
        
    def set_high(self) -> None:
        GPIO.output(self._pin, GPIO.HIGH)
        
    def set_low(self) -> None:
        GPIO.output(self._pin, GPIO.LOW)
        