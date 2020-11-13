

import unittest

from pisat.handler import PyserialSerialHandler
from pisat.sensor import Gysfdmaxb
from pisat.tester.sensor import SensorTestor


PORT_GYFSDMAXB = "/dev/serial0"


class TestGYSFDMAXB(unittest.TestCase):
    
    def setUp(self) -> None:
        handler = PyserialSerialHandler(PORT_GYFSDMAXB, baudrate=9600)
        self.gysfdmaxb = Gysfdmaxb(handler, name="gysdfdmaxb")
        self.testor = SensorTestor(self.gysfdmaxb)
        
    def test_observe(self):
        self.testor.print_data()
        
    def test_bench_mark(self):
        result = self.testor.exec_benchmark(show=True)
        print(f"time to read 100 times: {result}")
        
        
if __name__ == "__main__":
    unittest.main()
