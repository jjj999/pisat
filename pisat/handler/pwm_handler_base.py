
from typing import Optional, Union

from pisat.handler.digital_io_handler_base import DigitalIOHandlerBase


class PWMHandlerBase(DigitalIOHandlerBase):
    
    DUTY_MAX = 100.
    DUTY_MIN = 0.
    
    def __init__(self,
                 pin: int,
                 freq: Union[int, float],
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            pin : int
                Number of pin which emits pwm signal
            freq : Union[int, float]
                Frequency of signal
            name : Optional[str], optional
                Name of the component, by default None
        """
        super().__init__(pin, name=name)
        
        self._freq = 0
        self._duty = 0.
        
        self.set_freq(freq) 
        
    @classmethod
    def is_valid_duty(cls, duty: Union[int, float]) -> bool:
        return cls.DUTY_MIN <= duty <= cls.DUTY_MAX       
    
    @property
    def duty(self) -> Union[int, float]:
        return self._duty
    
    @property
    def freq(self) -> Union[int, float]:
        return self._freq
    
    def set_duty(self, duty: Union[int, float]) -> None:
        """Set duty-cycle of pwm signal to be emitted.

        Parameters
        ----------
            duty : Union[int, float]
                Duty-cycle to be set
        """
        pass
    
    def set_freq(self, freq: Union[int, float]) -> None:
        """Set frequency of pwm signal to be emitted.

        Parameters
        ----------
            freq : Union[int, float]
                Frequency to be set
        """
        pass
    
    def start(self, duty: Optional[Union[int, float]] = None) -> None:
        """Start emitting pwm signal using current duty-cycle.

        Parameters
        ----------
            duty : Optional[Union[int, float]], optional
                Duty-cycle to be set before the start emitting, by default None
        """
        pass
    
    def stop(self) -> None:
        """Stop emitting pwm signal.
        
        This method only stops emitting signal, not reset the current duty-cycle.
        """
        pass
    