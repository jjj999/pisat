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

from typing import List, Tuple, Dict, Union
import math

from pisat.config.type import Logable
from pisat.config.dname import (
    GPS_LONGITUDE, GPS_LATITUDE,
    DISTANCE, RELATIVE_COORDINATE_X, RELATIVE_COORDINATE_Y, ANGLE_RADIAN_FROM_NORTH_POLE
)
from pisat.adapter.adapter_base import AdapterBase


class GpsAdapter(AdapterBase):

    ADAPTER_NAME: str = "GpsAdapter"
    DATA_NAMES: Tuple[str] = (
        DISTANCE, RELATIVE_COORDINATE_X, RELATIVE_COORDINATE_Y, ANGLE_RADIAN_FROM_NORTH_POLE
    )
    DATA_REQUIRES: Dict[str, Tuple[str]] = {
        DISTANCE:                       (GPS_LONGITUDE, GPS_LATITUDE),
        RELATIVE_COORDINATE_X:          (GPS_LONGITUDE, GPS_LATITUDE),
        RELATIVE_COORDINATE_Y:          (GPS_LONGITUDE, GPS_LATITUDE),
        ANGLE_RADIAN_FROM_NORTH_POLE:   (GPS_LONGITUDE, GPS_LATITUDE),
    }

    MAJOR_RADIUS_WGS84: float = 6378137.000
    MINOR_RADIUS_WGS84: float = 6356752.314245
    ECCENTRICITY: float = math.sqrt(
        1 - (MINOR_RADIUS_WGS84 / MAJOR_RADIUS_WGS84) ** 2)

    def __init__(self,
                 goal: Union[Tuple[float], List[float]]):

        self._goal: Union[Tuple[float], List[float]] = self.set_goal(goal)

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

        target = (data[GPS_LATITUDE], data[GPS_LONGITUDE])

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
                        coordinate = \
                            self.calc_relative_coordinate(target, self._goal)
                    result[RELATIVE_COORDINATE_X] = coordinate[0]
                elif dname == RELATIVE_COORDINATE_Y:
                    if len(coordinate) == 0:
                        coordinate = \
                            self.calc_relative_coordinate(target, self._goal)
                    result[RELATIVE_COORDINATE_Y] = coordinate[1]
                elif dname == ANGLE_RADIAN_FROM_NORTH_POLE:
                    if len(coordinate) == 0:
                        result[ANGLE_RADIAN_FROM_NORTH_POLE] = \
                            self.calc_relative_angle(target, self._goal)
                    else:
                        result[ANGLE_RADIAN_FROM_NORTH_POLE] = \
                            self.calc_relative_angle(coordinate)
            return result

    @classmethod
    def calc_distance(cls, r1: Tuple[float], r2: Tuple[float]) -> float:
        # r2 -> r1 のベクトル
        diffs = [x1 - x2 for x1, x2 in zip(r1, r2)]
        # 2点の緯度の平均
        mean_lati = (r1[1] + r2[1]) / 2
        denom_carvature = math.sqrt(
            1 - (cls.ECCENTRICITY * math.sin(mean_lati)) ** 2)              # 子午線・卯酉線の分母
        meridian_carvature = cls.MAJOR_RADIUS_WGS84 * \
            (1 - cls.ECCENTRICITY) / denom_carvature ** 3     # 子午線曲率半径
        prime_carvature = cls.MAJOR_RADIUS_WGS84 / \
            denom_carvature                                  # 卯酉線曲率半径

        return math.sqrt((diffs[1] * meridian_carvature) ** 2 + (diffs[0] * prime_carvature) ** 2)

    @classmethod
    def calc_relative_quadrant(cls,
                               target: Union[Tuple[float], List[float]],
                               origin: Union[Tuple[float], List[float]]) -> int:

        diff_longi: float = target[0] - origin[0]
        diff_lati: float = target[1] - origin[1]

        # Compensation is needed only as for longitude.
        if abs(diff_longi) > 180.:
            abs_diff_longi = 360. - abs(target[0]) - abs(origin[0])
            if diff_longi > 0:
                diff_longi = - abs_diff_longi
            else:
                diff_longi = abs_diff_longi

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
        radian = math.atan2(coordinate[0], coordinate[1])

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
