
from typing import Any, Optional, Tuple, Union
from enum import Enum

from pisat.handler.handler_base import HandlerBase
from pisat.base.component import Component


class TransceiverBase(Component):
    
    # TODO to be overrided
    class Packet(Enum):
        MAX = 0
    
    def __init__(self,
                 handler: Optional[HandlerBase] = None,
                 address: Optional[Tuple[Any]] = None,
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._handler: Optional[HandlerBase] = handler
        self._addr: Optional[Tuple[Any]] = address
        
    @property
    def addr(self):
        return self._addr
    
    # TODO to be overrided
    def check_addr(self, address: Tuple[Any]) -> bool:
        pass
    
    # TODO to be overrided
    def recv_raw(self) -> Tuple[Tuple[Any], bytes]:
        pass
    
    # TODO to be overrided
    def send_raw(self, address: Tuple[Any], data: Union[bytes, bytearray]) -> bool:
        pass
