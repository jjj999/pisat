
from typing import Optional, Union

from pisat.util.platform import is_raspberry_pi
from pisat.handler.pwm_handler_base import PWMHandlerBase
from pisat.handler.rpigpio_digital_output_handler import RpiGpioDigitalOutputHandler

if is_raspberry_pi():
    from RPi import GPIO
    GPIO.setmode(GPIO.BCM)
    

class RpiGpioPWMHandler(PWMHandlerBase):            
    
    def __init__(self, 
                 pin: int, 
                 freq: float,
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            pin : int
                Number of pin which emits pwm signal
            freq : int
                Frequency of signal
            name : Optional[str], optional
                Name of the component, by default None
        """
        GPIO.setup(pin, GPIO.OUT)
        self._pwm = GPIO.PWM(pin, freq)
        
        super().__init__(pin, freq, name=name)
        
        self._is_start = False
        
    def close(self) -> None:
        """Clean up the pin used.
        """
        GPIO.cleanup(self._pin)
        
    def set_duty(self, duty: Union[int, float]) -> None:
        """Set duty-cycle of pwm signal to be emitted.

        Parameters
        ----------
            duty : Union[int, float]
                Duty-cycle to be set
        """
        if self.is_valid_duty(duty):
            self._duty = duty
            
            # NOTE
            # If the stert method has been already called and the 
            # stop not called, this method change duty-cycle and
            # apply the value to the signal. If the start has not
            # been called yet or the start not recalled, then
            # the method only change the current value of duty.
            if self._is_start:
                self._pwm.ChangeDutyCycle(duty)
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
        if freq >= 0.:
            self._pwm.ChangeFrequency(freq)
            self._freq = freq
        else:
            ValueError(
                "'freq' must be 0 and more."
            )
            
    def start(self, duty: Optional[Union[int, float]] = None) -> None:
        """Start emitting pwm signal using current duty-cycle.

        Parameters
        ----------
            duty : Optional[Union[int, float]], optional
                Duty-cycle to be set before the start emitting, by default None
        """
        if duty is not None:
            self.set_duty(duty)
            
        self._pwm.start(self._duty)
        self._is_start = True
        
    def stop(self) -> None:
        """Stop emitting pwm signal.
        
        This method only stops emitting signal, not reset the current duty-cycle.
        """
        # NOTE Read the docstring.
        self._pwm.stop()
        self._is_start = False
            