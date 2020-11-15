
import time
import unittest

import pigpio

from pisat.handler import PigpioPWMHandler


PIN = 25


class TestPigpioPWMHandler(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        self.handler = PigpioPWMHandler(pi, PIN, 1000)
        
    def test_calc_true_duty(self):
        range = 40000
        self.assertEqual(self.handler.calc_true_duty(range, 50), 20000)
        self.assertEqual(self.handler.calc_true_duty(range, 10), 4000)
        self.assertEqual(self.handler.calc_true_duty(range, 100), 40000)
        print(self.handler.calc_true_duty(range, 100 / 3))
        print(self.handler.calc_true_duty(range, 100 / 7))
        
    def test_is_valid_duty(self):
        for i in range(100):
            self.assertTrue(self.handler.is_valid_duty(i))
            
    def test_is_valid_range(self):
        for i in range(25, 40000):
            self.assertTrue(self.handler.is_valid_range(i))
            
    def test_set_duty(self):
        self.handler.stop()
        self.handler.set_duty(50)
        self.assertEqual(50, self.handler.duty)
        self.handler.set_duty(0)
        
    def test_start_stop(self):
        self.handler.start()
        for i in range(101):
            self.handler.set_duty(i)
            time.sleep(0.1)
        self.stop()
        
        self.assertEqual(self.handler.duty, 100)


if __name__ == "__main__":
    unittest.main()
