
import inspect
from typing import Any, Dict, List, Optional, Tuple

from pisat.config.loggable import loggable, DataModelBase

    
class LinkNotSetError(Exception):
    """Raised if a link doesn't be set and a loggable is retrieved."""
    pass
    

class linked_loggable(loggable):
    
    def __init__(self,
                 loggable: loggable,
                 comp_name: str) -> None:
        super().__init__(loggable._fget)
        self._loggable = loggable
        self._obj = None
        self._comp_name = comp_name
    
    def __get__(self, obj: Any, type: Optional[type] = None):
        if obj is None:
            return self
        if self._fget is not None:
            if self._obj is not None:
                return self._fget(self._obj)
            else:
                raise LinkNotSetError(
                    "An object which links to the loggable is not set."
                )
    
    def extract(self, obj: Any) -> str:
        if self._fmat is None:
            return self._loggable._fmat(self._obj)
        else:
            return self._fmat(obj)
        
    def sync(self, obj: DataModelBase):
        self._obj = obj
        
        
class LinkedDataModelBase(DataModelBase):
    
    @classmethod
    def get_linked_loggables(cls):
        return inspect.getmembers(cls, lambda x: isinstance(x, linked_loggable))
        
    @classmethod
    def _get_Name2Link(cls) -> Dict[str, List[linked_loggable]]:
        result = {}
        for _, val in cls.get_loggables():
            d = result.get(val._comp_name)
            if d is None:
                result[val._comp_name] = [val]
            else:
                result[val._comp_name].append(val)
                
        return result
    
    def sync(self, *obj: Tuple[DataModelBase, ...]):
        Name2Link = self._get_Name2Link()
        
        for o in obj:
            links = Name2Link.get(o._comp_name)
            if links is not None:
                for link in links:
                    link.sync(o)
    