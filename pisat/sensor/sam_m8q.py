
from typing import Optional, Tuple, Union

from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.model.datamodel import DataModelBase, loggable
from pisat.sensor.sensor_base import HandlerMismatchError, SensorBase
from pisat.sensor.serial_gps import SerialGPS


class UARTSamM8Q(SerialGPS):
    pass


# TODO I2C ver.
class I2CSamM8Q(SensorBase):
    pass


# TODO I2C ver.
class SamM8Q(SensorBase):
    
    class DataModel(DataModelBase):
        
        def setup(self, 
                  time_utc: Optional[Tuple[Union[int, float]]] = None,
                  latitude: Optional[float] = None,
                  longitude: Optional[float] = None,
                  altitude: Optional[float] = None):
            self._time_utc = time_utc
            self._latitude = latitude
            self._longitude = longitude
            self._altitude = altitude
        
        @loggable
        def time_utc(self):
            return self._time_utc
        
        @time_utc.formatter
        def time_utc(self):
            name = self.get_tag("time_utc")
            value = None
            if self._time_utc is not None:
                value = f"{self._time_utc[0]}:{self._time_utc[1]}:{self._time_utc[2]}"
            return {name: value}
        
        @loggable
        def latitude(self):
            return self._latitude
        
        @loggable
        def longitude(self):
            return self._longitude
        
        @loggable
        def altitude(self):
            return self._altitude
    
    
    def __init__(self,
                 handler: Union[I2CHandlerBase, SerialHandlerBase],
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)

        if isinstance(handler, SerialHandlerBase):
            self._base = UARTSamM8Q(handler=handler)
        elif isinstance(handler, I2CHandlerBase):
            self._base = I2CSamM8Q(handler=handler)
        else:
            raise HandlerMismatchError(
                "'handler' must be for UART or I2C."
            )
            
        self._handler = handler
            
    def read(self):
        return self._base.read()
        