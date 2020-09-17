#! python3

"""

pisat.sensor.sensor.gyfsdmaxb
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sensor class of GYFSDMAXB GPS module compatible with the pisat system.
This module works completely, regardless of whether using the pisat system or not.

NOTE
    This sensor can be read 10 times per second at most. Therefore it is strongly
    recommended that you should set the interval time of sampling as long as 
    outputting data successfully is possible.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
GYFSDMAXB datasheet
    https://www.yuden.co.jp/wireless_module/document/datareport2/jp/TY_GPS_GYSFDMAXB_DataReport_V1.0J_20161201.pdf
    
TODO    debug, docstring
"""

from typing import *

from pisat.config.dname import (
    GPS_ALTITUDE_GEOID,
    GPS_ALTITUDE_SEALEVEL,
    GPS_BODY_MAGNETIC_ANGLE_VELOCITY,
    GPS_BODY_TRUE_ANGLE_VELOCITY,
    GPS_BODY_VELOCITY_KM,
    GPS_DIFF_ANGLE_TWONORTH,
    GPS_LATITUDE,
    GPS_LATITUDE_RADIAN,
    GPS_LONGITUDE,
    GPS_LONGITUDE_RADIAN,
)
from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.sensor.sensor.sensor_base import SensorBase
from pisat.sensor.sensor.sensor_base import HandlerMismatchError
from pisat.sensor.util.gps_parser import GPSParser


class Gyfsdmaxb(SensorBase):

    #   SensorAdditional ATTRIBUTES
    NAME = "GYFSDMAXB"
    DATA_NAMES = (GPS_LONGITUDE,                           # signed
                  GPS_LONGITUDE_RADIAN,                    # signed
                  GPS_LATITUDE,                            # signed
                  GPS_LATITUDE_RADIAN,                     # signed
                  GPS_DIFF_ANGLE_TWONORTH,                 # signed
                  GPS_BODY_VELOCITY_KM,
                  GPS_BODY_TRUE_ANGLE_VELOCITY,
                  GPS_BODY_MAGNETIC_ANGLE_VELOCITY,
                  GPS_ALTITUDE_SEALEVEL,
                  GPS_ALTITUDE_GEOID)

    def __init__(self, handler: SerialHandlerBase, rate: int = 5, init_wait=2000, suff_wait=500):

        self._handler: SerialHandlerBase = handler
        self._parser = GPSParser()
        self._rate = rate
        # minimum limit of bytes of in_waiting
        self._suff_wait = suff_wait

        if isinstance(self._handler, SerialHandlerBase):
            HandlerMismatchError(
                "Given handler object is not supported in the class.")

        # initializing
        while self._handler.in_waiting < init_wait:
            pass

    @property
    def dnames(self):
        return Gyfsdmaxb.NAMES

    @property
    def rate(self):
        return self._rate

    def set_rate(self, rate: int) -> None:
        self._rate = rate

    def _update(self) -> None:

        # TODO
        rate = self._rate if self._handler.in_waiting >= self._suff_wait else 1

        for sentence in [self._handler.readline() for _ in range(rate)]:
            self._parser.update(sentence)

    @classmethod
    def _configure(cls, data: list) -> list:

        if data[2] is not None:
            data[0] = - data[0] if data[2] == "W" else data[0]
            data[1] = - data[1] if data[2] == "W" else data[1]

        if data[5] is not None:
            data[3] = - data[3] if data[5] == "S" else data[3]
            data[4] = - data[4] if data[5] == "S" else data[4]

        if data[7] is not None:
            data[6] = - data[6] if data[7] == "W" else data[6]

        return [d for i, d in enumerate(data) if i not in (2, 5, 7)]

    def readf(self, *dnames) -> List[float]:

        self._update()
        data = Gyfsdmaxb._configure(self._parser.get_vals(*Gyfsdmaxb.REQUIRED))

        if len(dnames) == 0:
            return data

        else:
            res = []
            for dname in dnames:
                if dname == GPS_LONGITUDE:
                    res.append(data[0])
                elif dname == GPS_LONGITUDE_RADIAN:
                    res.append(data[1])
                elif dname == GPS_LATITUDE:
                    res.append(data[2])
                elif dname == GPS_LATITUDE_RADIAN:
                    res.append(data[3])
                elif dname == GPS_DIFF_ANGLE_TWONORTH:
                    res.append(data[4])
                elif dname == GPS_BODY_VELOCITY_KM:
                    res.append(data[5])
                elif dname == GPS_BODY_TRUE_ANGLE_VELOCITY:
                    res.append(data[6])
                elif dname == GPS_BODY_MAGNETIC_ANGLE_VELOCITY:
                    res.append(data[7])
                elif dname == GPS_ALTITUDE_SEALEVEL:
                    res.append(data[8])
                elif dname == GPS_ALTITUDE_GEOID:
                    res.append(data[9])

            return res

    def read(self, *dnames) -> Dict[str, float]:

        if len(dnames) == 0:
            return {dname: val for dname, val in zip(self.dnames, self.readf())}

        else:
            data = self.readf(*dnames)
            if len(data) == len(dnames):
                raise ValueError("Specified data names are incorrect.")
            else:
                return {dname: val for dname, val in zip(dnames, data)}
