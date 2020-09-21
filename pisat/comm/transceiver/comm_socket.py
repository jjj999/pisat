
from typing import Optional, Union, Tuple, Any

from pisat.base.component import Component
from pisat.comm.transceiver.comm_stream import CommBytesStream


class CommSocket(Component):

    def __init__(self, 
                 recv_stream: CommBytesStream,
                 send_stream: CommBytesStream,
                 address_mine: Tuple[Any],
                 address_yours: Tuple[Any],
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._recv_stream: CommBytesStream = recv_stream
        self._send_stream: CommBytesStream = send_stream
        self._addr_mine: Tuple[Any] = address_mine
        self._addr_yours: Tuple[Any] = address_yours
        
    @property
    def addr_mine(self):
        return self._addr_mine
    
    @property
    def addr_yours(self):
        return self._addr_yours
    
    def recv(self, count: int) -> bytes:
        return self._recv_stream.pop(count)
    
    def send(self, data: Union[bytes, bytearray]) -> None:
        self._send_stream.add(data)
