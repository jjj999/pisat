#! python3

"""

pisat.sensor.sensor.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION


[author]
AUTHOR NAME, ORGANIZATION NAME

[info]
OTHER INFORMATION
    
"""

from math import radians
from typing import Dict, Optional, Union, Tuple
from enum import Enum

from pisat.config.type import Logable
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


class GpsDataModelBuilder:

    class GGAModel:
        
        FORMAT = b"GGA"
        
        def __init__(self, sentence: bytes) -> None:
            pass
        
    class GLLModel:
        
        FORMAT = b"GLL"
        
        def __init__(self, sentence: bytes) -> None:
            pass
        
    class GSAModel:
        
        FORMAT = b"GSA"
        
        def __init__(self, sentence: bytes) -> None:
            pass
        
    class GSVModel:
        
        FORMAT = b"GSV"
        
        def __init__(self, sentence: bytes) -> None:
            pass
        
    class RMCModel:
        
        FORMAT = b"RMC"
        
        def __init__(self, sentence: bytes) -> None:
            pass
        
    class VTGModel:
        
        FORMAT = b"VTG"
        
        def __init__(self, sentence: bytes) -> None:
            pass
        
    class ZDAModel:
        
        FORMAT = b"ZDA"
        
        def __init__(self, sentence: bytes) -> None:
            pass
        
    MODELS = (GGAModel, GLLModel, GSAModel, GSVModel, RMCModel, VTGModel, ZDAModel)
        
    @classmethod
    def build(cls, format_name: bytes):
        model_obj = None
        for model in cls.MODELS:
            if format_name == model.FORMAT:
                target = model()


