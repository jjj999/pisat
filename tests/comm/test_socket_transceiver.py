
from collections import deque
from enum import Enum
from threading import Thread
from time import sleep
from typing import Deque, Dict, Optional, Tuple, Union
import unittest

from pisat.comm.transceiver import TransceiverBase
from pisat.comm.transceiver import SocketTransceiver
from pisat.comm.transceiver import CommSocket, CommBytesStream


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


class TestSocketTransceiver(unittest.TestCase):
    
    def setUp(self) -> None:
        
        self.addr_0 = (0,)
        self.addr_1 = (1,)
        self.addr_2 = (2,)
        
        self.period = 0.1
        
        self.transceiver_0 = TestTransceiver(self.addr_0)
        self.transceiver_1 = TestTransceiver(self.addr_1)
        self.transceiver_2 = TestTransceiver(self.addr_2)
        
        self.sock_transceiver_0 = SocketTransceiver(self.transceiver_0, 
                                                    period=self.period, 
                                                    certain=True)
        self.sock_transceiver_1 = SocketTransceiver(self.transceiver_1, 
                                                    period=self.period, 
                                                    certain=True)
        self.sock_transceiver_2 = SocketTransceiver(self.transceiver_2, 
                                                    period=self.period, 
                                                    certain=True)

    def test_period_check(self):
        self.assertEqual(self.sock_transceiver_0.period, self.period)
    
    def test_listen(self):
        data_send = b"Hello World"
        
        thread = Thread(target=self.exec_client, args=(data_send,))
        thread.start()
        
        sock = self.sock_transceiver_0.listen()
        self.assertEqual(sock.addr_mine, self.addr_0)
        self.assertEqual(sock.addr_yours, self.addr_1)
        
        data_recv = sock.recv(100)
        self.assertEqual(data_recv, data_send)
        
    def exec_client(self, data: bytes):
        sleep(5)
        self.transceiver_1.send_raw(self.addr_0, data)


if __name__ == "__main__":
    unittest.main()
        