

import math
from typing import Tuple, Union

import numpy as np



MAJOR_RADIUS_WGS84 = 6378137.000
MINOR_RADIUS_WGS84 = 6356752.314245
ECCENTRICITY = math.sqrt(1 - (MINOR_RADIUS_WGS84 / MAJOR_RADIUS_WGS84) ** 2)


def diff_geopos(longi_1, lati_1, longi_2, lati_2) -> Tuple[float]:
    diff_longi = longi_1 - longi_2
    diff_lati = lati_1 - lati_2
    
    # Compensation is needed only as for longitude.
    if abs(diff_longi) > math.pi:
        abs_diff_longi = 2 * math.pi - abs(longi_1) - abs(longi_2)
        if diff_longi > 0:
            diff_longi = - abs_diff_longi
        else:
            diff_longi = abs_diff_longi
                    
    return (diff_longi, diff_lati)


def relative_quadrant(longi_1, lati_1, longi_2, lati_2) -> int:
    diff_longi, diff_lati = diff_geopos(longi_1, lati_1, longi_2, lati_2)
    
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
    
    
def distance_hubeny(longi_1, lati_1, longi_2, lati_2) -> float:
    diff_longi, diff_lati = diff_geopos(longi_1, lati_1, longi_2, lati_2)
    mean_lati = (lati_1 + lati_2) / 2
    denom_carvature = math.sqrt(1 - (ECCENTRICITY * math.sin(mean_lati)) ** 2)
    meridian_carvature = MAJOR_RADIUS_WGS84 * (1 - ECCENTRICITY ** 2) / denom_carvature ** 3
    prime_carvature = MAJOR_RADIUS_WGS84 / denom_carvature
    return math.sqrt((diff_lati * meridian_carvature) ** 2 + (diff_longi * prime_carvature * math.cos(mean_lati)) ** 2)


def calc_relative_coordinate(longi_1, lati_1, longi_2, lati_2) -> Tuple[float]:
    diff_x = distance_hubeny(longi_1, lati_2, longi_2, lati_2)
    diff_y = distance_hubeny(longi_2, lati_1, longi_2, lati_2)
    quad = relative_quadrant(longi_1, lati_1, longi_2, lati_2)
    
    coordinate = []

    if quad in (1, 0, -1, -2):
        coordinate.append(diff_x)
        coordinate.append(diff_y)
    elif quad in (2, -3):
        coordinate.append(- diff_x)
        coordinate.append(diff_y)
    elif quad == 3:
        coordinate.append(- diff_x)
        coordinate.append(- diff_y)
    elif quad in (4, -4):
        coordinate.append(diff_x)
        coordinate.append(- diff_y)

    return tuple(coordinate)


class Position:
    
    ABS_TOL = 1e-16
    
    def __init__(self, longi: float, lati: float, degree: bool = False) -> None:
        self._pos = np.array([longi, lati])
        
        if degree:
            self._pos = self.to_radian(self._pos)
    
    def azimuth_from(self, p, degree: bool = False) -> float:
        delta_x, delta_y = calc_relative_coordinate(self.longi, self.lati, p.longi, p.lati)
        print(delta_x, delta_y)
        azim = math.pi / 2 - math.atan2(delta_y, delta_x)
        if azim < 0:
            azim += 2 * math.pi
        
        if degree:
            azim = self.to_degree(azim)
        return azim

    def azimuth_to(self, p, degree: bool = False) -> float:
        delta_x, delta_y = calc_relative_coordinate(p.longi, p.lati, self.longi, self.lati)
        azim = math.pi / 2 - math.atan2(delta_y, delta_x)
        if azim < 0:
            azim += 3 / 2 * math.pi
            
        if degree:
            azim = self.to_degree(azim)
        return azim
    
    def diff_from(self, p):
        diff_longi, diff_lati = diff_geopos(self.longi, self.lati, p.longi, p.lati)
        diff_pos = self.__class__(diff_longi, diff_lati) 
        return diff_pos
    
    def direction_from(self, p, degree: bool = False) -> float:
        delta_x, delta_y = calc_relative_coordinate(self.longi, self.lati, p.longi, p.lati)
        azim = - math.atan2(delta_x, delta_y)
        
        if math.isclose(azim, 0., abs_tol=self.ABS_TOL):
            azim = 0.
        if math.isclose(azim, - math.pi, abs_tol=self.ABS_TOL):
            azim = math.pi
        
        if degree:
            azim = self.to_degree(azim)
        return azim
    
    def direction_to(self, p, degree: bool = False) -> float:
        delta_x, delta_y = calc_relative_coordinate(p.longi, p.lati, self.longi, self.lati)
        azim = - math.atan2(delta_x, delta_y)
        
        if math.isclose(azim, 0., abs_tol=self.ABS_TOL):
            azim = 0.
        if math.isclose(azim, - math.pi, abs_tol=self.ABS_TOL):
            azim = math.pi
        
        if degree:
            azim = self.to_degree(azim)
        return azim
    
    def distance_from(self, p) -> float:
        return distance_hubeny(self.longi, self.lati, p.longi, p.lati)
    
    @property
    def longi(self):
        return self._pos[0]
    
    @property
    def lati(self):
        return self._pos[1]
    
    @staticmethod
    def to_radian(degree: Union[int, float, np.ndarray]):
        return degree / 180. * math.pi
    
    @staticmethod
    def to_degree(radian: Union[int, float, np.ndarray]):
        return radian / math.pi * 180.
