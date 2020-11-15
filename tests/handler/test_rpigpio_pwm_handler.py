
import time
import unittest

from pisat.handler import RpiGpioPWMHandler


PIN = 25


class TestPigpioPWMHandler(unittest.TestCase):
    
    def setUp(self) -> None:
        self.handler = RpiGpioPWMHandler(PIN, 1000)
        
    def test_is_valid_duty(self):
        for i in range(100):
            self.assertTrue(self.handler.is_valid_duty(i))
            
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
        self.handler.stop()
        
        self.assertEqual(self.handler.duty, 100)


if __name__ == "__main__":
    unittest.main()
