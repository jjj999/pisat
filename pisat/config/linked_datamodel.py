
import inspect
from typing import Any, Dict, List, Optional, Tuple

from pisat.config.datamodel import loggable, DataModelBase

    
class LinkNotSetError(Exception):
    """Raised if a link doesn't be set and a loggable is retrieved."""
    pass
    

class linked_loggable(loggable):
    
    def __init__(self,
                 loggable: loggable,
                 comp_name: str) -> None:
        super().__init__(loggable._fget)
        self._loggable = loggable
        self._model = None
        self._comp_name = comp_name
    
    def __get__(self, obj: Any, type: Optional[type] = None):
        if obj is None:
            return self
        if self._fget is not None:
            if self._model is not None:
                return self._fget(self._model)
            else:
                raise LinkNotSetError(
                    "An object which links to the loggable is not set."
                )
                
    @property
    def generate_component(self):
        return self._comp_name
    
    def extract(self, obj: Any) -> str:
        if self._fmat is None:
            return self._loggable._fmat(self._model)
        else:
            return self._fmat(obj)
        
    def sync(self, model: DataModelBase):
        self._model = model
        
        
class LinkedDataModelBase(DataModelBase):
    
    @classmethod
    def get_linked_loggables(cls):
        return inspect.getmembers(cls, lambda x: isinstance(x, linked_loggable))
        
    @classmethod
    def _get_Name2Link(cls) -> Dict[str, List[linked_loggable]]:
        result = {}
        for _, val in cls.get_loggables():
            d = result.get(val.generate_component)
            if d is None:
                result[val.generate_component] = [val]
            else:
                result[val.generate_component].append(val)
                
        return result
    
    def sync(self, *models: DataModelBase):
        Name2Link = self._get_Name2Link()
        
        for model in models:
            links = Name2Link.get(model.generate_component)
            if links is not None:
                for link in links:
                    link.sync(model)
    