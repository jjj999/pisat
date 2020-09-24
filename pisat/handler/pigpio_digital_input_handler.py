
from typing import Optional

from pisat.util.platform import is_raspberry_pi
from pisat.handler.digital_input_handler_base import DigitalInputHandlerBase

if is_raspberry_pi():
    import pigpio


class PigpioDigitalInputHandler(DigitalInputHandlerBase):
    
    def __init__(self, 
                 pi,
                 pin: int,
                 pullup: bool = False,
                 pulldown: bool = False,
                 name: Optional[str] = None) -> None:
        
        self._pi: pigpio.pi = pi
        self._pi.set_mode(pin, pigpio.INPUT)
        
        super().__init__(pin, pullup=pullup, pulldown=pulldown, name=name)
    
    def set_pull_up_down(self, pulldown: bool = False) -> None:
        if pulldown:
            self._pi.set_pull_up_down(self._pin, pigpio.PUD_DOWN)
        else:
            self._pi.set_pull_up_down(self._pin, pigpio.PUD_UP)
    
    def clear_pull_up_down(self) -> None:
        self._pi.set_pull_up_down(self._pin, pigpio.PUD_DOWN)
    
    def observe(self) -> bool:
        return bool(self._pi.read(self._pin))
        