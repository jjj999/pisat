#! python3

"""

pisat.comm.transceiver.comm_stream
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Simple streams for communication.

CommStreamBase class defines the interface of the stream.
All streams has a Lock object for multi-threading.

CommBytesStream class implements the CommStreamBase as 
the internal queue has bytes.

CommTextStream class implements the CommStreamBase as 
the internal queue has str.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.
"""

from typing import Iterable, Optional, Union
from collections import deque
from threading import Lock


class CommStreamBase:
    """Simple streams for communication.
    
    This class defines the interface of the stream. All streams 
    has a Lock object for multi-threading.
    """

    def __init__(self, 
                 initial: Optional[Iterable] = None,
                 maxlen: Optional[int] = None) -> None:
        """
        Parameters
        ----------
            initial : Optional[Iterable], optional
                Initial values of the stream, by default None
            maxlen : Optional[int], optional
                Size of the stream, by default None
        """
        
        self._que: deque = deque(maxlen=maxlen)
        self._lock: Lock = Lock()
        
        if initial is not None:
            self.add(initial)
    
    def add(self, data: Iterable) -> None:
        """Add data into the stream.

        Parameters
        ----------
            data : Iterable
                Data to be added.
        """
        pass
    
    def pop(self, count: int) -> Iterable:
        """Pop data from the stream.

        Parameters
        ----------
            count : int
                Counts of data to be pop.

        Returns
        -------
            Iterable
                Data to be pop.
        """
        pass
    
    def __len__(self):
        return len(self._que)
    

class CommBytesStream(CommStreamBase):
    """CommStreamBase as the internal queue has bytes.
    """
    
    def __init__(self,
                 initial: Optional[Union[bytes, bytearray]] = None,
                 maxlen: Optional[int] = None) -> None:
        """
        Parameters
        ----------
            initial : Optional[Union[bytes, bytearray]], optional
                Initial values of the stream, by default None
            maxlen : Optional[int], optional
                Size of the stream, by default None
        """
        super().__init__(initial=initial, maxlen=maxlen)
        
    def add(self, data: Union[bytes, bytearray]) -> None:
        """Add data into the stream.

        Parameters
        ----------
            data : Union[bytes, bytearray]
                Data to be added.
                
        Raises
        ------
            TypeError
                Raised if the given data is not bytes or bytearray.
        """
        with self._lock:
            if isinstance(data, (bytes, bytearray)):
                TypeError(
                    "'data' must be bytes or bytearray."
                )
                
            for d in data:
                self._que.appendleft(d)
            
    def pop(self, count: int) -> bytes:
        """Pop data from the stream.

        Parameters
        ----------
            count : int
                Counts of data to be pop.

        Returns
        -------
            bytes
                Data to be pop.
        """
        with self._lock:
            result = bytearray()
            for _ in range(count):
                if len(self._que) == 0:
                    break
                result.append(self._que.pop())
                
            return bytes(result)
    

class CommTextStream(CommStreamBase):
    """CommStreamBase as the internal queue has str.
    """
    
    def __init__(self,
                 initial: Optional[str] = None,
                 maxlen: Optional[int] = None) -> None:
        """
        Parameters
        ----------
            initial : Optional[str], optional
                Initial values of the stream, by default None
            maxlen : Optional[int], optional
                Size of the stream, by default None
        """
        super().__init__(initial=initial, maxlen=maxlen)
        
    def add(self, data: str) -> None:
        """Add data into the stream.

        Parameters
        ----------
            data : str
                Data to be added.
                
        Raises
        ------
            TypeError
                Raised if the given data is not str.
        """
        with self._lock:
            if isinstance(data, str):
                TypeError(
                    "'data' must be str."
                )
                
            for d in data:
                self._que.appendleft(d)
            
    def pop(self, count: int) -> str:
        """Pop data from the stream.

        Parameters
        ----------
            count : int
                Counts of data to be pop.

        Returns
        -------
            str
                Data to be pop.
        """
        with self._lock:
            result = []
            for _ in range(count):
                if len(self._que) == 0:
                    break
                result.append(self._que.pop())
                
            return "".join(result)
    