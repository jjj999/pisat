
from typing import Optional

from RPi import GPIO

from pisat.handler.digital_input_handler_base import DigitalInputHandlerBase


class RpiGpioDigitalInputHandler(DigitalInputHandlerBase):
    
    def __init__(self,
                 pin: int,
                 pullup: bool = False,
                 pulldown: bool = False,
                 name: Optional[str] = None) -> None:
        
        GPIO.setmode(GPIO.BCM)
        
        super().__init__(pin, name=name)
        
        # Setup default mode.
        if not (pullup or pulldown):
            GPIO.setup(pin, GPIO.IN)
        
    def close(self) -> None:
        GPIO.cleanup(self._pin)
        
    def set_pull_up_down(self, pulldown: bool) -> None:
        if pulldown:
            GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
    def clear_pull_up_down(self) -> None:
        # TODO Find better way
        GPIO.clean(self._pin)
        GPIO.setup(self._pin, GPIO.IN)
        
    def observe(self) -> bool:
        return bool(GPIO.input(self._pin))
        