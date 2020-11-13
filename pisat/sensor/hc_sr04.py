
import time
from typing import Optional

from pisat.handler.digital_input_handler_base import DigitalInputHandlerBase
from pisat.handler.digital_output_handler_base import DigitalOutputHandlerBase
from pisat.model.datamodel import DataModelBase, loggable
from pisat.sensor.sensor_base import SensorBase


class HcSr04(SensorBase):
    
    
    class DataModel(DataModelBase):
        
        def setup(self, dist):
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
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._handler_input = input
        self._handler_output = output
        
    def read(self):
        dist = self._read_distance()
        
        model = self.DataModel(self.name)
        model.setup(dist)
        return model
        
    def _read_distance(self) -> float:
        self._output_pulse()
        time_echo = self._observe_time_echo()
        return time_echo * self.VELOCITY_SOUND_AIR / 2
    
    def _output_pulse(self) -> None:
        self._handler_output.set_high()
        time.sleep(self.TIME_OUTPUT_PULSE)
        self._handler_output.set_low()
        
    def _observe_time_echo(self) -> float:
        while not self._handler_input.observe():
            pass
        time_init = time.time()
        
        while self._handler_input.observe():
            pass
        
        return time.time() - time_init
