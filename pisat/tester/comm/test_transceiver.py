
from collections import deque
from enum import Enum
from typing import Deque, Dict, Optional, Tuple, Union

from pisat.comm.transceiver import TransceiverBase


class TestTransceiver(TransceiverBase):
    """Transceiver for testing.
    """
    
    class Setting(Enum):
        BYTES_PACKET_MAX = 64
    
    shared_buf: Dict[Tuple, Deque[Tuple[Tuple, bytes]]] = {}
        
    def __init__(self,
                 addr: Tuple[int],
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            addr : Tuple[int]
                Address of the transceiver
            name : Optional[str], optional
                Name of the component, by default None
        """
        super().__init__(handler=None, address=addr, name=name)
        
        self.shared_buf[addr] = deque()
        
    @classmethod
    def check_addr(cls, address: Tuple[int]) -> bool:
        """Check if the given address is valid or not.

        Parameters
        ----------
            address : Tuple[Any]
                Address to be judged

        Returns
        -------
            bool
                Whether the given address is valid or not.
        """
        if len(address) == 1 and isinstance(address[0], int):
            return True
        else:
            return False
        
    @classmethod
    def encode(cls, data: str) -> bytes:
        """Encode str into bytes with certain encoding.

        Parameters
        ----------
            data : str
                Data to be encoded.

        Returns
        -------
            bytes
                Data encoded.
        """
        return data.encode()
    
    @classmethod
    def decode(cls, data: Union[bytes, bytearray]) -> str:
        return data.decode()
        
    def recv_raw(self) -> Tuple[Tuple[int], bytes]:
        """Receive raw data from the transceiver.

        Returns
        -------
            Tuple[Tuple[Any], bytes]
                Address which data is from, and raw data.
        """
        buf = self.shared_buf[self.addr]
        if not len(buf):
            return ()
        
        return buf.pop()
        
    def send_raw(self, addr: Tuple[int], data: Union[bytes, bytearray]) -> bool:
        """Send raw data to the transceiver which has the given address.

        Parameters
        ----------
            address : Tuple[Any]
                Address to which the data is to be send.
            data : Union[bytes, bytearray]
                Data to be send.
                
        Returns
        -------
            bool
                Whether the data is send certainly or not.
        """
        buf = self.shared_buf[addr]
        buf.appendleft((self.addr, data))
        return True
