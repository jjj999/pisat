

import re
from typing import Dict, Optional, Tuple, Type, Union

from pisat.model.datamodel import DataModelBase, loggable
from pisat.util.type import empty_None


class NMEAModelBase(DataModelBase):
    
        FORMAT: str = None
        NUM_FIELDS: int = 0
        
        def setup(self, fields: Tuple[str]):           
            self._talker = fields[0][:2]
            self._type = fields[0][2:]
            self._checksum = empty_None(fields[-1])
        
        @loggable
        def talker(self):
            return self._talker
        
        @loggable
        def type(self):
            return self._type
        
        @loggable
        def checksum(self):
            return self._checksum
        
        @classmethod
        def calc_time_utc(cls, raw: str) -> Tuple[Union[int, float]]:
            hour, min, sec = raw[:2], raw[2:4], raw[4:]
            return (int(hour), int(min), float(sec))
        
        @classmethod
        def calc_date_utc(cls, raw: str) -> Tuple[Union[int]]:
            day, month, year = raw[:2], raw[:4], raw[4:]
            return (int(day), int(month), int(year))
        
        @classmethod
        def calc_latitude(cls, value: str, ns: str) -> float:
            d, m = float(value[:-8]), float(value[-8:])
            degree = d + m / 60
            if ns == "S":
                degree = - degree
            return degree
        
        @classmethod
        def calc_longitude(cls, value: str, ew: str) -> float:
            d, m = float(value[:-8]), float(value[-8:])
            degree = d + m / 60
            if ew == "W":
                degree = - degree
            return degree
        
        @classmethod
        def format_time_utc(cls, pub_name: str, time_utc: Optional[Tuple[Union[int, float]]]) -> Dict[str, str]:
            name = f"{pub_name}-time_utc"
            value = None
            if time_utc is not None:
                value = f"{time_utc[0]}:{time_utc[1]}:{time_utc[2]}"
            return {name: value}
        
        @classmethod
        def format_date_utc(cls, pub_name: str, date_utc: Optional[Tuple[int]]) -> Dict[str, str]:
            name = f"{pub_name}-date_utc"
            value = None
            if date_utc is not None:
                value = f"{date_utc[2]}.{date_utc[1]}.{date_utc[0]}"
            return {name: value}

        
class GGAModel(NMEAModelBase):
        
    FORMAT = "GGA"
    NUM_FIELDS = 16
    
    def setup(self, fields: Tuple[str]):
        super().setup(fields)
        
        time_utc = empty_None(fields[1])
        latitude = empty_None(fields[2])
        latitude_ns = empty_None(fields[3])
        longitude = empty_None(fields[4])
        longitude_ew = empty_None(fields[5])
        
        self._time_utc: Optional[Tuple[Union[int, float]]] = None
        self._latitude: Optional[float] = None
        self._longitude: Optional[float] = None
        self._quality: Optional[int] = empty_None(fields[6], int)
        self._satellites_used: Optional[int] = empty_None(fields[7], int)
        self._HDOP: Optional[float] = empty_None(fields[8], float)
        self._altitude: Optional[float] = empty_None(fields[9], float)
        self._geoidal_separation: Optional[float] = empty_None(fields[11], float)
        self._station_id: Optional[float] = empty_None(fields[14], int)
        
        if time_utc is not None:
            self._time_utc = self.calc_time_utc(time_utc)
        if latitude is not None and latitude_ns is not None:
            self._latitude = self.calc_latitude(latitude, latitude_ns)
        if longitude is not None and longitude_ew is not None:
            self._longitude = self.calc_longitude(longitude, longitude_ew)
        
    @loggable
    def time_utc(self):
        return self._time_utc
    
    @time_utc.formatter
    def time_utc(self):
        return self.format_time_utc(self.publisher, self._time_utc)
    
    @loggable
    def latitude(self):
        return self._latitude
    
    @loggable
    def longitude(self):
        return self._longitude
    
    @loggable
    def quality(self):
        return self._quality
    
    @loggable
    def satellites_used(self):
        return self._satellites_used
    
    @loggable
    def HDOP(self):
        return self._HDOP
    
    @loggable
    def altitude(self):
        return self._altitude
    
    @loggable
    def geoidal_separation(self):
        return self._geoidal_separation
    
    @loggable
    def station_id(self):
        return self._station_id
        
        
