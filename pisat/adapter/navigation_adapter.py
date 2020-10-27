
import math
from typing import Dict, List, Optional, Tuple, Union

from pisat.adapter.gps_adapter import GpsAdapter
from pisat.config.type import Logable
from pisat.config.dname import (
    GPS_LATITUDE_NS, GPS_LONGITUDE, GPS_LATITUDE,
    DISTANCE, GPS_LONGITUDE_EW, RELATIVE_COORDINATE_X, 
    RELATIVE_COORDINATE_Y, ANGLE_RADIAN_FROM_NORTH_POLE
)
from pisat.util.gps_parser import GPSParser


class NavigationAdapter(GpsAdapter):
    
    # TODO
    DATA_NAMES: Tuple[str] = (
        DISTANCE, RELATIVE_COORDINATE_X, RELATIVE_COORDINATE_Y, 
        ANGLE_RADIAN_FROM_NORTH_POLE, "ANGLE_RADIAN_TO_GOAL"
    )
    DATA_REQUIRES: Dict[str, Tuple[str]] = {
        DISTANCE:                       (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
        RELATIVE_COORDINATE_X:          (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
        RELATIVE_COORDINATE_Y:          (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
        ANGLE_RADIAN_FROM_NORTH_POLE:   (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS),
        # TODO
        "ANGLE_RADIAN_TO_GOAL":         (GPS_LONGITUDE, GPS_LONGITUDE_EW, GPS_LATITUDE, GPS_LATITUDE_NS, "ANGLE_HEADING_RADIAN_FROM_NORTH_POLE")
    }
    
    # TODO
    def calc(self, data: Dict[str, Logable], *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        longitude = data.get(GPS_LONGITUDE)
        longitude_ew = data.get(GPS_LONGITUDE_EW)
        latitude = data.get(GPS_LATITUDE)
        latitude_ns = data.get(GPS_LATITUDE_NS)
        target = (GPSParser.convert2coordinate(longitude, longitude_ew),
                  GPSParser.convert2coordinate(latitude, latitude_ns))
        # TODO
        angle_heading = data.get("ANGLE_HEADING_RADIAN_FROM_NORTH_POLE")

        if len(dnames) == 0:
            distance = self.calc_distance(target, self._goal)
            coordinate = self.calc_relative_coordinate(target, self._goal)
            angle_position = self.calc_angle_from_north(coordinate)
            angle2goal = self.calc_relative_angle_heading(angle_heading, angle_position)
            return {DISTANCE: distance,
                    RELATIVE_COORDINATE_X: coordinate[0],
                    RELATIVE_COORDINATE_Y: coordinate[1],
                    ANGLE_RADIAN_FROM_NORTH_POLE: angle_position,
                    "ANGLE_RADIAN_TO_GOAL": angle2goal}
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
                # TODO
                elif dname == "ANGLE_RADIAN_TO_GOAL":
                    result["ANGLE_RADIAN_TO_GOAL"] = self.calc_relative_angle_heading_from(angle_heading, target, self._goal)
                    
            return result

    @classmethod
    def calc_relative_angle_heading(cls, 
                                    offset_heading: float,
                                    offset_position: float,
                                    isradian: True) -> float:
        if isradian:
            return math.pi + offset_position - offset_heading
        else:
            return 180. + offset_position - offset_heading
        
    @classmethod
    def calc_relative_angle_heading_from(cls,
                                         offset_heading: float,
                                         target: Tuple[float],
                                         origin: Tuple[float],
                                         isradian: True) -> float:
        offset_position = cls.calc_relative_angle(target, origin, isradian=isradian)
        return cls.calc_relative_angle_heading(offset_heading, offset_position, isradian=isradian)
