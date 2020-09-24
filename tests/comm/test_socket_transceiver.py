
from collections import deque
from typing import Deque, Optional, Tuple, Union
from enum import Enum
import random
from threading import Thread
from time import sleep

from pisat.comm.transceiver import TransceiverBase
from pisat.comm.transceiver import SocketTransceiver
from pisat.comm.transceiver import CommSocket


class TestTransceiver(TransceiverBase):
    
    class Setting(Enum):
        BYTES_PACKET_MAX = 64
        
    DATA = b"abcdefghijklmn"
    ADDRESS = [1, 2, 3, 4, 5]
        
    def __init__(self,
                 address: Tuple[int],
                 name: Optional[str] = None) -> None:
        super().__init__(handler=None, address=address, name=name)
        
        self._buf: Deque[bytes] = deque()
        self._buf_send: Deque[bytes] = deque()
        
    def update_data(self):
        def update():
            time = 0
            while True:
                self._buf.appendleft(self.DATA)
                sleep(1)
                time += 1
                
                if time > 10:
                    break
                
            print("end update_data")
            
        thread = Thread(target=update)
        thread.start()
        
    def recv_raw(self) -> Tuple[Tuple[int], bytes]:
        if len(self._buf) > 0:
            addr = 1
            # addr = random.choice(self.ADDRESS)
            data = self._buf.pop()
            return (addr, ), data
        else:
            return ()
        
    def send_raw(self, address: Tuple[int], data: Union[bytes, bytearray]) -> None:
        address_str = str(address[0])
        self._buf_send.appendleft(address_str.encode() + bytes(data))
        
        
def main_1():
        
    test_transceiver = TestTransceiver((0,))
    sock_transceiver = SocketTransceiver(test_transceiver)

    socket_1 = sock_transceiver.create_socket((1, ), name="socket_1")
    socket_2 = sock_transceiver.create_socket((2, ), name="socket_2")

    test_transceiver.update_data()
    sock_transceiver.observe()
    
    time = 0
    while True:
        socket_1.send(b'hello' * 20)
        sleep(0.5)
        time += 0.5
        print(socket_1.recv(10))
        
        if time > 11:
            break
        
    
    sock_transceiver.stop_observe()
    print(test_transceiver._buf_send)
    
    
def main_2():
    
    test_transceiver = TestTransceiver((0,))
    sock_transceiver = SocketTransceiver(test_transceiver)

    socket_1 = sock_transceiver.create_socket((1, ), name="socket_1")
    socket_2 = sock_transceiver.create_socket((2, ), name="socket_2")

    sock_transceiver.observe()
    
    print("go")
    socket_1.send(b"hello world " * 10)
    socket_2.send(b"bye world " * 10)
    sleep(0.01)
    print(test_transceiver._buf_send)
    
    for d in test_transceiver._buf_send:
        print(len(d))
    
    sock_transceiver.stop_observe()
        
if __name__ == "__main__":
    main_2()
        