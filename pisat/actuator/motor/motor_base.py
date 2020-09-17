#! python3

"""

pisat.actuator.motor.motor_base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



[author]
Taiki Okada, From The Earth 10th @Tohoku univ.
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pigpio API
    http://abyz.me.uk/rpi/pigpio/python.html
    
"""

from typing import *

import pigpio as gpio

from pisat.base.component import Component


class UnablePWMmodeError(Exception):
    """Raised if tries to use pwm functions despite the pwm is unable"""


class MotorBase(Component):

    def __init__(self, 
                 pi:gpio.pi, 
                 fin:int, 
                 rin:int, 
                 freq:int=50000,
                 drange:int=1000,
                 pwm_fin=True,
                 pwm_rin=True,
                 cw_fin=True):
        
        """
        Parameters
        ----------
        pi : pigpio.pi
            pi object to handle a raspberry pi.
        fin : int
            pin number connected to FIN on a driver.
        rin : int
            pin number connected to RIN on a driver.
        freq : int, default 50000
            PWM frequency.
        drange : int, default 1000
            range of PWM duty. 
        pwm_fin : bool, default True
            whether using pwm mode on fin or not.
        pwm_rin : bool, default True
            whether using pwm mode on fin or not.
        cw_fin : bool, default True
            if give fin pwm pulse and turn clockwise, then True,
            else False.
        """
        
        # init instance variables
        self._pi:gpio.pi = pi
        self._fin:int = fin
        self._rin:int = rin
        self._freq:Optional[int] = None
        self._drange:Optional[int] = None
        self._is_pwm_fin:bool = pwm_fin
        self._is_pwm_rin:bool = pwm_rin
        self._is_cw_fin:bool = cw_fin
        
        # setting pins up
        self._pi.set_mode(self._fin, gpio.OUTPUT)
        self._pi.set_mode(self._rin, gpio.OUTPUT)
        
        # setting pwm
        if self._is_pwm_fin:
            
            self._freq = freq
            self._drange = drange
            
            self._pi.set_PWM_frequency(self._fin, self._freq)
            self._pi.set_PWM_range(self._fin, self._drange)
            
        if self._is_pwm_rin:
            self._pi.set_PWM_frequency(self._rin, self._freq)
            self._pi.set_PWM_range(self._rin, self._drange)
    
            
    @property
    def pin_fin(self):
        return self._fin
    
    
    @property
    def pin_rin(self):
        return self._rin
    
    
    @property
    def freq(self):
        return self._freq
    
    
    @property
    def duty_range(self):
        return self._drange
    
    
    def set_freq(self, freq:int) -> None:
        if self._is_pwm_fin or self._is_pwm_rin:
            raise UnablePWMmodeError("Pins were not setup as PWM mode.")
        
        if self._is_pwm_fin:
            self._pi.set_PWM_frequency(self._fin, freq)
        if self._is_pwm_rin:
            self._pi.set_PWM_frequency(self._rin, freq)
            
            
    def set_duty_range(self, drange:int) -> None:
        if self._is_pwm_fin or self._is_pwm_rin:
            raise UnablePWMmodeError("Pins were not setup as PWM mode.")
        
        if self._is_pwm_fin:
            self._pi.set_PWM_range(self._fin, drange)
        if self._is_pwm_rin:
            self._pi.set_PWM_range(self._rin, drange)
    
    
    def onoff(self, fin:bool, rin:bool) -> None:
        self._pi.write(self._fin, int(fin))
        self._pi.write(self._rin, int(rin))
    
    
    def standby(self) -> None:
        # if this code doesn't work, should divide pwm mode and on-off mode
        self.onoff(False, False)
        
        
    def brake(self):
        self.onoff(True, True)
        
        
    def pwm(self, fin:Union[int, bool], rin:Union[int, bool]) -> None:
        
        if isinstance(fin, int):
            if self._is_pwm_fin:
                self._pi.set_PWM_dutycycle(self._fin, fin)
            else:
                raise UnablePWMmodeError("FIN's pin was not setup as PWM mode.")
        else:
            self._pi.write(self._fin, int(fin))
        
        if isinstance(rin, int):
            if self._is_pwm_rin:
                self._pi.set_PWM_dutycycle(self._rin, rin)
            else:
                raise UnablePWMmodeError("FIN's pin was not setup as PWM mode.")
        else:
            self._pi.write(self._rin, int(rin))
    
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -    
    #   clockwise, counterclockwise
    #   
    #   NOTE
    #   1. Problem about not matching pwm mode  
    #       This problem is solved at this level, so don't have to take
    #       take care of it at higher levels than here.
    #
    #   2. Which direction is clockwise and counterclockwise?
    #       We defines the clockwise is clockwise direction when you see
    #       terminals of a motor. 
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    def cw(self, duty:Union[int, bool]) -> None:
        if self._is_cw_fin:
            self.pwm(duty, False)
        else:
            self.pwm(True, duty)

        
    def ccw(self, duty:Union[int, bool]) -> None:
        if self._is_cw_fin:
            self.pwm(False, duty)
        else:
            self.pwm(duty, True)
