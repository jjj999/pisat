#! python3

"""

pisat.comm.transceiver.transceiver_base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The base class of transceivers.
This class defines the interface of transceivers 
which can exchange flexible data with each other.

"""

from typing import Optional, Tuple, Union
from enum import Enum

from pisat.handler.handler_base import HandlerBase
from pisat.base.component import Component


TypeAddress = Tuple[Union[int, str]]


class TransceiverBase(Component):
    """The base class of transceivers.
    
    This class defines interfaces of transceivers 
    which can exchange flexible data with each other.
    """
    
    # TODO to be overrided
    class Packet(Enum):
        MAX = 0
    
    def __init__(self,
                 handler: Optional[HandlerBase] = None,
                 address: Optional[TypeAddress] = None,
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            handler : Optional[HandlerBase], optional
                Handler for handling communication, by default None
            address : Optional[TypeAddress], optional
                Logical address of the device, by default None
            name : Optional[str], optional
                Name of this component, by default None
                
        Notes
        -----
            The 'address' is defined freely by developer who 
            makes a transceiver. The address is kind of logical 
            identifier of the device itself or sockets. 
        """
        super().__init__(name=name)
        
        self._handler: Optional[HandlerBase] = handler
        self._addr: Optional[TypeAddress] = address
        
    @property
    def addr(self):
        return self._addr
    
    # TODO to be overrided
    @classmethod
    def check_addr(cls, address: TypeAddress) -> bool:
        """Check if the given address is valid or not.

        Parameters
        ----------
            address : TypeAddress
                Address to be judged

        Returns
        -------
            bool
                Whether the given address is valid or not.
        """
        pass
    
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
        pass
    
    @classmethod
    def decode(cls, data: Union[bytes, bytearray]) -> str:
        """Decode bytes into str with certain encoding.

        Parameters
        ----------
            data : Union[bytes, bytearray]
                Data to be decoded.

        Returns
        -------
            str
                Data decoded.
        """
        pass
    
    # TODO to be overrided
    def recv_raw(self) -> Tuple[TypeAddress, bytes]:
        """Receive raw data from the transceiver.

        Returns
        -------
            Tuple[TypeAddress, bytes]
                Address which data is from, and raw data.
        """
        pass
    
    # TODO to be overrided
    def send_raw(self, address: TypeAddress, data: Union[bytes, bytearray]) -> bool:
        """Send raw data to the transceiver which has the given address.

        Parameters
        ----------
            address : TypeAddress
                Address to which the data is to be send.
            data : Union[bytes, bytearray]
                Data to be send.
                
        Returns
        -------
            bool
                Whether the data is send certainly or not.
        """
        pass
