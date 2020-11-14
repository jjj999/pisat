

from typing import Optional, Tuple, Union

from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.model.datamodel import DataModelBase, loggable
from pisat.sensor.sensor_base import SensorBase
from pisat.util.nmea import NMEAParser


class SerialGPS(SensorBase):
    
    FORMAT_GGA = "GGA"
    FORMAT_GLL = "GLL"
    FORMAT_RMC = "RMC"
    FORMAT_ZDA = "ZDA"
    
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
                 handler: SerialHandlerBase,
                 name: Optional[str] = None) -> None:
        if not isinstance(handler, SerialHandlerBase):
            raise TypeError(
                "'handler' must be SerialHandlerBase."
            )
        super().__init__(handler=handler, name=name)

        self._handler: SerialHandlerBase = handler
        self._parser: NMEAParser = NMEAParser(self.name)
        
    def read(self):
        sentence = self._handler.readline()
        data = self._parser.parse(sentence)
        
        model = self.DataModel(self.name)
        if data is None:
            model.setup()
        elif data.type == self.FORMAT_GGA:
            model.setup(time_utc=data.time_utc, 
                        latitude=data.latitude,
                        longitude=data.longitude,
                        altitude=data.altitude)
        elif data.type == self.FORMAT_GLL:
            model.setup(time_utc=data.time_utc,
                        latitude=data.latitude,
                        longitude=data.longitude)
        elif data.type == self.FORMAT_RMC:
            model.setup(time_utc=data.time_utc,
                        latitude=data.latitude,
                        longitude=data.longitude)
        elif data.type == self.FORMAT_ZDA:
            model.setup(time_utc=data.time_utc)
            
        return model
