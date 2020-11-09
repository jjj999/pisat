
from typing import Callable, Optional, Union

from pisat.config.datamodel import DataModelBase, loggable
from pisat.sensor.sensor_base import SensorBase


class NumberGenerator(SensorBase):
    

    class DataModel(DataModelBase):
                
        def setup(self, num):
            self._num = num
            
        @loggable
        def num(self):
            return self._num

    
    def __init__(self, func: Callable[[], Union[int, float]], name: Optional[str]) -> None:
        super().__init__(name=name)
        self._func = func
        
    def read(self):
        num = self._func()
        model = self.DataModel(self.name)
        model.setup(num)
        
        return model
        