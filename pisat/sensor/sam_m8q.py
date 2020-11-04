
from typing import Dict, List, Optional, Tuple

from pisat.config.type import Logable
from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.handler.handler_base import HandlerBase
from pisat.sensor.sensor_base import HandlerMismatchError, SensorBase
from pisat.sensor.serial_gps import SerialGPS


class UARTSamM8Q(SerialGPS):
    pass


class I2CSamM8Q(SensorBase):
    pass


# TODO Confirm UART signals
class SamM8Q(SensorBase):
    
    def __init__(self,
                 handler: Optional[HandlerBase] = None,
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(handler=handler, debug=debug, name=name)
        
        if debug:
            return
        
        if isinstance(handler, SerialHandlerBase):
            self._base = UARTSamM8Q(handler=handler)
        elif isinstance(handler, I2CHandlerBase):
            self._base = I2CSamM8Q(handler=handler)
        else:
            raise HandlerMismatchError(
                "'handler' must be for UART or I2C."
            )
            
    # TODO
    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        pass
    
    # TODO
    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        pass
        