
from typing import Optional, Union

from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.handler.handler_base import HandlerBase
from pisat.model.datamodel import DataModelBase
from pisat.sensor.sensor_base import HandlerMismatchError, SensorBase
from pisat.sensor.serial_gps import SerialGPS


class UARTSamM8Q(SerialGPS):
    pass


# TODO I2C ver.
class I2CSamM8Q(SensorBase):
    pass


# TODO I2C ver.
class SamM8Q(SensorBase):
    
    DataModel: DataModelBase = SerialGPS.DataModel
    
    def __init__(self,
                 handler: Union[I2CHandlerBase, SerialHandlerBase],
                 name: Optional[str] = None) -> None:
        super().__init__(handler=handler, name=name)

        if isinstance(handler, SerialHandlerBase):
            self._base = UARTSamM8Q(handler=handler)
        elif isinstance(handler, I2CHandlerBase):
            self._base = I2CSamM8Q(handler=handler)
        else:
            raise HandlerMismatchError(
                "'handler' must be for UART or I2C."
            )
            
    def read(self):
        return self._base.read()
        