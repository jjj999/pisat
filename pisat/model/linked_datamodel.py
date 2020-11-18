

import inspect
from typing import Any, Dict, Generic, List, Optional, Tuple

from pisat.model.datamodel import (
    loggable, DataModelBase, Loggable, Model, GetReturn
)
from pisat.util.deco import class_property


class linked_loggable(loggable, Generic[Model, GetReturn, Loggable]):
    
    def __init__(self,
                 loggable: loggable,
                 publisher: str,
                 logging: bool = True,
                 default: Optional[Any] = None) -> None:
        super().__init__(loggable._fget)
        self._loggable = loggable
        self._model = None
        self._publisher = publisher
        self._logging = logging
        self._default = default
    
    def __get__(self, obj: Any, clazz: Optional[type] = None):
        if obj is None:
            return self
        if self._fget is not None:
            if self._model is not None:
                return self._fget(self._model)
            else:
                return self._default
            
    def extract(self, model: Model, dname: str) -> Dict[str, Loggable]:
        # Enable not to log the liked data.
        if self._logging:
            return super().extract(model, dname)
        else:
            return {}
            
    @property
    def publisher(self) -> str:
        return self._publisher
        
    def sync(self, model: DataModelBase) -> None:
        self._model = model
        
        
class LinkedDataModelBase(DataModelBase):
    
    _linked_loggables: List[Tuple[str, linked_loggable]]
    _Pub2Link: Dict[str, List[linked_loggable]]
    
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        
        cls._linked_loggables = inspect.getmembers(cls, lambda x: isinstance(x, linked_loggable))
        cls._Pub2Link = {}
        for _, linked in cls._linked_loggables:
            if cls._Pub2Link.get(linked.publisher) is None:
                cls._Pub2Link[linked.publisher] = []
            cls._Pub2Link[linked.publisher].append(linked)
            
    @class_property
    def linked_loggables(cls):
        return cls._linked_loggables
    
    def sync(self, *models: DataModelBase):
        # NOTE If needless models are given, it works.
        for model in models:
            links = self._Pub2Link.get(model.publisher)
            if links is not None:
                for link in links:
                    link.sync(model)
    