class GLLModel(NMEAModelBase):
    
    FORMAT = "GLL"
    NUM_FIELDS = 9
    
    def setup(self, fields: Tuple[str]):
        super().setup(fields)
        
        latitude = empty_None(fields[1])
        latitude_ns = empty_None(fields[2])
        longitude = empty_None(fields[3])
        longitude_ew = empty_None(fields[4])
        time_utc = empty_None(fields[5])
        
        self._latitude: Optional[float] = None
        self._longitude: Optional[float] = None
        self._time_utc: Optional[Tuple[Union[int, float]]] = None
        self._status = empty_None(fields[6])
        
        if latitude is not None and latitude_ns is not None:
            self._latitude = self.calc_latitude(latitude, latitude_ns)
        if longitude is not None and longitude_ew is not None:
            self._longitude = self.calc_longitude(longitude, longitude_ew)
        if time_utc is not None:
            self._time_utc = self.calc_time_utc(time_utc)
        
    @loggable
    def latitude(self):
        return self._latitude
    
    @loggable
    def longitude(self):
        return self._longitude
    
    @loggable
    def time_utc(self):
        return self._time_utc
    
    @time_utc.formatter
    def time_utc(self):
        return self.format_time_utc(self.publisher, self._time_utc)
    
    @loggable
    def status(self):
        return self._status
        
    
class GSAModel(NMEAModelBase):
    
    FORMAT = "GSA"
    NUM_FIELDS = 19
        
    def setup(self, fields: Tuple[str]):
        super().setup(fields)
        
        self._mode = empty_None(fields[1])
        self._fix_type = empty_None(fields[2])
        
        self._satellite_id = tuple([empty_None(id, int) for id in fields[3:15]])
        self._PDOP = empty_None(fields[15], float)
        self._HDOP = empty_None(fields[16], float)
        self._VDOP = empty_None(fields[17], float)
        
    @loggable
    def mode(self):
        return self._mode
    
    @mode.formatter
    def mode(self):
        return {f"{self.publisher}-GSA_mode": self._mode}
    
    @loggable
    def fix_type(self):
        return self._fix_type
    
    @fix_type.formatter
    def fix_type(self):
        return {f"{self.publisher}-GSA_fix_type": self._fix_type}
    
    @loggable
    def satellite_id(self):
        return self._satellite_id
    
    @satellite_id.formatter
    def satellite_id(self):
        names = [f"{self.publisher}-satellite_id_{num}" for num in range(1, 13)]                
        return {name: val for name, val in zip(names, self._satellite_id)}
    
    @loggable
    def PDOP(self):
        return self._PDOP
    
    @loggable
    def HDOP(self):
        return self._HDOP

    @loggable
    def VDOP(self):
        return self._VDOP
        
    
