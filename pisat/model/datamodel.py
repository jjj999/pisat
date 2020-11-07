
import inspect
from typing import Any, Callable, Dict, Optional, Tuple, Type


class loggable:
    
    def __init__(self, 
                 fget: Optional[Callable[[Any], Any]] = None,
                 fmat: Optional[Callable[[Any], Any]] = None) -> None:
        self._fget = fget
        self._fmat = fmat
        
    def __get__(self, obj: Any, type: Optional[type] = None):
        if obj is None:
            return self
        if self._fget is not None:
            return self._fget(obj)
        raise AttributeError
    
    def getter(self, fget: Optional[Callable[[Any], Any]]):
        self._fget = fget
        return self
    
    def formatter(self, fmat: Optional[Callable[[Any], Any]]):
        self._fmat = fmat
        return self
    
    def extract(self, obj: Any) -> str:
        return self._fmat(obj)
    

class DataModelBase:
    
    def __init__(self, comp_name: str) -> None:
        self._comp_name = comp_name
        
    def setup(self):
        pass
        
    @property
    def generate_component(self):
        return self._comp_name
    
    @classmethod
    def get_loggables(cls):
        return inspect.getmembers(cls, lambda x: isinstance(x, loggable))
    
    def extract(self):
        result = {}
        for _, val in self.get_loggables():
            result.update(val.extract(self))
            
        return result
        