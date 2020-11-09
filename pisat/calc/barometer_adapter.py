#! python3

"""

pisat.adapter.barometer_adapter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An adapter class for calculating from barometer data.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
https://keisan.casio.jp/exec/system/1257609530
"""

from typing import Dict, Tuple, Union
import math

from pisat.config.type import Logable
from pisat.config.dname import PRESSURE, TEMPERATURE, ALTITUDE_SEALEVEL
from pisat.adapter.adapter_base import AdapterBase


class BarometerAdapter(AdapterBase):

    DATA_NAMES: Tuple[str]                  = (ALTITUDE_SEALEVEL,)
    DATA_REQUIRES: Dict[str, Tuple[str]]    = {ALTITUDE_SEALEVEL: (PRESSURE, TEMPERATURE)}
    
    PRESSURE_ATMOSPHERE             = 1013.25           # [hPa]
    TEMPELATURE_ABSOLUTE_CELSIUS    = 273.15            # [K]

    def __init__(self):
        super().__init__()

    def calc(self, data: Dict[str, Logable], *dnames) -> Dict[str, Logable]:
        return {self.DATA_NAMES[0]: self.calc_altitude(data[PRESSURE], data[TEMPERATURE])}
    
    @classmethod
    def calc_altitude(cls,
                      press: Union[int, float],
                      temp: Union[int, float]) -> float:
        dep_p = math.pow(cls.PRESSURE_ATMOSPHERE / press, 1. / 5.257) - 1.
        dep_T = temp + cls.TEMPELATURE_ABSOLUTE_CELSIUS
        return dep_p * dep_T / 0.0065
