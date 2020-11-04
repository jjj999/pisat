
from typing import Optional, Dict, List, Tuple

from pisat.config.type import Logable
from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.sensor.sensor_base import SensorBase
from pisat.util.gps_parser import GPSParser
from pisat.config.dname import (
    GPS_ALTITUDE_GEOID,
    GPS_ALTITUDE_GEOID_UNIT,
    GPS_ALTITUDE_SEALEVEL,
    GPS_ALTITUDE_SEALEVEL_UNIT,
    GPS_ANGLE_AZIMUTH_SATTELITE,
    GPS_ANGLE_ELEVATION_SATTELITE,
    GPS_ANGLE_TWONORTH_EW,
    GPS_BODY_MAGNETIC_ANGLE_VELOCITY,
    GPS_BODY_TRUE_ANGLE_VELOCITY,
    GPS_BODY_VELOCITY_KM,
    GPS_BODY_VELOCITY_KNOT,
    GPS_CHECK_SUM,
    GPS_DATE_UTC,
    GPS_DIFF_ANGLE_TWONORTH,
    GPS_ID_DIFF_POINT,
    GPS_LATITUDE,
    GPS_LATITUDE_NS,
    GPS_LONGITUDE,
    GPS_LONGITUDE_EW,
    GPS_MODE,
    GPS_NUMBER_SATELLITE,
    GPS_HOWMANY_SATELLITES_IN_VIEW,
    GPS_HOWMANY_SENTENCES_GSV,
    GPS_NUMBER_SENTENCE_GSV,
    GPS_NUMBERS_SATELLITE,
    GPS_HOWMANY_SATELLITES_USED,
    GPS_QUALITY_POSITION,
    GPS_RATE_DECLINE_QUALITY_HORIZONTAL,
    GPS_RATE_DECLINE_QUALITY_POSITION,
    GPS_RATE_DECLINE_QUALITY_VERTICAL,
    GPS_RATIO_CARRIER_NOISE, 
    GPS_SATELLITE_INFO,
    GPS_STATUS,
    GPS_TIME_FROM_LATEST_DGPS,
    GPS_TIME_UTC,
    GPS_TYPE_DETECT
)


class SerialGPS(SensorBase):
    
    DATA_NAMES = (
        GPS_ALTITUDE_GEOID,
        GPS_ALTITUDE_GEOID_UNIT,
        GPS_ALTITUDE_SEALEVEL,
        GPS_ALTITUDE_SEALEVEL_UNIT,
        GPS_ANGLE_AZIMUTH_SATTELITE,
        GPS_ANGLE_ELEVATION_SATTELITE,
        GPS_ANGLE_TWONORTH_EW,
        GPS_BODY_MAGNETIC_ANGLE_VELOCITY,
        GPS_BODY_TRUE_ANGLE_VELOCITY,
        GPS_BODY_VELOCITY_KM,
        GPS_BODY_VELOCITY_KNOT,
        GPS_CHECK_SUM,
        GPS_DATE_UTC,
        GPS_DIFF_ANGLE_TWONORTH,
        GPS_ID_DIFF_POINT,
        GPS_LATITUDE,
        GPS_LATITUDE_NS,
        GPS_LONGITUDE,
        GPS_LONGITUDE_EW,
        GPS_MODE,
        GPS_NUMBER_SATELLITE,
        GPS_HOWMANY_SATELLITES_IN_VIEW,
        GPS_HOWMANY_SENTENCES_GSV,
        GPS_NUMBER_SENTENCE_GSV,
        GPS_NUMBERS_SATELLITE,
        GPS_HOWMANY_SATELLITES_USED,
        GPS_QUALITY_POSITION,
        GPS_RATE_DECLINE_QUALITY_HORIZONTAL,
        GPS_RATE_DECLINE_QUALITY_POSITION,
        GPS_RATE_DECLINE_QUALITY_VERTICAL,
        GPS_RATIO_CARRIER_NOISE, 
        GPS_SATELLITE_INFO,
        GPS_STATUS,
        GPS_TIME_FROM_LATEST_DGPS,
        GPS_TIME_UTC,
        GPS_TYPE_DETECT
    )
    
    def __init__(self,
                 handler: SerialHandlerBase,
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        if not isinstance(handler, SerialHandlerBase):
            raise TypeError(
                "'handler' must be SerialHandlerBase."
            )
        super().__init__(handler=handler, debug=debug, name=name)

        self._handler: SerialHandlerBase = handler
        
    def clear_buf(self):
        self._handler.readlines(end=GPSParser.Sentense.TERMINOR.value)
        
    def _load_data(self) -> Dict[str, Logable]:
        data = {}
        for line in self._handler.readlines(end=GPSParser.Sentense.TERMINOR.value):
            data.update(GPSParser.parse(line))
            
        for dname in self.dnames:
            if dname not in data:
                data[dname] = None
                
        return data
    
    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        debugging = super().readf(*dnames)
        if debugging:
            return debugging
        
        data = self._load_data()
        if len(dnames) == 0:
            return list(data.values())
        else:
            res = []
            for dname in dnames:
                if dname in self.dnames:
                    res.append(data[dname])
            return res
        
    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        debugging = super().readf(*dnames)
        if debugging:
            return debugging
        
        data = self._load_data()
        if len(dnames) == 0:
            return data
        else:
            res = {}
            for dname in dnames:
                if dname in self.dnames:
                    res[dname] = data[dname]
            return res
