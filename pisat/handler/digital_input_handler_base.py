
from typing import Optional
from pisat.handler.digital_io_handler_base import DigitalIOHandlerBase


class DigitalInputHandlerBase(DigitalIOHandlerBase):
    
    def __init__(self, 
                 pin: int, 
                 pullup: bool = False,
                 pulldown: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._pin: int = pin
        
        if pullup and pulldown:
            raise ValueError(
                "'pullup' and 'pulldown' must not be True at once."
            )
        if pullup:
            self.set_pull_up_down(pulldown=False)
        elif pulldown:
            self.set_pull_up_down(pulldown=True)
    
    def set_pull_up_down(self, pulldown: bool = False) -> None:
        pass
    
    def clear_pull_up_down(self) -> None:
        pass
    
    def observe(self) -> bool:
        pass