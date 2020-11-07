
import random
import unittest

from pisat.config.linked_datamodel import LinkedDataModelBase, linked_loggable
from pisat.sensor.number_generator import NumberGenerator
from pisat.sensor.sensor_base import SensorGroup


NAME_NUMGEN1 = "gen1"
NAME_NUMGEN2 = "gen2"
NAME_NUMGEN3 = "gen3"

RANGE_NUMGEN1 = (0, 10)
RANGE_NUMGEN2 = (10, 20)
RANGE_NUMGEN3 = (20, 30)


class TestDataModel(LinkedDataModelBase):
    
    num1 = linked_loggable(NumberGenerator.DataModel.num, NAME_NUMGEN1)
    num2 = linked_loggable(NumberGenerator.DataModel.num, NAME_NUMGEN2)
    num3 = linked_loggable(NumberGenerator.DataModel.num, NAME_NUMGEN3)
    
    @num1.formatter
    def num1(self):
        return {"num1": self.num1}
    
    @num2.formatter
    def num2(self):
        return {"num2": self.num2}
    
    @num3.formatter
    def num3(self):
        return {"num3": self.num3}


class TestSesorGroup(unittest.TestCase):
    
    def setUp(self) -> None:
        self.numgen1 = NumberGenerator(lambda: random.uniform(*RANGE_NUMGEN1), name=NAME_NUMGEN1)
        self.numgen2 = NumberGenerator(lambda: random.uniform(*RANGE_NUMGEN2), name=NAME_NUMGEN2)
        self.numgen3 = NumberGenerator(lambda: random.uniform(*RANGE_NUMGEN3), name=NAME_NUMGEN3)
        
        self.group = SensorGroup(TestDataModel)
        self.group.add(self.numgen1, self.numgen2, self.numgen3)
        
    def test_sensor_len(self):
        self.assertEqual(len(self.group), 3)
        
    def test_read(self):
        data = self.group.read()
        
        self.assertGreaterEqual(data.num1, RANGE_NUMGEN1[0])
        self.assertLess(data.num1, RANGE_NUMGEN1[1])
        
        self.assertGreaterEqual(data.num2, RANGE_NUMGEN2[0])
        self.assertLess(data.num2, RANGE_NUMGEN2[1])
        
        self.assertGreaterEqual(data.num3, RANGE_NUMGEN3[0])
        self.assertLess(data.num3, RANGE_NUMGEN3[1])
        
        
if __name__ == "__main__":
    unittest.main()