class GSVModel(NMEAModelBase):
    
    FORMAT = "GSV"
    
    
    class SatelliteProperty:
        
        def __init__(self, id: str = "", elev: str = "", azim: str = "", SNR: str = "") -> None:
            self._id = empty_None(id, int)
            self._elev = empty_None(elev, int)
            self._azim = empty_None(azim, int)
            self._SNR= empty_None(SNR, int)
            
        @property
        def id(self):
            return self._id
        
        @property
        def elevation(self):
            return self._elev
        
        @property
        def azimuth(self):
            return self._azim
        
        @property
        def SNR(self):
            return self._SNR
        
        def format(self, gen: str, name: str):
            return {f"{gen}-{name}_id": f"{self._id}",
                    f"{gen}-{name}_elevation": f"{self._elev}",
                    f"{gen}-{name}_azimuth": f"{self._azim}",
                    f"{gen}-{name}_SNR": f"{self._SNR}"}
    
    
    def setup(self, fields: Tuple[str]):
        super().setup(fields)
        
        self._num_message = empty_None(fields[1], int)
        self._seq_num = empty_None(fields[2], int)
        self._satellites_in_view = empty_None(fields[3], int)
        self._satellite_1 = None
        self._satellite_2 = None
        self._satellite_3 = None
        self._satellite_4 = None
        
        # NOTE a length of the GSV format is changable. 
        if len(fields) > 8:
            self._satellite_1 = self.SatelliteProperty(fields[4], fields[5], fields[6], fields[7])
        else:
            self._satellite_1 = self.SatelliteProperty()
        if len(fields) > 12:
            self._satellite_2 = self.SatelliteProperty(fields[8], fields[9], fields[10], fields[11])
        else:
            self._satellite_2 = self.SatelliteProperty()
        if len(fields) > 16:
            self._satellite_3 = self.SatelliteProperty(fields[12], fields[13], fields[14], fields[15])
        else:
            self._satellite_3 = self.SatelliteProperty()
        if len(fields) > 20:
            self._satellite_4 = self.SatelliteProperty(fields[16], fields[17], fields[18], fields[19])
        else:
            self._satellite_4 = self.SatelliteProperty()
        
    @loggable
    def num_message(self):
        return self._num_message
    
    @loggable
    def seq_num(self):
        return self._seq_num
    
    @loggable
    def satellites_in_view(self):
        return self._satellites_in_view
    
    @loggable
    def satellite_1(self):
        return self._satellite_1
    
    @satellite_1.formatter
    def satellite_1(self):
        return self._satellite_1.format(self.publisher, "satellite1")
    
    @loggable
    def satellite_2(self):
        return self._satellite_2
    
    @satellite_2.formatter
    def satellite_2(self):
        return self._satellite_2.format(self.publisher, "satellite2")
    
    @loggable
    def satellite_3(self):
        return self._satellite_3
    
    @satellite_3.formatter
    def satellite_3(self):
        return self._satellite_3.format(self.publisher, "satellite3")
    
    @loggable
    def satellite_4(self):
        return self._satellite_4
    
    @satellite_4.formatter
    def satellite_4(self):
        return self._satellite_4.format(self.publisher, "satellite4")
    
    
class RMCModel(NMEAModelBase):
    
    FORMAT = "RMC"
    NUM_FIELDS = 14
    
    def setup(self, fields: Tuple[str]):
        super().setup(fields)
        
        time_utc = empty_None(fields[1])
        latitude = empty_None(fields[3])
        latitude_ns = empty_None(fields[4])
        longitude = empty_None(fields[5])
        longitude_ew = empty_None(fields[6])
        date_utc = empty_None(fields[9])
        
        self._time_utc = None
        self._status = empty_None(fields[2])
        self._latitude = None
        self._longitude = None
        self._speed_knots = empty_None(fields[7], float)
        self._true_course = empty_None(fields[8], float)
        self._date_utc = None
        self._mode = empty_None(fields[12])
        
        if time_utc is not None:
            self._time_utc = self.calc_time_utc(time_utc)
        if latitude is not None and latitude_ns is not None:
            self._latitude = self.calc_latitude(latitude, latitude_ns)
        if longitude is not None and longitude_ew is not None:
            self._longitude = self.calc_longitude(longitude, longitude_ew)
        if date_utc is not None:
            self._date_utc = self.calc_date_utc(date_utc)
    
    @loggable
    def time_utc(self):
        return self._time_utc
    
    @time_utc.formatter
    def time_utc(self):
        return self.format_time_utc(self.publisher, self._time_utc)
    
    @loggable
    def status(self):
        return self._status
    
    @loggable
    def latitude(self):
        return self._latitude
    
    @loggable
    def longitude(self):
        return self._longitude
    
    @loggable
    def speed_knots(self):
        return self._speed_knots
    
    @loggable
    def true_course(self):
        return self._true_course
    
    @loggable
    def date_utc(self):
        return self._date_utc
    
    @date_utc.formatter
    def date_utc(self):
        return self.format_date_utc(self.publisher, self._date_utc)
    
    @loggable
    def mode(self):
        return self._mode
    
    
