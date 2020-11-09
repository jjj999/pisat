#! python3

"""

FILE NAME
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION


[author]
AUTHOR NAME, ORGANIZATION NAME

[info]
OTHER INFORMATION
    
"""

from typing import List, Optional, Tuple, Dict, Union
import math

from pisat.config.type import Logable
from pisat.config.dname import (
    GPS_LATITUDE_NS, GPS_LONGITUDE, GPS_LATITUDE,
    DISTANCE, GPS_LONGITUDE_EW, RELATIVE_COORDINATE_X, 
    RELATIVE_COORDINATE_Y, ANGLE_RADIAN_FROM_NORTH_POLE
)
from pisat.adapter.adapter_base import AdapterBase
from pisat.util.gps_parser import GPSParser


class GpsAdapter(AdapterBase):

    DATA_NAMES: Tuple[str] = (
        DISTANCE, RELATIVE_COORDINATE_X, RELATIVE_COORDINATE_Y, ANGLE_RADIAN_FROM_NORTH_POLE
    )
    DATA_REQUIRES: Dict[str, Tuple[str]] = {
        DISTANCE:                       (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
        RELATIVE_COORDINATE_X:          (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
        RELATIVE_COORDINATE_Y:          (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
        ANGLE_RADIAN_FROM_NORTH_POLE:   (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
    }

    MAJOR_RADIUS_WGS84: float = 6378137.000
    MINOR_RADIUS_WGS84: float = 6356752.314245
    ECCENTRICITY: float = math.sqrt(1 - (MINOR_RADIUS_WGS84 / MAJOR_RADIUS_WGS84) ** 2)

    def __init__(self,
                 goal: Union[Tuple[float], List[float]],
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.set_goal(goal)

    @property
    def goal(self):
        return self._goal

    def set_goal(self, goal: Union[Tuple[float], List[float]]):
        if not isinstance(goal, (tuple, list)):
            raise TypeError(
                "'goal' must be tuple or list, but {} was given."
                .format(goal.__class__.__name__)
            )
        self._goal = goal

    def calc(self, data: Dict[str, Logable], *dnames) -> Dict[str, Logable]:
        longitude = data.get(GPS_LONGITUDE)
        longitude_ew = data.get(GPS_LONGITUDE_EW)
        latitude = data.get(GPS_LATITUDE)
        latitude_ns = data.get(GPS_LATITUDE_NS)
        target = (GPSParser.convert2coordinate(longitude, longitude_ew),
                  GPSParser.convert2coordinate(latitude, latitude_ns))

        if len(dnames) == 0:
            distance = self.calc_distance(target, self._goal)
            coordinate = self.calc_relative_coordinate(target, self._goal)
            angle = self.calc_angle_from_north(coordinate)
            return {DISTANCE: distance,
                    RELATIVE_COORDINATE_X: coordinate[0],
                    RELATIVE_COORDINATE_Y: coordinate[1],
                    ANGLE_RADIAN_FROM_NORTH_POLE: angle}
        else:
            result = {}
            coordinate = []
            for dname in dnames:
                if dname == DISTANCE:
                    result[DISTANCE] = self.calc_distance(target, self._goal)
                elif dname == RELATIVE_COORDINATE_X:
                    if len(coordinate) == 0:
                        coordinate = self.calc_relative_coordinate(target, self._goal)
                    result[RELATIVE_COORDINATE_X] = coordinate[0]
                elif dname == RELATIVE_COORDINATE_Y:
                    if len(coordinate) == 0:
                        coordinate = self.calc_relative_coordinate(target, self._goal)
                    result[RELATIVE_COORDINATE_Y] = coordinate[1]
                elif dname == ANGLE_RADIAN_FROM_NORTH_POLE:
                    if len(coordinate) == 0:
                        result[ANGLE_RADIAN_FROM_NORTH_POLE] = self.calc_relative_angle(target, self._goal)
                    else:
                        result[ANGLE_RADIAN_FROM_NORTH_POLE] = self.calc_angle_from_north(coordinate)
            return result
        
    @classmethod
    def calc_diffs(cls, r1: Tuple[float], r2: Tuple[float]) -> Tuple[float]:
        diff_longi: float = r1[0] - r2[0]
        diff_lati: float = r1[1] - r2[1]

        # Compensation is needed only as for longitude.
        if abs(diff_longi) > math.pi:
            abs_diff_longi = 2 * math.pi - abs(r1[0]) - abs(r2[0])
            if diff_longi > 0:
                diff_longi = - abs_diff_longi
            else:
                diff_longi = abs_diff_longi
                        
        return (diff_longi, diff_lati)

    @classmethod
    def calc_distance(cls, r1: Tuple[float], r2: Tuple[float]) -> float:
        diff_longi, diff_lati = cls.calc_diffs(r1, r2)
        mean_lati = (r1[1] + r2[1]) / 2
        denom_carvature = math.sqrt(1 - (cls.ECCENTRICITY * math.sin(mean_lati)) ** 2)
        meridian_carvature = cls.MAJOR_RADIUS_WGS84 * (1 - cls.ECCENTRICITY ** 2) / denom_carvature ** 3
        prime_carvature = cls.MAJOR_RADIUS_WGS84 / denom_carvature
        return math.sqrt((diff_lati * meridian_carvature) ** 2 + (diff_longi * prime_carvature * math.cos(mean_lati)) ** 2)

    @classmethod
    def calc_relative_quadrant(cls,
                               target: Union[Tuple[float], List[float]],
                               origin: Union[Tuple[float], List[float]]) -> int:

        #   NOTE
        #                   |
        #                   |
        #          2       -2        1
        #                   |
        #   ----- -3 -------0------ -1 --------
        #                   |
        #          3       -4        4
        #                   |
        #                   |
        #
        #              Quadrant Map
        #
        diff_longi, diff_lati = cls.calc_diffs(target, origin)

        # positive area of the longi axis
        if diff_longi > 0:
            if diff_lati > 0:
                quadrant = 1
            elif diff_lati == 0:
                quadrant = -1
            else:
                quadrant = 4

        # on the longi axis
        elif diff_longi == 0:
            if diff_lati > 0:
                quadrant = -2
            elif diff_lati < 0:
                quadrant = -4
            else:
                quadrant = 0

        # negative area of the longi axis
        else:
            if diff_lati > 0:
                quadrant = 2
            elif diff_lati == 0:
                quadrant = -3
            else:
                quadrant = 3

        return quadrant

    @classmethod
    def calc_relative_coordinate(cls,
                                 target: Tuple[float],
                                 origin: Tuple[float]) -> List[float]:

        distance_x: float = cls.calc_distance((origin[0], target[1]), target)
        distance_y: float = cls.calc_distance((target[0], origin[1]), target)
        quadrant: int = cls.calc_relative_quadrant(target, origin)
        coordinate: List[float] = []

        if quadrant in (1, 0, -1, -2):
            coordinate.append(distance_x)
            coordinate.append(distance_y)
        elif quadrant in (2, -3):
            coordinate.append(- distance_x)
            coordinate.append(distance_y)
        elif quadrant == 3:
            coordinate.append(- distance_x)
            coordinate.append(- distance_y)
        elif quadrant in (4, -4):
            coordinate.append(distance_x)
            coordinate.append(- distance_y)

        return coordinate

    @classmethod
    def calc_angle_from_north(cls,
                              coordinate: Union[Tuple[float], List[float]],
                              isradan: bool = True) -> float:
        # positive --> ccw
        # negative --> cw
        radian = - math.atan2(coordinate[0], coordinate[1])
        
        # range --> (-90, 90]
        if math.isclose(radian, - 90., abs_tol=2e-10):
            radian = 90.

        if isradan:
            return radian
        else:
            return radian / math.pi * 180.

    @classmethod
    def calc_relative_angle(cls,
                            target: Tuple[float],
                            origin: Tuple[float],
                            isradian: bool = True) -> float:
        coordinate = cls.calc_relative_coordinate(target, origin)
        return cls.calc_angle_from_north(coordinate, isradan=isradian)
