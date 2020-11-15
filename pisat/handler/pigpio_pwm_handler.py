
from typing import Optional, Union

from pisat.util.platform import is_raspberry_pi
from pisat.handler.pwm_handler_base import PWMHandlerBase

if is_raspberry_pi():
    import pigpio
    

class PigpioPWMHandler(PWMHandlerBase):
    
    RANGE_MAX = 40000
    RANGE_MIN = 25
    
    def __init__(self, 
                 pi,
                 pin: int,
                 freq: int,
                 range: int = 40000,
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            pi : pigpio.pi
                Interface to GPIO
            pin : int
                Number of pin which emits pwm signal
            freq : int
                Frequency of signal
            range: int
                Resolution of duty-cycle, by default 40000
            name : Optional[str], optional
                Name of the component, by default None
        """
        self._pi = pi
        
        super().__init__(pin, freq, name=name)
        
        self._range = range
        self._is_start = False
        self.set_range(self._range)
        
    @staticmethod
    def calc_true_duty(range: int, duty: Union[int, float]) -> int:
        result = int(duty / 100 * range)
        
        # compensation to be in the tolerance
        if result > range:
            result = range
        elif result < 0:
            result = 0
            
        return result
        
    @classmethod
    def is_valid_range(cls, range: int) -> bool:
        return cls.RANGE_MIN <= range <= cls.RANGE_MAX
    
    @property
    def range(self) -> int:
        return self._range
        
    def set_duty(self, duty: Union[int, float]) -> None:
        """Set duty-cycle of pwm signal to be emitted.

        Parameters
        ----------
            duty : Union[int, float]
                Duty-cycle to be set
        """
        if self.is_valid_duty(duty):
            self._duty = duty
            
            # calculating a true value for the interface of pigpio
            duty_true = self.calc_true_duty(self._range, duty)
            
            # NOTE
            # If the stert method has been already called and the 
            # stop not called, this method change duty-cycle and
            # apply the value to the signal. If the start has not
            # been called yet or the start not recalled, then
            # the method only change the current value of duty.
            if self._is_start:
                self._pi.set_PWM_dutycycle(self._pin, duty_true)
        else:
            ValueError(
                f"'duty' must be {self.DUTY_MIN} <= 'duty' <= {self.DUTY_MAX}."
            )
    
    def set_freq(self, freq: int) -> None:
        """Set frequency of pwm signal to be emitted.

        Parameters
        ----------
            freq : int
                Frequency to be set
        """
        result = self._pi.set_PWM_frequency(self._pin, freq)
        self._freq = result
        
    def set_range(self, range: int) -> None:
        """Change resolution of value of duty-cycle.
        
        The bigger given range is, the better resolution duty-cycle has.
        The max value is 40000, min 25.

        Parameters
        ----------
            range : int
                Resolution of duty-cycle
        """
        if self.is_valid_range(range):
            self._pi.set_PWM_range(self._pin, range)
            self._range = range
        else:
            ValueError(
                f"'range' must be {self.RANGE_MIN} <= 'range' <= {self.RANGE_MAX}."
            )
        
    def start(self, duty: Optional[Union[int, float]] = None) -> None:
        """Start emitting pwm signal using current duty-cycle.

        Parameters
        ----------
            duty : Optional[Union[int, float]], optional
                Duty-cycle to be set before the start emitting, by default None
        """
        self._is_start = True
        if duty is not None:
            self.set_duty(duty)
        
        true_duty = self.calc_true_duty(self._range, self._duty)
        self._pi.set_PWM_dutycycle(self._pin, true_duty)
            
    def stop(self) -> None:
        """Stop emitting pwm signal.
        
        This method only stops emitting signal, not reset the current duty-cycle.
        """
        # NOTE Read the docstring.
        self._pi.set_PWM_dutycycle(self._pin, 0)
        self._is_start = False
        