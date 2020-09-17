

from typing import Dict, Optional, Tuple

from pisat.config.type import Logable
from pisat.config.dname import *
from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.sensor.sensor_base import SensorBase


class Bno055(SensorBase):
    
    DATA_NAMES: Tuple[str] = ()
    DEFAULT_VALUES: Dict[str, Logable]
    
    #   RESISTOR ADDRESS
    
    def __init__(self,
                 handler: Optional[I2CHandlerBase] = None,
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(handler=handler, debug=debug, name=name)
        if debug:
            return
        
    
