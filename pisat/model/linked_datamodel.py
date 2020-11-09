
import inspect
from typing import Any, Dict, List, Optional

from pisat.base.component import Component
from pisat.model.datamodel import loggable, DataModelBase
    

class linked_loggable(loggable):
    
    def __init__(self,
                 loggable: loggable,
                 publisher: Component,
                 default: Any = None) -> None:
        super().__init__(loggable._fget)
        self._loggable = loggable
        self._model = None
        self._publisher = publisher
        self._default = default
    
    def __get__(self, obj: Any, type: Optional[type] = None):
        if obj is None:
            return self
        if self._fget is not None:
            if self._model is not None:
                return self._fget(self._model)
            else:
                return self._default
                
    @property
    def publisher(self):
        return self._publisher
    
    def extract(self, obj: Any, name: str, gen: str) -> Dict[str, str]:
        if self._fmat is None:
            return self._loggable.extract(obj, name, gen)
        else:
            return self._fmat(obj)
        
    def sync(self, model: DataModelBase):
        self._model = model
        
        
class LinkedDataModelBase(DataModelBase):
    
    def __init_subclass__(cls) -> None:
        cls._linked_loggables = inspect.getmembers(cls, lambda x: isinstance(x, linked_loggable))
        cls._Pub2Link: Dict[Component, List[linked_loggable]] = {}
        for _, linked in cls.linked_loggables:
            if cls._Pub2Link.get(linked.publisher) is None:
                cls._Pub2Link[linked.publisher] = []
            cls._Pub2Link[linked.publisher].append(linked)
    
    def sync(self, *models: DataModelBase):
        # NOTE If needless models are given, it works.
        for model in models:
            links = self._Pub2Link.get(model.publisher)
            if links is not None:
                for link in links:
                    link.sync(model)
    