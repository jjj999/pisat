
class cached_property:
    
    def __init__(self, func) -> None:
        self.__doc__ = getattr(func, "__doc__")
        self._func = func
        
    def __get__(self, instance, owner = None):
        if owner is None:
            return self
        
        value = self._func(instance)
        instance.__dict__[self._func.__name__] = value
        
        return value
        