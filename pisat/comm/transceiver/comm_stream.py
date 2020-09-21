

from typing import Iterable, Optional, Union
from collections import deque
from threading import Lock


class CommStreamBase:

    def __init__(self, 
                 initial: Optional[Iterable] = None,
                 maxlen: Optional[int] = None) -> None:
        
        self._que: deque = deque(maxlen=maxlen)
        self._lock: Lock = Lock()
        
        if initial is not None:
            self.add(initial)
    
    def add(self, data: Iterable) -> None:
        pass
    
    def pop(self, count: int) -> Iterable:
        pass
    
    def __len__(self):
        return len(self._que)
    

class CommBytesStream(CommStreamBase):
    
    def __init__(self,
                 initial: Optional[Union[bytes, bytearray]] = None,
                 maxlen: Optional[int] = None) -> None:
        super().__init__(initial=initial, maxlen=maxlen)
        
    def add(self, data: Union[bytes, bytearray]) -> None:
        with self._lock:
            if isinstance(data, (bytes, bytearray)):
                TypeError(
                    "'data' must be bytes or bytearray."
                )
                
            for d in data:
                self._que.appendleft(d)
            
    def pop(self, count: int) -> bytes:
        with self._lock:
            result = bytearray()
            for _ in range(count):
                if len(self._que) == 0:
                    break
                result.append(self._que.pop())
                
            return bytes(result)
    

class CommTextStream(CommStreamBase):
    
    def __init__(self,
                 initial: Optional[str] = None,
                 maxlen: Optional[int] = None) -> None:
        super().__init__(initial=initial, maxlen=maxlen)
        
    def add(self, data: str) -> None:
        with self._lock:
            if isinstance(data, str):
                TypeError(
                    "'data' must be str."
                )
                
            for d in data:
                self._que.appendleft(d)
            
    def pop(self, count: int) -> str:
        with self._lock:
            result = []
            for _ in range(count):
                if len(self._que) == 0:
                    break
                result.append(self._que.pop())
                
            return "".join(result)
    