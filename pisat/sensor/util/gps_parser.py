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

from typing import *
import math

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
    GPS_LATITUDE_DEGREE,
    GPS_LATITUDE_MINUITE,
    GPS_LATITUDE_NS,
    GPS_LATITUDE_RADIAN,
    GPS_LONGITUDE,
    GPS_LONGITUDE_DEGREE,
    GPS_LONGITUDE_EW,
    GPS_LONGITUDE_MINUITE,
    GPS_LONGITUDE_RADIAN,
    GPS_MODE,
    GPS_NUM_SATELLITES,
    GPS_NUM_SATELLITES_IN_VIEW,
    GPS_NUM_SENTENCES_GSV,
    GPS_NUM_THIS_SENTENCE_GSV,
    GPS_NUMBER_SATELLITE,
    GPS_NUMBER_THIS_SATELLITE,
    GPS_QUALITY_POSITION,
    GPS_RATE_DECLINE_QUALITY_HORIZONTAL,
    GPS_RATE_DECLINE_QUALITY_POSITION,
    GPS_RATE_DECLINE_QUALITY_VERTICAL,
    GPS_RATIO_CARRIER_NOISE,
    GPS_STATUS,
    GPS_TIME_FROM_LATEST_DGPS,
    GPS_TIME_UTC,
    GPS_TYPE_DETECT
)


