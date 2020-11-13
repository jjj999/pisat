
import math
from typing import Optional

from pisat.base.component import Component
from pisat.calc.position import Position


class Navigator(Component):
    
    ABS_TOL = 1e-16
    
    def __init__(self, goal: Position, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._goal = goal
        
    @property
    def goal(self):
        return self._goal
    
    def delta_angle(self, p: Position, heading: float, degree: Optional[str] = None) -> float:
        azim = self._goal.azimuth_from(p)
        delta = math.pi - heading + azim
        
        if math.isclose(delta, 0, abs_tol=self.ABS_TOL):
            delta = 0.
        if math.isclose(delta, - math.pi, abs_tol=self.ABS_TOL):
            delta = math.pi
            
        if degree:
            delta = self._goal.to_degree(delta)
        return delta
    
    def delta_distance(self, p: Position) -> float:
        return self._goal.distance_from(p) 