class VTGModel(NMEAModelBase):
    
    FORMAT = "VTG"
    NUM_FIELDS = 11
    
    def setup(self, fields: Tuple[str]):
        super().setup(fields)
        
        self._true_course = empty_None(fields[1], float)
        self._mag_course = empty_None(fields[3], float)
        self._speed_knots = empty_None(fields[5], float)
        self._speed_km = empty_None(fields[7], float)
        self._mode = empty_None(fields[9])
        
    @loggable
    def true_course(self):
        return self._true_course
    
    @loggable
    def mag_course(self):
        return self._mag_course
    
    @loggable
    def speed_km(self):
        return self._speed_km
    
    @loggable
    def speed_knots(self):
        return self._speed_knots
    
    @loggable
    def mode(self):
        return self._mode
    
    
class ZDAModel(NMEAModelBase):
    
    FORMAT = "ZDA"
    NUM_FIELDS = 8
    
    def setup(self, fields: Tuple[str]):
        super().setup(fields)
        
        time_utc = empty_None(fields[1])
        day = empty_None(fields[2], int)
        month = empty_None(fields[3])
        year = empty_None(fields[4][2:])

        self._time_utc = None        
        self._date_utc = None
        self._local_zone_hour = empty_None(fields[5], int)
        self._local_zone_min = empty_None(fields[6], int)
        
        if time_utc is not None:
            self._time_utc = self.calc_time_utc(time_utc)
        if day is not None and month is not None and year is not None:
            self._date_utc = (day, month, year)
        
    @loggable
    def time_utc(self):
        return self._time_utc
    
    @time_utc.formatter
    def time_utc(self):
        return self.format_time_utc(self.publisher, self._time_utc)
    
    @loggable
    def date_utc(self):
        return self._date_utc
    
    @date_utc.formatter
    def date_utc(self):
        return self.format_date_utc(self.publisher, self._date_utc)
    
    @loggable
    def local_zone_hour(self):
        return self._local_zone_hour
    
    @loggable
    def local_zone_min(self):
        return self._local_zone_min
    
    
TYPE_MODELS = Union[GGAModel, GLLModel, GSAModel, GSVModel, RMCModel, VTGModel, ZDAModel, None]
TYPE_MODELCLASS = Union[Type[GGAModel], Type[GLLModel], Type[GSAModel], Type[GSVModel],
                        Type[RMCModel], Type[VTGModel], Type[ZDAModel]]


class NMEAParser:
    
    HEAD = "$"
    TAIL = "\r\n"
    DELIMITER_FILED = ","
    DELIMITER_CHECKSUM = "*"
    DELIMITER_PATTERN = "[,*]"
        
    MODELS: Dict[bytes, TYPE_MODELCLASS] = {GGAModel.FORMAT: GGAModel, GLLModel.FORMAT: GLLModel, 
                                            GSAModel.FORMAT: GSAModel, GSVModel.FORMAT: GSVModel, 
                                            RMCModel.FORMAT: RMCModel, VTGModel.FORMAT: VTGModel,
                                            ZDAModel.FORMAT: ZDAModel}
    
    def __init__(self, comp_name: str) -> None:
        self._comp_name = comp_name
        
    def parse(self, sentence: bytes) -> TYPE_MODELS:
        
        try:
            sentence = sentence.decode()
        except UnicodeDecodeError:
            return None
            
        if len(sentence) < 5:
            return None
        if sentence[0] != self.HEAD or sentence[-2:] != self.TAIL:
            return None
                
        fields = re.split(self.DELIMITER_PATTERN, sentence[1:-2])
        modeltype = self.MODELS.get(fields[0][2:])
        if modeltype is None:
            return None
        # a length of the GSV format is changable, but the others not.
        if modeltype != GSVModel and len(fields) != modeltype.NUM_FIELDS:
            return None
                 
        model = modeltype(self._comp_name)
        model.setup(fields)
        return model