class GPSParserBase:

    SENTENSE_HEAD = "$"
    SENTENSE_TERMINOR = "\r\n"

    TYPE_GPRMC = "GPRMC"
    TYPE_GPGGA = "GPRMC"
    TYPE_GPGSA = "GPRMC"
    TYPE_GPGSV = "GPRMC"
    TYPE_GPVTG = "GPRMC"
    TYPES = (TYPE_GPRMC, TYPE_GPGGA,
             TYPE_GPGSA, TYPE_GPGSV,
             TYPE_GPVTG             )
    LEN_TYPE = 5

    def __init__(self):
        super().__init__()

    def resultolve(self,
                sentence: Union[str, bytes, bytearray],
                include_head=True,
                include_terminal=True,
                len_terminal=2) -> Tuple[str, list]:

        try:
            if isinstance(sentence, (bytes, bytearray)):
                sentence = sentence.decode()

            if include_head and sentence[0] != GPSParser.SENTENSE_HEAD:
                return []

            sentence = sentence[1:] if include_head else sentence
            sentence = sentence[:-
                                len_terminal] if include_terminal else sentence

            if sentence[:GPSParser.LEN_TYPE] not in GPSParser.TYPES:
                return []

            sentence = sentence.split(",")
            return sentence[0], sentence[1:]

        except:
            return []

    # to be override
    def update(self, sentence: bytes) -> None:
        pass

    def _parse_float(self, content: str) -> Optional[float]:
        try:
            return float(content)
        except:
            return None

    def _parse_int(self, content: str) -> Optional[int]:
        try:
            int(content)
        except:
            return None

    def _parse_time_utc(self, content: str) -> tuple:
        if len(content) != 10:
            return None

        # hour, min, sec, milisec
        try:
            return (int(content[:2]),
                    int(content[2:4]),
                    int(content[4:6]),
                    int(content[7:]))
        except:
            return None

    def _parse_date_utc(self, content: str) -> tuple:
        if len(content) != 6:
            return None

        try:
            # day, month, year
            return (int(content[:2]), int(content[2:4], int(content[4:])))
        except:
            return None

    def _parse_latitude(self, content: str) -> Optional[tuple]:
        if len(content) != 9:
            return None

        try:
            return (int(content[:-7]),
                    float(content[-7:]))
        except:
            return None

    def _parse_longitude(self, content: str) -> tuple:
        return self._parse_latitude(content)

    def _parse_velocity(self, content: str) -> float:
        return self._parse_float(content)

    def _parse_true_angle_velocity(self, content: str) -> float:
        return self._parse_float(content)

    def _parse_magnetic_angle_velocity(self, content: str) -> float:
        return self._parse_float(content)

    def _parse_angle_twonorth(self, content: str) -> float:
        return self._parse_float(content)

    def _parse_quality_position(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_num_satellites(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_rate_decline(self, content: str) -> float:
        return self._parse_float(content)

    def _parse_altitude(self, content: str) -> float:
        return self._parse_float(content)

    def _parse_check_sum(self, content: str) -> Optional[str]:
        try:
            return content[1:]
        except:
            return None

    def _parse_type_detect(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_number_satellite(self, content: List[str]) -> Optional[tuple]:
        try:
            result = []
            for cont in content:
                if cont is None:
                    continue
                else:
                    result.append(int(cont))

            return tuple(result)

        except:
            return None

    def _parse_num_sentence_gsv(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_num_sentence(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_num_satellites_in_view(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_number_satellite(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_angle_satellite(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_ratio_carrier_noise(self, content: str) -> int:
        return self._parse_int(content)

    def _parse_NS(self, content: str) -> str:
        return content if content in ("N", "S") else None

    def _parse_EW(self, content: str) -> str:
        return content if content in ("E", "W") else None


class GPSParser(GPSParserBase):

    def __init__(self,
                 include_head=True,
                 include_terminal=True,
                 len_terminal=2):
        super().__init__()

        self._data = {
            GPS_TIME_UTC: None,
            GPS_STATUS: None,
            GPS_LONGITUDE: None,
            GPS_LONGITUDE_RADIAN: None,
            GPS_LONGITUDE_DEGREE: None,
            GPS_LONGITUDE_MINUITE: None,
            GPS_LONGITUDE_EW: None,
            GPS_LATITUDE: None,
            GPS_LATITUDE_RADIAN: None,
            GPS_LATITUDE_DEGREE: None,
            GPS_LATITUDE_MINUITE: None,
            GPS_LATITUDE_NS: None,
            GPS_BODY_VELOCITY_KNOT: None,
            GPS_BODY_VELOCITY_KM: None,
            GPS_BODY_TRUE_ANGLE_VELOCITY: None,
            GPS_DIFF_ANGLE_TWONORTH: None,
            GPS_ANGLE_TWONORTH_EW: None,
            GPS_MODE: None,
            GPS_CHECK_SUM: None,
            GPS_ALTITUDE_SEALEVEL: None,
            GPS_ALTITUDE_SEALEVEL_UNIT: None,
            GPS_ALTITUDE_GEOID: None,
            GPS_ALTITUDE_GEOID_UNIT: None,
            GPS_TIME_FROM_LATEST_DGPS: None,
            GPS_ID_DIFF_POINT: None,
            GPS_TYPE_DETECT: None,
            GPS_NUM_SATELLITES: None,
            GPS_NUMBER_SATELLITE: None,
            GPS_QUALITY_POSITION: None,
            GPS_RATE_DECLINE_QUALITY_HORIZONTAL: None,
            GPS_RATE_DECLINE_QUALITY_VERTICAL: None,
            GPS_NUM_SENTENCES_GSV: None,
            GPS_NUM_THIS_SENTENCE_GSV: None,
            GPS_NUM_SATELLITES_IN_VIEW: None,
            GPS_NUMBER_THIS_SATELLITE: None,
            GPS_ANGLE_ELEVATION_SATTELITE: None,
            GPS_ANGLE_AZIMUTH_SATTELITE: None,
            GPS_RATIO_CARRIER_NOISE: None
        }

        self._include_head = include_head
        self._include_terminal = include_terminal
        self._len_terminal = len_terminal

    @property
    def data(self):
        return self._data

    def get_vals(self, *dnames) -> list:

        if len(dnames) == 0:
            return self._data.values

        result = []
        for dname in dnames:
            try:
                result.append(self._data[dname])
            except:
                pass

        return result

    def get_data(self, *dnames) -> dict:

        if len(dnames) == 0:
            return self._data

        result = {}
        for dname in dnames:
            try:
                result[dname] = self._data[dname]
            except:
                pass

        return result

    def update(self, sentence: bytes) -> None:
        resolved = self.resultolve(sentence,
                                include_head=self._include_head,
                                include_terminal=self._include_terminal,
                                len_terminal=self._len_terminal)

        if len(resolved) == 0:
            return

        dtype, contents = resolved

        if dtype not in GPSParser.TYPES:
            return

        if dtype == GPSParser.TYPE_GPRMC:
            result = self._parse_GPRMC(contents)
        elif dtype == GPSParser.TYPE_GPGGA:
            result = self._parse_GPGGA(contents)
        elif dtype == GPSParser.TYPE_GPGSA:
            result = self._parse_GPGSA(contents)
        elif dtype == GPSParser.TYPE_GPGSV:
            result = self._parse_GPGSV(contents)
        else:
            result = self._parse_GPVTG(contents)

        for key, val in result.items():
            if val is not None:
                self._data[key] = val

    def _parse_GPRMC(self, contents: List[str]) -> Optional[dict]:

        # Returns None if data is broken
        if len(contents) != 13:
            return None

        latitude = self._parse_latitude(contents[2])
        longitude = self._parse_longitude(contents[4])

        result = {}

        result[GPS_TIME_UTC]                   = self._parse_time_utc(contents[0])
        result[GPS_STATUS]                     = contents[1]

        result[GPS_LATITUDE]                   = latitude[0] + latitude[1] / 60
        result[GPS_LATITUDE_RADIAN]            = result[GPS_LATITUDE] / 180 * math.pi
        result[GPS_LATITUDE_DEGREE]            = latitude[0]
        result[GPS_LATITUDE_MINUITE]           = latitude[1]
        result[GPS_LATITUDE_NS]                = self._parse_NS(contents[3])
        result[GPS_LONGITUDE]                  = longitude[0] + longitude[1] / 60
        result[GPS_LONGITUDE_RADIAN]           = result[GPS_LONGITUDE] / 180 * math.pi
        result[GPS_LONGITUDE_DEGREE]           = longitude[0]
        result[GPS_LONGITUDE_MINUITE]          = longitude[1]
        result[GPS_LONGITUDE_EW]               = self._parse_EW(contents[5])

        result[GPS_BODY_VELOCITY_KNOT]         = self._parse_velocity(contents[6])
        result[GPS_BODY_TRUE_ANGLE_VELOCITY]   = self._parse_true_angle_velocity(contents[7])
        result[GPS_DATE_UTC]                   = self._parse_date_utc(contents[8])
        result[GPS_DIFF_ANGLE_TWONORTH]        = self._parse_angle_twonorth(contents[9])
        result[GPS_ANGLE_TWONORTH_EW]          = self._parse_EW(contents[10])
        result[GPS_MODE]                       = contents[11]
        result[GPS_CHECK_SUM]                  = self._parse_check_sum(contents[12])

        return result

    def _parse_GPGGA(self, contents: List[str]) -> Optional[dict]:

        # Returns None if data is broken
        if len(contents) != 15:
            return None

        latitude = self._parse_latitude(contents[1])
        longitude = self._parse_longitude(contents[3])

        result = {}

        result[GPS_TIME_UTC]                            = self._parse_time_utc(contents[0])

        result[GPS_LATITUDE]                            = latitude[0] + latitude[1] / 60
        result[GPS_LATITUDE_RADIAN]                     = result[GPS_LATITUDE] / 180 * math.pi
        result[GPS_LATITUDE_DEGREE]                     = latitude[0]
        result[GPS_LATITUDE_MINUITE]                    = latitude[1]
        result[GPS_LATITUDE_NS]                         = self._parse_NS(contents[2])
        result[GPS_LONGITUDE]                           = longitude[0] + longitude[1] / 60
        result[GPS_LONGITUDE_RADIAN]                    = result[GPS_LONGITUDE] / 180 * math.pi
        result[GPS_LONGITUDE_DEGREE]                    = longitude[0]
        result[GPS_LONGITUDE_MINUITE]                   = longitude[1]
        result[GPS_LONGITUDE_EW]                        = self._parse_EW(contents[4])

        result[GPS_QUALITY_POSITION]                    = self._parse_quality_position(contents[5])
        result[GPS_NUM_SATELLITES]                      = self._parse_num_satellites(contents[6])
        result[GPS_RATE_DECLINE_QUALITY_HORIZONTAL]     = self._parse_rate_decline(contents[7])
        result[GPS_ALTITUDE_SEALEVEL]                   = self._parse_altitude(contents[8])
        result[GPS_ALTITUDE_SEALEVEL_UNIT]              = contents[9]
        result[GPS_ALTITUDE_GEOID]                      = self._parse_altitude(contents[10])
        result[GPS_ALTITUDE_GEOID_UNIT]                 = contents[11]
        result[GPS_TIME_FROM_LATEST_DGPS]               = contents[12]
        result[GPS_ID_DIFF_POINT]                       = contents[13]
        result[GPS_CHECK_SUM]                           = self._parse_check_sum(contents[14])

        return result

    def _parse_GPGSA(self, contents: List[str]) -> Optional[dict]:

        # Returns None if data is broken
        if len(contents) != 7:
            return None

        result = {}

        result[GPS_MODE]                                = contents[0]
        result[GPS_TYPE_DETECT]                         = self._parse_type_detect(contents[1])
        result[GPS_NUMBER_SATELLITE]                    = self._parse_number_satellite(contents[2])
        result[GPS_RATE_DECLINE_QUALITY_POSITION]       = self._parse_rate_decline(contents[3])
        result[GPS_RATE_DECLINE_QUALITY_HORIZONTAL]     = self._parse_rate_decline(contents[4])
        result[GPS_RATE_DECLINE_QUALITY_VERTICAL]       = self._parse_rate_decline(contents[5])
        result[GPS_CHECK_SUM]                           = self._parse_check_sum(contents[6])

        return result

    def _parse_GPGSV(self, contents: List[str]) -> Optional[dict]:

        # Returns None if data is broken
        if len(contents) != 20:
            return None

        result = {}

        result[GPS_NUM_SENTENCES_GSV]                   = self._parse_num_sentence_gsv(contents[0])
        result[GPS_NUM_THIS_SENTENCE_GSV]               = self._parse_num_sentence(contents[1])
        result[GPS_NUM_SATELLITES_IN_VIEW]              = self._parse_num_satellites_in_view(contents[2])

        result[GPS_NUMBER_THIS_SATELLITE]               = []
        result[GPS_ANGLE_ELEVATION_SATTELITE]           = []
        result[GPS_ANGLE_AZIMUTH_SATTELITE]             = []
        result[GPS_RATIO_CARRIER_NOISE]                 = []

        for i in range(4):
            result[GPS_NUMBER_THIS_SATELLITE].append(
                self._parse_int(contents[3 + 4 * i]))
            result[GPS_ANGLE_ELEVATION_SATTELITE].append(
                self._parse_angle_satellite(contents[4 + 4 * i]))
            result[GPS_ANGLE_AZIMUTH_SATTELITE].append(
                self._parse_angle_satellite(contents[5 + 4 * i]))
            result[GPS_RATIO_CARRIER_NOISE].append(
                self._parse_ratio_carrier_noise(contents[6 + 4 * i]))

        result[GPS_CHECK_SUM]                           = self._parse_check_sum(contents[19])

        return result

    def _parse_GPVTG(self, contents: List[str]) -> Optional[dict]:

        # Returns None if data is broken
        if len(contents) != 10:
            return None

        result = {}

        result[GPS_BODY_TRUE_ANGLE_VELOCITY]            = self._parse_true_angle_velocity(contents[0])
        result[GPS_BODY_MAGNETIC_ANGLE_VELOCITY]        = self._parse_magnetic_angle_velocity(contents[2])
        result[GPS_BODY_VELOCITY_KNOT]                  = self._parse_velocity(contents[4])
        result[GPS_BODY_VELOCITY_KM]                    = self._parse_velocity(contents[6])
        result[GPS_MODE]                                = contents[8]
        result[GPS_CHECK_SUM]                           = self._parse_check_sum(contents[9])
