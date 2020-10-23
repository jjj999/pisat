#! python3

"""

pisat.comm.transceiver.socket_transceiver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The wrapper of transceivers to generate sockets 
associated with the transceivers.
This class wraps a given transceiver and makes 
users get sockets combined with the transceiver, 
which is like the 'socket' of python.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.comm.transceiver.CommSocket
"""

from collections import deque
from enum import Enum
from time import sleep
from typing import Any, Deque, Dict, Optional, Tuple, Union
from threading import Thread, Event

from pisat.comm.transceiver.transceiver_base import TransceiverBase
from pisat.comm.transceiver.comm_stream import CommBytesStream
from pisat.comm.transceiver.comm_socket import CommSocket


class SocketTransceiver(TransceiverBase):
    """The wrapper of transceivers to generate sockets associated 
    with the transceivers.
    
    This class wraps a given transceiver and makes 
    users get sockets combined with the transceiver, 
    which is like the 'socket' of python.
    
    See Also
    --------
        pisat.comm.transceiver.CommSocket : 
            SocketTransceiver makes objects of the class.
    """
    
    class Period(Enum):
        MIN = 0.
        
        @classmethod
        def is_valid(cls, period: float) -> bool:
            if period >= cls.MIN.value:
                return True
            else:
                return False
    
    def __init__(self, 
                 transceiver: TransceiverBase,
                 period: float = 0.,
                 certain: bool = True,
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            transceiver : TransceiverBase
                Transceiver to be wrapped.
            period : float, optional
                Period for sending, by default 0.
            certain : bool, optional
                If the transceiver sends data certainly, by default True
            name : Optional[str], optional
                Name of the component, by default None

        Raises
        ------
            TypeError
                Raised if 'transceiver' is not TransceiverBase.
            TypeError
                Raised if 'certain' is not bool.
        """
        super().__init__(handler=transceiver._handler,
                         address=transceiver._addr,
                         name=name)
        
        if not isinstance(transceiver, TransceiverBase):
            raise TypeError(
                "'transceiver' must be TransceiverBase."
            )
            
        if not isinstance(certain, bool):
            raise TypeError(
                "'certain' must be bool."
            )
        
        self._transceiver: TransceiverBase = transceiver
        self._Addr2Socket: Dict[Tuple[Any], CommSocket] = {}
        self._event_recv: Event = Event()
        self._event_send: Event = Event()
        self._period = period
        self._certain: bool = certain
        
    @property
    def addr_mine(self):
        return self._transceiver.addr
    
    @property
    def period(self):
        return self._period
    
    @period.setter
    def period(self, val):
        if not self.Period.is_valid(val):
            raise ValueError(
                "'period' must be no less than {}."
                .format(self.Period.MIN.value)
            )
        self._period = val
    
    @property
    def certain(self):
        return self._certain
    
    def certain_on(self) -> None:
        """Make the transceiver send data certainly.
        """
        self._certain = True
        
    def certain_off(self) -> None:
        """Ignore whether the transceiver send data certainly.
        """
        self._certain = False
        
    def create_socket(self, 
                      address: Tuple[Any], 
                      maxlen: Optional[int] = None, 
                      name: Optional[str] = None) -> CommSocket:
        """Create CommSocket object associated with the transceiver.

        Parameters
        ----------
            address : Tuple[Any]
                Address of another socket to send data.
            maxlen : Optional[int], optional
                Size of bytes of the internal buffer, by default None
            name : Optional[str], optional
                Name of the socket as a component, by default None

        Returns
        -------
            CommSocket
                Socket associated with the transceiver.

        Raises
        ------
            ValueError
                Raised if the address is invalid.
        """
        
        if not self._transceiver.check_addr(address):
            raise ValueError(
                "Given 'address' is invalid."
            )
        
        recv_stream = CommBytesStream(maxlen=maxlen)
        send_stream = CommBytesStream()
        socket = CommSocket(self, recv_stream, send_stream, self.addr_mine, address, name=name)
        self._Addr2Socket[address] = socket
        
        return socket
        
    def check_addr(self, address: Tuple[Any]) -> bool:
        """Check if the given address is valid or not.

        Parameters
        ----------
            address : Tuple[Any]
                Address to be judged.

        Returns
        -------
            bool
                Whether the given address is valid or not.
        """
        return self._transceiver.check_addr(address)
    
    def recv_raw(self) -> Tuple[Tuple[Any], bytes]:
        """Receive raw data from wrapped transceiver.

        Returns
        -------
            Tuple[Tuple[Any], bytes]
                Address which data is from, and raw data.
        """
        return self._transceiver.recv_raw()
    
    def send_raw(self, address: Tuple[Any], data: Union[bytes, bytearray]) -> bool:
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
        return self._transceiver.send_raw(address, data)
        
    def load(self, size: int = -1) -> None:
        """Update the buffers of sockets associated with the transceiver.

        Parameters
        ----------
            size : int, optional
                Number of packets to be loaded, by default -1
        """
        if size < 0:
            while True:
                if not self._load_single_data():
                    break
        else:
            for _ in range(size):
                if not self._load_single_data():
                    break
                
    def flush(self, 
              socket: Optional[CommSocket] = None,
              blocking: bool = True, 
              period: Optional[float] = None, 
              certain: Optional[bool] = None) -> None:
        """Flush internal sending-buffer of registered sockets.

        Parameters
        ----------
            socket : Optional[CommSocket], optional
                Socket whose buffer to be flushed, by default None
            blocking : bool, optional
                If blocks and flushes, by default True
            period : Optional[float], optional
                Period for sending, by default None
            certain : Optional[bool], optional
                If the transceiver sends data certainly, by default None
                
        Raises
        ------
            ValueError
                Raised if the given socket is invalid.
                
        Notes
        -----
            If the 'socket' is None, then the method flushes buffers of 
            all sockets, while only the buffer of the socket is to be 
            flushed when the 'socket' is given.
            
            If the 'blocking' is False, then this method executes 
            task of sending in another method.
            
            If period is None, then the method uses the value of 
            SocketTransceiver.period property as the parameter of period.
            
            If certain is None, then the method uses the value of 
            SocketTransceiver.certain property as the parameter of certain.
        """
        period_used = period if period is not None else self.period
        certain_used = certain if certain is not None else self.certain
        
        scheduled: Deque[Tuple[Tuple[Any], bytes]] = deque()
        
        if socket is None:
            for sock in self._Addr2Socket.values():
                que = self._retreive_send_data(sock)
                scheduled.extendleft(que)
        else:
            sock = self._Addr2Socket.get(socket.addr_yours)
            if sock is None:
                raise ValueError(
                    "Given 'socket' is invalid."
                )
            que = self._retreive_send_data(sock)
            scheduled.extendleft(que)
                
        if blocking:
            self._flush_scheduled(scheduled, period=period_used, certain=certain_used)
        else:
            thread = Thread(target=self._flush_scheduled, 
                            args=(scheduled, ), 
                            kwargs={"period": period_used, "certain": certain_used})
            thread.start()
        
    def _load_single_data(self) -> bool:
        raw = self._transceiver.recv_raw()
        if len(raw) == 2:
            addr, data = raw
            socket = self._Addr2Socket.get(addr)
            
            if socket is not None:
                socket._recv_stream.add(data)
            return True
        else:
            return False
           
    def _flush_scheduled(self, 
                         scheduled: Deque[Tuple[Tuple[Any], bytes]], 
                         period: float = 0.,
                         certain: bool = True) -> None:
        try:
            while True:
                if not len(scheduled):
                    break
                
                addr, data = scheduled.pop()
                
                def send_single_packet():
                    flag = self._transceiver.send_raw(addr, data)
                    if period > 0.:
                        sleep(period)
                    if certain and not flag:
                        send_single_packet()
                        
                send_single_packet()
        except:
            pass
        
    def _retreive_send_data(self, socket: CommSocket) -> Deque[Tuple[Tuple[Any], bytes]]:
        que = deque()
        while True:
            data = socket._send_stream.pop(self._transceiver.Packet.MAX.value)
            if len(data) > 0:
                que.append((socket.addr_yours, data))
            else:
                break
        return que
        