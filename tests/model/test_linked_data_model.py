
from pisat.base.component import Component
import time
from typing import Dict, List, Optional
import unittest
import random

from pisat.model import *
from pisat.sensor import SensorBase


NAME_PUBLISHER_1 = "publisher1"
NAME_PUBLISHER_2 = "publisher2"


class Publisher(SensorBase):


    class DataModel(DataModelBase):
        
        def setup(self, a: float, b: List[float], c: Dict[str, float]):
            self._a = a
            self._b = b
            self._c = c
            
        @loggable
        def a(self):
            return self._a
        
        @loggable
        def b(self):
            return self._b
        
        @b.formatter
        def b(self):
            name = self.get_tag("b")
            return {f"{name}_0": self._b[0], f"{name}_1": self._b[1], f"{name}_2": self._b[2]}
        
        @loggable
        def c(self) -> Dict[str, float]:
            return self._c
        
        @c.formatter
        def c(self):
            name = self.get_tag("c")
            return {f"{name}_{key}": val for key, val in self._c.items()}
        
        @cached_loggable
        def d(self) -> float:
            time.sleep(0.1)
            result = 0
            for val in self._b:
                result += val
            return result
        
        
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(handler=None, name=name)
        
    def read(self):
        model = self.DataModel(self.name)
        
        a = random.random()
        b = [random.random() for _ in range(3)]
        c = {key: random.random() for key in ("hello", "world", "!!!")}
        
        model.setup(a, b, c)
        return model
    
    
class Reserver(Component):

    class LinkedDataModel(LinkedDataModelBase):
        
        a = linked_loggable(Publisher.DataModel.a, NAME_PUBLISHER_1)
        b = linked_loggable(Publisher.DataModel.b, NAME_PUBLISHER_1)
        c = linked_loggable(Publisher.DataModel.c, NAME_PUBLISHER_1)
        d = linked_loggable(Publisher.DataModel.d, NAME_PUBLISHER_1)
        e = linked_loggable(Publisher.DataModel.a, NAME_PUBLISHER_2)
        f = linked_loggable(Publisher.DataModel.b, NAME_PUBLISHER_2)
        
        @cached_loggable
        def g(self):
            return self.a * self.d
        
    def get_model(self, *models):
        linked = self.LinkedDataModel(self.name)
        linked.sync(*models)
        return linked
    
    
class TestLinkedDataModel(unittest.TestCase):
    
    def setUp(self) -> None:
        self.publisher1 = Publisher(name=NAME_PUBLISHER_1)
        self.publisher2 = Publisher(name=NAME_PUBLISHER_2)
        self.reserver = Reserver(name="reserver")
        
    def test_monitor(self):
        model1 = self.publisher1.read()
        model2 = self.publisher2.read()
        
        linked = self.reserver.get_model(model1, model2)
        
        print()
        print(f"{linked.get_tag('a')}: {linked.a}")
        print(f"{linked.get_tag('b')}: {linked.b}")
        print(f"{linked.get_tag('c')}: {linked.c}")
        print(f"{linked.get_tag('d')}: {linked.d}")
        print(f"{linked.get_tag('e')}: {linked.e}")
        print(f"{linked.get_tag('f')}: {linked.f}")
        print(f"{linked.get_tag('g')}: {linked.g}")
        print()
        
    def test_sync(self):
        model1 = self.publisher1.read()
        model2 = self.publisher2.read()
        
        linked = self.reserver.get_model(model1, model2)
        
        self.assertEqual(model1.a, linked.a)
        self.assertEqual(model1.b, linked.b)
        self.assertEqual(model1.c, linked.c)
        self.assertEqual(model1.d, linked.d)
        self.assertEqual(model2.a, linked.e)
        self.assertEqual(model2.b, linked.f)


if __name__ == "__main__":
    unittest.main()