

from typing import Callable, Generic, Optional, Type, TypeVar, Union


def restricted_setter(*args):
    if not len(args):
        raise ValueError(
            "This method needs 1 or more arguments."
        )
        
    def wrapper(func):
        
        def setter(self, val):
            str_args = tuple(map(str, args))
            if len(str_args) > 1:
                formatted = [", ".join(str_args[:-1]), str_args[-1]]
                formatted = " or ".join(formatted)
            else:
                formatted = str_args[0]
            
            if val not in args:
                raise ValueError(
                    f"'{func.__name__}' must be {formatted}."
                )
                
            return func(self, val)
        
        return setter
    
    return wrapper


def restricted_range_setter(inf: Union[int, float], 
                            sup: Union[int, float],
                            ismin: bool = True,
                            ismax: bool = True):
    def wrapper(func):
        
        def format_range(ismin: bool, ismax: bool) -> str:
            lower = "<=" if ismin else "<"
            upper = "<=" if ismax else "<"
            return f"{inf} {lower} {func.__name__} {upper} {sup}" 
        
        def setter(self, val: Union[int, float]):
            condition = None
            if ismin:
                if ismax:
                    condition = inf <= val <= sup
                else:
                    condition = inf <= val < sup
            else:
                if ismax:
                    condition = inf < val <= sup
                else:
                    condition = inf < val < sup
                    
            if not condition:
                raise ValueError(
                    f"'{func.__name__}' must be {format_range(ismin, ismax)}"
                )
                
            return func(self, val)
        
        return setter

    return wrapper


Object = TypeVar("Object")
ReturnGetter = TypeVar("ReturnGetter")


class class_property(Generic[Object, ReturnGetter]):
    
    def __init__(self,
                 fget: Callable[[Object], ReturnGetter]) -> None:
        self.__doc__ = getattr(fget, "__doc__")
        self._fget = fget
        
    def __get__(self, obj: Union[Object, None], clazz: Optional[Type[Object]] = None) -> ReturnGetter:
        if clazz is None:
            clazz = type(obj)
            
        if self._fget is not None:
            return self._fget(clazz)
        raise AttributeError(
            "'getter' has not been set yet."
        )
            
    def getter(self, fget: Callable[[Object], ReturnGetter]):
        self._fget = fget
        return self
        

class cached_property(Generic[Object, ReturnGetter]):
    
    def __init__(self, 
                 fget: Callable[[Object], ReturnGetter]) -> None:
        self.__doc__ = getattr(fget, "__doc__")
        self._fget = fget
        
    def __get__(self, obj: Union[Object, None], clazz: Optional[Type[Object]] = None) -> ReturnGetter:
        if obj is None:
            return self
        if self._fget is not None:
            value = self._fget(obj)
            obj.__dict__[self._fget.__name__] = value
            return value
        raise AttributeError(
            "'getter' has not been set yet."
        )
    
    def getter(self, fget: Callable[[Object], ReturnGetter]):
        self._fget = fget
        return self
    
    
class cached_class_property(Generic[Object, ReturnGetter]):
    
    def __init__(self,
                 fget: Callable[[Object], ReturnGetter]) -> None:
        self.__doc__ = getattr(fget, "__doc__")
        self._fget = fget
        self._result: Union[ReturnGetter, None] = None
        
    def __get__(self, obj: Union[Object, None], clazz: Optional[Type[Object]] = None) -> ReturnGetter:
        if clazz is None:
            clazz = type(obj)
        
        if self._fget is not None:
            if self._result is None:
                self._result = self._fget(clazz)
            return self._result
        raise AttributeError(
            "'getter' has not been set yet."
        )
        
    def getter(self, fget: Callable[[Object], ReturnGetter]):
        self._fget = fget
        return self
