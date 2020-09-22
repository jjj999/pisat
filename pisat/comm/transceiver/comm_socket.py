
from typing import Optional, Union, Tuple, Any

from pisat.base.component import Component
from pisat.comm.transceiver.comm_stream import CommBytesStream


class CommSocket(Component):

    # NOTE this transceiver must be SocketTransceiver
    def __init__(self, 
                 transceiver,
                 recv_stream: CommBytesStream,
                 send_stream: CommBytesStream,
                 address_mine: Tuple[Any],
                 address_yours: Tuple[Any],
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)

        self._transceiver = transceiver
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
    
    @property
    def counts_recv(self):
        return len(self._recv_stream)
    
    @property
    def counts_send(self):
        return len(self._send_stream)
    
    def recv(self, count: int, load: bool = True) -> bytes:
        if load:
            self._transceiver.load()
        return self._recv_stream.pop(count)
    
    def send(self, 
             data: Union[bytes, bytearray],
             blocking: Union[bool, None] = True,
             period: Optional[float] = None,
             certain: Optional[bool] = None) -> None:
        self._send_stream.add(data)
        if blocking is not None:
            self._transceiver.flush(socket=self, blocking=blocking, period=period, certain=certain)
