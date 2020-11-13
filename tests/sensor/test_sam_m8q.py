

import unittest

from pisat.handler import PyserialSerialHandler
from pisat.sensor import SamM8Q
from pisat.tester.sensor import SensorTestor


PORT_SAMM8Q = "/dev/serial0"


class TestSAMM8Q(unittest.TestCase):
    
    def setUp(self) -> None:
        handler = PyserialSerialHandler(PORT_SAMM8Q, baudrate=9600)
        self.samm8q = SamM8Q(handler, name="sam_m8q")
        self.testor = SensorTestor(self.samm8q)
        
    def test_observe(self):
        self.testor.print_data()
        
    def test_bench_mark(self):
        result = self.testor.exec_benchmark(show=True)
        print(f"time to read 100 times: {result}")
        
        
if __name__ == "__main__":
    unittest.main()
