

import time
from typing import Dict, List
import unittest
import random

from pisat.base.component import Component
from pisat.model.datamodel import DataModelBase, cached_loggable, loggable


class Publisher(Component):
    pass


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
    

def create_new_model(publisher: Component) -> DataModel:
    model = DataModel(publisher.name)
    a = random.random()
    b = [random.random() for _ in range(3)]
    c = {key: random.random() for key in ("hello", "world", "!!!")}
    model.setup(a, b, c)
    
    return model

    
class TestDataModel(unittest.TestCase):
    
    def setUp(self) -> None:
        self.publisher_name = "publisher"
        self.publisher = Publisher(name=self.publisher_name)
    
    def test_publisher(self):        
        model = DataModel(self.publisher_name)
        self.assertEqual(model.publisher, self.publisher_name)
        
    def test_get_tag(self):
        dname = "test_data"
        
        model = DataModel(self.publisher_name)
        tag = model.get_tag(dname)
        self.assertEqual(tag, f"{self.publisher_name}-{dname}")
        
    def test_loggables(self):
        model = DataModel(self.publisher_name)
        names = ("a", "b", "c", "d")
        
        loggables = model.loggables
        for logg, name in zip(loggables, names):
            self.assertEqual(logg[0], name)
            
    def test_monitor(self):
        model = create_new_model(self.publisher)
        
        print()
        print(f"{model.get_tag('a')}: {model.a}")
        print(f"{model.get_tag('b')}: {model.b}")
        print(f"{model.get_tag('c')}: {model.c}")
        print(f"{model.get_tag('d')}: {model.d}")
        print()
        
    def test_cached_loggable(self):
        model = create_new_model(self.publisher)
        
        time_init = time.time()
        result = model.d
        time_first = time.time() - time_init
        
        for _ in range(10):
            time_init = time.time()
            self.assertEqual(result, model.d)
            self.assertLess(time.time() - time_init, time_first)
            
    def test_extract(self):
        model = create_new_model(self.publisher)
        
        expected_values = []
        expected_values.append(model.a)
        expected_values.extend(model.b)
        expected_values.extend(list(model.c.values()))
        expected_values.append(model.d)
        
        for true in model.extract().values():
            self.assertIn(true, expected_values)
            
            
if __name__ == "__main__":
    unittest.main()
