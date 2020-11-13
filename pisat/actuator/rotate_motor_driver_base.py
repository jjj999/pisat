

from typing import Union

from pisat.actuator.motor_driver_base import MotorDriverBase


class RotateMotorDriverBase(MotorDriverBase):
    
    # TODO to be overrided
    def cw(self, param: Union[int, float]) -> None:
        pass
    
    # TODO to be overrided
    def ccw(self, param: Union[int, float]) -> None:
        pass