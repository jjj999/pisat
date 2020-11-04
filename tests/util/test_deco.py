
import unittest

from pisat.util.deco import restricted_setter, restricted_range_setter


class TestRestrictedSetterClass:
    
    def __init__(self, a: int, b: str) -> None:
        self._a = a
        self._b = b
        
    @property
    def a(self):
        return self._a
    
    @a.setter
    @restricted_setter(0, 1, 2)
    def a(self, val: int):
        self._a = val
        
    @property
    def b(self):
        return self._b
    
    @b.setter
    @restricted_setter("hello", "world")
    def b(self, val: str):
        self._b = val
        

class TestRestrictedRangeSetterClass:
    
    def __init__(self, a: int, b: int, c: int, d: int) -> None:
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        
    @property
    def a(self):
        return self._a
    
    @a.setter
    @restricted_range_setter(0, 10)
    def a(self, val: int):
        self._a = val
        
    @property
    def b(self):
        return self._b
    
    @b.setter
    @restricted_range_setter(0, 10, ismin=False)
    def b(self, val: int):
        self._b = val
        
    @property
    def c(self):
        return self._c
    
    @c.setter
    @restricted_range_setter(0, 10, ismax=False)
    def c(self, val: int):
        self._c = val
        
    @property
    def d(self):
        return self._d
    
    @d.setter
    @restricted_range_setter(0, 10, ismin=False, ismax=False)
    def d(self, val: int):
        self._d = val
        

class TestDeco(unittest.TestCase):
    
    def setUp(self) -> None:
        self.obj_restricted_setter = TestRestrictedSetterClass(0, "hello")
        self.obj_restricted_range_setter = TestRestrictedRangeSetterClass(1, 1, 1, 1)
        
    def test_restricted_setter(self):
        self.obj_restricted_setter.a = 0
        self.obj_restricted_setter.a = 1
        
        self.obj_restricted_setter.b = "hello"
        self.obj_restricted_setter.b = "world"
        
    def test_restricted_setter_illegal(self):
        try:
            self.obj_restricted_setter.a = 100
            raise Exception
        except ValueError:
            pass
        
        try:
            self.obj_restricted_setter.b = -100
            raise Exception
        except ValueError:
            pass
        
    def test_restricted_range_setter(self):
        for val in range(0, 11):
            self.obj_restricted_range_setter.a = val
        for val in range(1, 11):
            self.obj_restricted_range_setter.b = val
        for val in range(0, 10):
            self.obj_restricted_range_setter.c = val
        for val in range(1, 10):
            self.obj_restricted_range_setter.d = val
            
    def test_restricted_range_setter_illegal(self):
        try:
            for val in range(0, 11):
                self.obj_restricted_range_setter.b = val
            raise Exception
        except ValueError:
            pass
        
        try:
            for val in range(0, 11):
                self.obj_restricted_range_setter.c = val
            raise Exception
        except ValueError:
            pass
        
        try:
            for val in range(0, 11):
                self.obj_restricted_range_setter.d = val
            raise Exception
        except ValueError:
            pass
        
if __name__ == "__main__":
    unittest.main()
        