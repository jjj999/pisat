

import time

from pisat.model.datamodel import DataModelBase
from pisat.sensor.sensor_base import SensorBase


class SensorTestor:
    
    def __init__(self, sensor: SensorBase) -> None:
        if not isinstance(sensor, SensorBase):
            raise TypeError(
                "'sensor' must be an instance of subclasses of SensorBase."
            )
            
        self._sensor = sensor
        
    @staticmethod
    def _print_data(data: DataModelBase):
        print()
        for name, val in data.extract().items():
            print(f"{name}: {val}")
        print()
        
    def print_data(self):
        data = self._sensor.read()
        self._print_data(data)
        
    def exec_benchmark(self, times: int = 100, show: bool = False) -> float:
        time_total = 0.
        for _ in range(times):
            time_init = time.time()
            data = self._sensor.read()
            time_total += time.time() - time_init
            
            if show:
                self._print_data(data)
                
        return time_total
