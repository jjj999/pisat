
from typing import Optional
from pisat.base.component import Component
import unittest

from pisat.config import *


NAME_SENSOR = "sensor"

class TestSensor(Component):
    
    class DataModel(DataModelBase):        
            
        def setup(self, a, b, c, d):
            self._a = a
            self._b = b
            self._c = c
            self._d = d
            
        @loggable
        def a(self):
            return self._a
        
        @a.formatter
        def a(self):
            return {"a": str(self._a)}
        
        @loggable
        def b(self):
            return self._b
        
        @b.formatter
        def b(self):
            return {"b": str(self._b)}
        
        @loggable
        def c(self):
            return self._c
        
        @c.formatter
        def c(self):
            return {"c": str(self._c)}
        
        @loggable
        def d(self):
            return self._d
        
        @d.formatter
        def d(self):
            return {"d": str(self._d)}
        
    def __init__(self, name: Optional[None]) -> None:
        super().__init__(name=name)
        
    def get_data(self, a, b, c, d):
        model = self.DataModel(self.name)
        model.setup(a, b, c, d)
        return model
        
    
class LinkedDataModel(LinkedDataModelBase):
    
    a = linked_loggable(TestSensor.DataModel.a, NAME_SENSOR)
    b = linked_loggable(TestSensor.DataModel.b, NAME_SENSOR)
    
    
class TestLoggable(unittest.TestCase):
    
    def setUp(self) -> None:
        sensor = TestSensor("sensor")
        self.model = sensor.get_data(1, 2, 3, 4)
        
    def test_model(self):
        print(f"a: {self.model.a}, b: {self.model.b}, c: {self.model.c}, d: {self.model.d}")
        print(self.model.extract())
        
    def test_linked_model(self):
        linked = LinkedDataModel("test")
        linked.sync(self.model)
        print(linked.extract())
        
        
if __name__ == "__main__":
    unittest.main()
    