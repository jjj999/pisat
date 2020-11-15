
import time
from typing import Optional, Union

from pisat.handler.digital_input_handler_base import DigitalInputHandlerBase
from pisat.handler.digital_output_handler_base import DigitalOutputHandlerBase
from pisat.model.datamodel import DataModelBase, loggable
from pisat.sensor.sensor_base import SensorBase


class HcSr04(SensorBase):
    
    
    class DataModel(DataModelBase):
        
        def setup(self, dist: Optional[float] = None):
            self._dist = dist
            
        @loggable
        def dist(self):
            return self._dist
    
    
    # sec
    TIME_OUTPUT_PULSE = 1e-6
    
    # m/s at 15 celsius deg
    VELOCITY_SOUND_AIR = 340.65
    
    def __init__(self,
                 input: DigitalInputHandlerBase,
                 output: DigitalOutputHandlerBase,
                 timeout: float = -1.,
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._handler_input = input
        self._handler_output = output
        self._timeout = timeout
        
    @property
    def timeout(self):
        return self._timeout
    
    @timeout.setter
    def timeout(self, val: Union[int, float]):
        if not isinstance(val, (int, float)):
            raise TypeError(
                "'timeout' must be int or float"
            )
        self._timeout = val
        
    def read(self):
        dist = self._read_distance(self._timeout)
        
        model = self.DataModel(self.name)
        model.setup(dist)
        return model
        
    def _read_distance(self, timeout: float = -1.) -> Optional[float]:
        self._output_pulse()
        time_echo = self._observe_time_echo(timeout=timeout)
        if time_echo is None:
            return None
        else:
            return time_echo * self.VELOCITY_SOUND_AIR / 2
    
    def _output_pulse(self) -> None:
        self._handler_output.set_high()
        time.sleep(self.TIME_OUTPUT_PULSE)
        self._handler_output.set_low()
        
        
    def _observe_time_echo(self, timeout: float = -1.) -> Optional[float]:
        time_temp = time.time()
        while not self._handler_input.observe():
            if timeout > 0 and time.time() - time_temp > timeout:
                return None
        
        time_init = time.time()
        
        time_temp = time.time()
        while self._handler_input.observe():
            if timeout > 0 and time.time() - time_temp > timeout:
                return None
        
        return time.time() - time_init
