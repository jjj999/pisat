
import random
import unittest

from pisat.sensor.number_generator import NumberGenerator


class TestNumberGenerator(unittest.TestCase):
    
    def setUp(self) -> None:
        fun1 = lambda: random.uniform(0, 10)
        
        self.numgen1 = NumberGenerator(fun1, name="numgen1")
        
    def test_read(self):
        print(self.numgen1.read().extract())
        
        
if __name__ == "__main__":
    unittest.main()
    