

from typing import Union

from pisat.base.component import Component


class RotateMotorDriverBase(Component):
    
    # TODO to be overrided
    def cw(self, param: Union[int, float]) -> None:
        pass
    
    # TODO to be overrided
    def ccw(self, param: Union[int, float]) -> None:
        pass
    
    # TODO to be overrided
    def brake(self) -> None:
        pass
    
    # TODO to be overrided
    def standby(self) -> None:
        pass
    