
from collections import deque
from enum import Enum
from typing import Deque, Dict, Optional, Tuple, Union

from pisat.comm.transceiver import TransceiverBase


class TestTransceiver(TransceiverBase):
    
    class Setting(Enum):
        BYTES_PACKET_MAX = 64
    
    shared_buf: Dict[Tuple, Deque[Tuple[Tuple, bytes]]] = {}
        
    def __init__(self,
                 addr: Tuple[int],
                 name: Optional[str] = None) -> None:
        super().__init__(handler=None, address=addr, name=name)
        
        self.shared_buf[addr] = deque()
        
    @classmethod
    def check_addr(cls, address: Tuple[int]) -> bool:
        if len(address) == 1 and isinstance(address[0], int):
            return True
        else:
            return False
        
    def recv_raw(self) -> Tuple[Tuple[int], bytes]:
        buf = self.shared_buf[self.addr]
        if not len(buf):
            return ()
        
        return buf.pop()
        
    def send_raw(self, addr: Tuple[int], data: Union[bytes, bytearray]) -> None:
        buf = self.shared_buf[addr]
        buf.appendleft((self.addr, data))