class GPSParser:

    class Sentense(Enum):
        HEAD = b"$"
        SEPARATOR = b","
        SEPARATOR_LAST = b"*"
        TERMINOR = b"\r\n"
        
        @classmethod
        def is_valid(cls, sentence: bytes) -> bool:
            if sentence.startswith(cls.HEAD.value):
                return True
            else:
                return False

    class Type(Enum):
        GPRMC = "GPRMC"
        GPGGA = "GPRMC"
        GPGSA = "GPRMC"
        GPGSV = "GPRMC"
        GPVTG = "GPRMC"
        AVAILABLES = (GPRMC, GPGGA, GPGSA, GPGSV, GPVTG)
        LENGTH = 5
        
        SIZE_GPRMC = 13
        SIZE_GPGGA = 15
        SIZE_GPGSA = 18
        SIZE_GPGSV = 20
        SIZE_GPVTG = 10
        
        @classmethod
        def is_valid(cls, type: str) -> bool:
            if type in cls.AVAILABLES.value:
                return True
            else:
                return False
            
    class Direction(Enum):
        NORTH = "N"
        SOUTH = "S"
        EAST = "E"
        WEST = "W"
        AVAILABLES = (NORTH, SOUTH, EAST, WEST)
        
        @classmethod
        def is_valid(cls, direction: str) -> bool:
            if direction in cls.AVAILABLES.value:
                return True
            else:
                return False
            
        @classmethod
        def is_positive(cls, direction: str) -> bool:
            if direction in (cls.NORTH.value, cls.EAST.value):
                return True
            else:
                return False
            
        @classmethod
        def is_negative(cls, direction: str) -> bool:
            if direction in (cls.SOUTH.value, cls.WEST.value):
                return True
            else:
                return False
    
    @classmethod
    def parse(cls, raw: bytes) -> Dict[str, Logable]:
        resolved = cls._resolve(raw)
        if not len(resolved):
            return {}
        
        type = resolved[0]
        if type == cls.Type.GPRMC.value:
            return cls._parse_GPRMC(resolved[1:])
        elif type == cls.Type.GPGGA.value:
            return cls._parse_GPGGA(resolved[1:])
        elif type == cls.Type.GPGSA.value:
            return cls._parse_GPGSA(resolved[1:])
        elif type == cls.Type.GPGSV.value:
            return cls._parse_GPGSV(resolved[1:])
        elif type == cls.Type.GPVTG.value:
            return cls._parse_GPVTG(resolved[1:])
        else:
            return {}
        
    @classmethod
    def convert2radian(cls, degree: float) -> float:
        return radians(degree)
    
    @classmethod
    def convert2coordinate(cls, degree: float, direction: str, radian: bool = True) -> float:
        if cls.Direction.is_valid(direction):
            if cls.Direction.is_negative(direction):
                degree = - degree
        else:
            raise ValueError(
                "'direction' must be 'N', 'S', 'E' or 'W'."
            )
            
        if radian:
            return radians(degree)
        else:
            return degree

    @classmethod
    def _resolve(cls, raw: bytes) -> Tuple[str]:
        if not cls.Sentense.is_valid(raw):
            return ()
        try:
            raw = raw[1:].decode()
            result = raw.split(cls.Sentense.SEPARATOR.value)
            last = result.pop()
            result.extend(last.split(cls.Sentense.SEPARATOR_LAST.value))
            return tuple(result)
        except:
            return ()
    
    @classmethod
    def _parse_GPRMC(cls, contents: Tuple[str]) -> Dict[str, Optional[Logable]]:
        result = {}
        if len(contents) != cls.Type.SIZE_GPRMC.value:
            return result

        latitude = cls._parse_latitude(contents[2])
        longitude = cls._parse_longitude(contents[4])

        result[GPS_TIME_UTC] = cls._parse_time_utc(contents[0])
        result[GPS_STATUS] = contents[1]

        result[GPS_LATITUDE] = latitude[0] + latitude[1] / 60
        result[GPS_LATITUDE_NS] = cls._parse_NS(contents[3])
        result[GPS_LONGITUDE] = longitude[0] + longitude[1] / 60
        result[GPS_LONGITUDE_EW] = cls._parse_EW(contents[5])

        result[GPS_BODY_VELOCITY_KNOT] = cls._parse_velocity(contents[6])
        result[GPS_BODY_TRUE_ANGLE_VELOCITY] = cls._parse_true_angle_velocity(contents[7])
        result[GPS_DATE_UTC] = cls._parse_date_utc(contents[8])
        result[GPS_DIFF_ANGLE_TWONORTH] = cls._parse_angle_twonorth(contents[9])
        result[GPS_ANGLE_TWONORTH_EW] = cls._parse_EW(contents[10])
        result[GPS_MODE] = contents[11]
        result[GPS_CHECK_SUM] = cls._parse_check_sum(contents[12])

        return result

    @classmethod
    def _parse_GPGGA(cls, contents: Tuple[str]) -> Dict[str, Optional[Logable]]:
        result = {}
        if len(contents) != cls.Type.SIZE_GPGGA.value:
            return result

        latitude = cls._parse_latitude(contents[1])
        longitude = cls._parse_longitude(contents[3])

        result[GPS_TIME_UTC] = cls._parse_time_utc(contents[0])

        result[GPS_LATITUDE] = latitude[0] + latitude[1] / 60
        result[GPS_LATITUDE_NS] = cls._parse_NS(contents[2])
        result[GPS_LONGITUDE] = longitude[0] + longitude[1] / 60
        result[GPS_LONGITUDE_EW] = cls._parse_EW(contents[4])

        result[GPS_QUALITY_POSITION] = cls._parse_quality_position(contents[5])
        result[GPS_HOWMANY_SATELLITES_USED] = cls._parse_int(contents[6])
        result[GPS_RATE_DECLINE_QUALITY_HORIZONTAL] = cls._parse_rate_decline(contents[7])
        result[GPS_ALTITUDE_SEALEVEL] = cls._parse_altitude(contents[8])
        result[GPS_ALTITUDE_SEALEVEL_UNIT] = contents[9]
        result[GPS_ALTITUDE_GEOID] = cls._parse_altitude(contents[10])
        result[GPS_ALTITUDE_GEOID_UNIT] = contents[11]
        result[GPS_TIME_FROM_LATEST_DGPS] = contents[12]
        result[GPS_ID_DIFF_POINT] = contents[13]
        result[GPS_CHECK_SUM] = cls._parse_check_sum(contents[14])

        return result

    @classmethod
    def _parse_GPGSA(cls, contents: Tuple[str]) -> Dict[str, Optional[Logable]]:
        result = {}
        if len(contents) != cls.Type.GPGSA.value:
            return result

        result[GPS_MODE] = contents[0]
        result[GPS_TYPE_DETECT] = cls._parse_type_detect(contents[1])
        result[GPS_NUMBERS_SATELLITE] = cls._parse_number_satellite(contents[2:14])
        result[GPS_RATE_DECLINE_QUALITY_POSITION] = cls._parse_rate_decline(contents[14])
        result[GPS_RATE_DECLINE_QUALITY_HORIZONTAL] = cls._parse_rate_decline(contents[15])
        result[GPS_RATE_DECLINE_QUALITY_VERTICAL] = cls._parse_rate_decline(contents[16])
        result[GPS_CHECK_SUM] = cls._parse_check_sum(contents[17])

        return result

    @classmethod
    def _parse_GPGSV(cls, contents: Tuple[str]) -> Dict[str, Optional[Logable]]:
        result = {}
        if len(contents) != cls.Type.SIZE_GPGSV.value:
            return result

        result[GPS_HOWMANY_SENTENCES_GSV] = cls._parse_num_sentence_gsv(contents[0])
        result[GPS_NUMBER_SENTENCE_GSV] = cls._parse_num_sentence(contents[1])
        result[GPS_HOWMANY_SATELLITES_IN_VIEW] = cls._parse_num_satellites_in_view(contents[2])
        result[GPS_SATELLITE_INFO] = cls._parse_info(contents[3:19])
        result[GPS_CHECK_SUM]= cls._parse_check_sum(contents[19])
        return result

    @classmethod
    def _parse_GPVTG(cls, contents: Tuple[str]) -> Dict[str, Optional[Logable]]:
        result = {}
        if len(contents) != cls.Type.SIZE_GPVTG.value:
            return result

        result[GPS_BODY_TRUE_ANGLE_VELOCITY] = cls._parse_true_angle_velocity(contents[0])
        result[GPS_BODY_MAGNETIC_ANGLE_VELOCITY] = cls._parse_magnetic_angle_velocity(contents[2])
        result[GPS_BODY_VELOCITY_KNOT] = cls._parse_velocity(contents[4])
        result[GPS_BODY_VELOCITY_KM] = cls._parse_velocity(contents[6])
        result[GPS_MODE] = contents[8]
        result[GPS_CHECK_SUM] = cls._parse_check_sum(contents[9])
        return result

    @classmethod
    def _parse_float(cls, content: str) -> Optional[float]:
        try:
            return float(content)
        except:
            return None

    @classmethod
    def _parse_int(cls, content: str) -> Optional[int]:
        try:
            return int(content)
        except:
            return None

    @classmethod
    def _parse_time_utc(cls, content: str) -> Optional[str]:
        if len(content) != 10:
            return None
        return ":".join((content[:2], content[2:4], content[4:]))
    
    @classmethod
    def convert_time(cls, time: str) -> Tuple[Union[int, float]]:
        time_list = time.split(":")
        return (int(time_list[0]), int(time_list[1]), float(time_list[2]))

    @classmethod
    def _parse_date_utc(cls, content: str) -> Optional[str]:
        if len(content) != 6:
            return None
        return ".".join((content[:2], content[2:4], content[4:]))
    
    @classmethod
    def convert_date(cls, date: str) -> Tuple[int]:
        return tuple(map(int, date.split(".")))

    @classmethod
    def _parse_latitude(cls, content: str) -> Optional[Tuple[float]]:
        if len(content) != 9:
            return None
        try:
            return (float(content[:-7]), float(content[-7:]))
        except:
            return None

    @classmethod
    def _parse_longitude(cls, content: str) -> Optional[Tuple[Union[int, float]]]:
        return cls._parse_latitude(content)

    @classmethod
    def _parse_velocity(cls, content: str) -> Optional[float]:
        return cls._parse_float(content)

    @classmethod
    def _parse_true_angle_velocity(cls, content: str) -> Optional[float]:
        return cls._parse_float(content)

    @classmethod
    def _parse_magnetic_angle_velocity(cls, content: str) -> Optional[float]:
        return cls._parse_float(content)

    @classmethod
    def _parse_angle_twonorth(cls, content: str) -> Optional[float]:
        return cls._parse_float(content)

    @classmethod
    def _parse_quality_position(cls, content: str) -> Optional[int]:
        return cls._parse_int(content)
    
    @classmethod
    def _parse_rate_decline(cls, content: str) -> Optional[float]:
        return cls._parse_float(content)

    @classmethod
    def _parse_altitude(cls, content: str) -> Optional[float]:
        return cls._parse_float(content)

    @classmethod
    def _parse_check_sum(cls, content: str) -> Optional[str]:
        return content if len(content) == 2 else None

    @classmethod
    def _parse_type_detect(cls, content: str) -> Optional[int]:
        return cls._parse_int(content)

    @classmethod
    def _parse_number_satellite(cls, content: Tuple[str]) -> Optional[str]:
        try:
            result = []
            for num in content:
                if not len(num):
                    continue
                else:
                    result.append(int(num))
            return ":".join(result)
        except:
            return None

    @classmethod
    def _parse_num_sentence_gsv(cls, content: str) -> Optional[int]:
        return cls._parse_int(content)

    @classmethod
    def _parse_num_sentence(cls, content: str) -> Optional[int]:
        return cls._parse_int(content)

    @classmethod
    def _parse_num_satellites_in_view(cls, content: str) -> Optional[int]:
        return cls._parse_int(content)

    @classmethod
    def _parse_angle_satellite(cls, content: str) -> Optional[int]:
        return cls._parse_int(content)

    @classmethod
    def _parse_ratio_carrier_noise(cls, content: str) -> Optional[int]:
        return cls._parse_int(content)

    @classmethod
    def _parse_NS(cls, content: str) -> Optional[str]:
        return content if content in (cls.Direction.NORTH.value, cls.Direction.SOUTH.value) else None

    @classmethod
    def _parse_EW(cls, content: str) -> Optional[str]:
        return content if content in (cls.Direction.EAST.value, cls.Direction.WEST.value) else None
    
    @classmethod
    def _parse_info(cls, content: str) -> Optional[str]:
        if len(content) != 16:
            return None
        
        info = []
        for i in range(4):
            satellite = []
            satellite.append(content[4 * i])
            satellite.append(content[1 + 4 * i])
            satellite.append(content[2 + 4 * i])
            satellite.append(content[3 + 4 * i])
            info.append(":".join(satellite))
        return "/".join(info)
    
    @classmethod
    def convert_info(cls, info: str) -> Tuple[Dict[str, int]]:
        try:
            result = []
            for satellite in info.split("/"):
                content = satellite.split(":")
                data = {}
                data[GPS_NUMBER_SATELLITE] = cls._parse_int(content[0])
                data[GPS_ANGLE_ELEVATION_SATTELITE] = cls._parse_int(content[1])
                data[GPS_ANGLE_AZIMUTH_SATTELITE] = cls._parse_int(content[2])
                data[GPS_RATIO_CARRIER_NOISE] = cls._parse_int(content[3])
                result.append(data)
            return tuple(result)
        except:
            return ()
