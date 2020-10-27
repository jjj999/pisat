
import time
from typing import Dict, List, Optional, Tuple

from pisat.config.type import Logable
from pisat.handler.digital_input_handler_base import DigitalInputHandlerBase
from pisat.handler.digital_output_handler_base import DigitalOutputHandlerBase
from pisat.sensor.sensor_base import SensorBase


class HcSr04(SensorBase):
    
    # TODO
    DATA_NAMES = ()
    DEFAULT_VALUES = {}
    
    TIME_OUTPUT_PULSE = 1e-6
    
    # m/s at 15 celsius deg
    VELOCITY_SOUND_AIR = 340.65
    
    def __init__(self,
                 input: Optional[DigitalInputHandlerBase] = None,
                 output: Optional[DigitalOutputHandlerBase] = None,
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(debug=debug, name=name)
        if not debug:
            if input is None and output is None:
                raise ValueError(
                    "'input' and 'output' both must be given when not debugging mode."
                )
        else:
            return
        
        self._handler_input = input
        self._handler_output = output
        
    # TODO
    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        pass
    
    # TODO
    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        pass
        
    def _read_distance(self):
        self._output_pulse()
        time_echo = self._observe_time_echo()
        return time_echo * self.VELOCITY_SOUND_AIR / 2
    
    def _output_pulse(self):
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
