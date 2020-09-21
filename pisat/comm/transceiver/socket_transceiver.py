
from collections import deque
from time import sleep, time
from typing import Any, Dict, Optional, Tuple, Union
from threading import Thread, Event

from pisat.comm.transceiver.transceiver_base import TransceiverBase
from pisat.comm.transceiver.comm_stream import CommBytesStream
from pisat.comm.transceiver.comm_socket import CommSocket


class SocketTransceiver(TransceiverBase):
    
    def __init__(self, 
                 transceiver: TransceiverBase,
                 name: Optional[str] = None) -> None:
        super().__init__(handler=transceiver._handler,
                         address=transceiver._addr,
                         name=name)
        
        self._transceiver: TransceiverBase = transceiver
        
        self._Addr2Recv: Dict[Tuple[Any], CommBytesStream] = {}
        self._Addr2Send: Dict[Tuple[Any], CommBytesStream] = {}
        self._Socket2Recv: Dict[CommSocket, CommBytesStream] = {}
        self._Socket2Send: Dict[CommSocket, CommBytesStream] = {}
        
        self._event_recv: Event = Event()
        self._event_send: Event = Event()
        
    def create_socket(self, 
                      address: Tuple[Any], 
                      maxlen: Optional[int] = None, 
                      name: Optional[str] = None) -> CommSocket:
        
        if not self._transceiver.check_addr(address):
            raise ValueError(
                "Given 'address' is invalid."
            )
        
        recv_stream = CommBytesStream(maxlen=maxlen)
        send_stream = CommBytesStream()
        self._Addr2Recv[address] = recv_stream
        self._Addr2Send[address] = send_stream
        
        socket = CommSocket(recv_stream, send_stream, self._transceiver.addr, address, name=name)
        self._Socket2Recv[socket] = recv_stream
        self._Socket2Send[socket] = send_stream
        
        return socket
        
    def check_addr(self, address: Tuple[Any]) -> bool:
        return self._transceiver.check_addr(address)
    
    def recv_raw(self) -> Tuple[Tuple[Any], bytes]:
        return self._transceiver.recv_raw()
    
    def send_raw(self, address: Tuple[Any], data: Union[bytes, bytearray]) -> None:
        self._transceiver.send_raw(address, data)
        
    def recv_from(self, socket: CommSocket, count: int) -> bytes:
        recv_stream = self._Socket2Recv.get(socket)
        if recv_stream is None:
            ValueError(
                "'socket' is not included in this transceiver."
            )
            
        return recv_stream.pop(count)
    
    def send_to(self, socket: CommSocket, data: Union[bytes, bytearray]) -> None:
        send_stream = self._Socket2Send.get(socket)
        if send_stream is None:
            ValueError(
                "'socket' is not included in this transceiver."
            )
            
        send_stream.add(data)
        
    def observe(self) -> None:
        
        def observe_recv():
            while not self._event_recv.is_set():
                try:
                    raw = self._transceiver.recv_raw()
                    if len(raw) == 2:
                        addr, data = raw
                        stream = self._Addr2Recv.get(addr)
                        if stream is not None:
                            stream.add(data)
                except:
                    pass
            self._event_recv.clear()
        
        def observe_send():
            while not self._event_send.is_set():
                try:
                    for addr, stream in self._Addr2Send.items():
                        if len(stream) > 0:
                            data = stream.pop(self._transceiver.Packet.MAX.value)
                            self._transceiver.send_raw(addr, data)
                except:
                    pass
            self._event_send.clear()
        
        th_recv = Thread(target=observe_recv)
        th_send = Thread(target=observe_send)
        
        th_recv.start()
        th_send.start()
        
    def stop_observe(self) -> None:
        self._event_recv.set()
        self._event_send.set()
        