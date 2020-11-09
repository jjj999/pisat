#! python3

"""

pisat.core.logger.refque
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implementation of reference to data in LogQueue
with a lock. 

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
OTHER INFORMATION

"""

from threading import Lock
from collections import deque
from typing import Deque,  Generic, Optional, TypeVar
from copy import deepcopy

from pisat.base.component import Component
from pisat.model.datamodel import DataModelBase


Model = TypeVar("Model", DataModelBase)


class RefQueue(Component, Generic[Model]):
    """Queue with a lock.
    
    This object is often used for retrieving data same as LogQueue
    by DataLogger object. The object has syncronized data as LogQueue,
    but smaller size than its size.
    
    See Also
    --------
        pisat.core.logger.DataLogger : An operator of this object.
        pisat.core.logger.LogQueue : Main container of data log.
    """
    
    def __init__(self, 
                 maxlen: int = 100, 
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            maxlen : int, optional
                size of inner deque, by default 100.
            name : Optional[str], optional
                name of this component, by default None.
        """
        super().__init__(name)
        
        self._lock: Lock = Lock()
        self._que: Deque[Model] = deque(maxlen=maxlen)
    
    @property
    def islocked(self) -> bool:
        return self._lock.locked()
        
    def get(self) -> Deque[Model]:
        """Get deep copy of inner deque in the way of thread safe.

        Returns
        -------
            Deque[Dict[str, Logable]]
                copy of inner deque.
        """
        with self._lock:
            que = deepcopy(self._que)
        return que
    
    def append(self, x: Model):
        """Append data into inner deque.

        Parameters
        ----------
            x : Dict[str, Logable]
                data logged.
        """
        with self._lock:
            self._que.appendleft(x)
            