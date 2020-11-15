

import inspect
from typing import Callable, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from pisat.util.deco import class_property


Loggable = TypeVar("Loggable", str, bytes, int, float, None)
Model = TypeVar("Model")
GetReturn = TypeVar("GetReturn")


class loggable(Generic[Model, GetReturn]):
    
    def __init__(self, 
                 fget: Optional[Callable[[Model], GetReturn]] = None,
                 fmat: Optional[Callable[[Model], Dict[str, Loggable]]] = None) -> None:
        self.__doc__ = getattr(fget, "__doc__")
        self._fget = fget
        self._fmat = fmat
        
    def __get__(self, obj: Model, clazz: Optional[Type[Model]] = None):
        if obj is None:
            return self
        if self._fget is not None:
            return self._fget(obj)
        raise AttributeError(
            "'getter' has not been set yet."
        )
    
    def getter(self, fget: Optional[Callable[[Model], GetReturn]]):
        self._fget = fget
        return self
    
    def formatter(self, fmat: Callable[[Model], Dict[str, Loggable]]):
        self._fmat = fmat
        return self
    
    def extract(self, model: Model, dname: str) -> Dict[str, Loggable]:
        # Default formatting
        if self._fmat is None:
            name = model.get_tag(dname)
            return {name: getattr(model, dname)}
        # User-defined formatting
        else:
            return self._fmat(model)
    

class cached_loggable(loggable):
    
    def __init__(self,
                 fget: Optional[Callable[[Model], GetReturn]] = None,
                 fmat: Optional[Callable[[Model], Dict[str, Loggable]]] = None) -> None:
        super().__init__(fget=fget, fmat=fmat)
        
    def __get__(self, obj: Model, clazz: Optional[Type[Model]] = None):
        if obj is None:
            return self
        if self._fget is not None:
            value = self._fget(obj)
            obj.__dict__[self._fget.__name__] = value
            return value
        raise AttributeError(
            "'getter' has not been set yet."
        )


class DataModelBase:
    
    def __init_subclass__(cls) -> None:
        cls._loggables = inspect.getmembers(cls, lambda x: isinstance(x, loggable))
    
    def __init__(self, publisher: str) -> None:
        if not isinstance(publisher, str):
            raise TypeError("'publisher' must be str.")
        
        self._publisher = publisher
        
    def setup(self):
        pass
        
    @property
    def publisher(self) -> str:
        return self._publisher
    
    def get_tag(self, dname: str) -> str:
        return f"{self.publisher}-{dname}"
    
    @class_property
    def loggables(cls) -> List[Tuple[str, loggable]]:
        return cls._loggables
    
    def extract(self) -> Dict[str, Loggable]:
        result = {}
        for dname, logg in self.loggables:
            result.update(logg.extract(self, dname))
            
        return result
        