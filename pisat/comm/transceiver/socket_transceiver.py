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
from time import time, sleep
from typing import Deque, Dict, List, Optional, Tuple, Union
from threading import Thread

from pisat.config.type import TypeAddress
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
        self._Addr2Socket: Dict[TypeAddress, CommSocket] = {}
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
        
    @classmethod
    def encode(cls, data: str) -> bytes:
        return 
        
    def create_socket(self, 
                      address: TypeAddress, 
                      maxlen: Optional[int] = None, 
                      name: Optional[str] = None) -> CommSocket:
        """Create CommSocket object associated with the transceiver.

        Parameters
        ----------
            address : TypeAddress
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
    
    def close(self, address: TypeAddress) -> None:
        """Close a socket assosiated with given address.
        
        This method deletes a socket with the given address. After execution 
        of the method, the socket object will not be accessed.

        Parameters
        ----------
            address : TypeAddress
                Address of a socket with which a socket object is connected.
        """
        socket = self._Addr2Socket.pop(address)
        del socket
        
    def closes(self, socket: CommSocket) -> None:
        """Close given socket.
        
        This method deletes the given socket. After execution of the method, 
        the object will not be accessed.
        
        Parameters
        ----------
            socket : CommSocket
                Socket to be closed.
        """
        del self._Addr2Socket[socket.addr_yours]
        del socket
        
    def check_addr(self, address: TypeAddress) -> bool:
        """Check if the given address is valid or not.

        Parameters
        ----------
            address : TypeAddress
                Address to be judged.

        Returns
        -------
            bool
                Whether the given address is valid or not.
        """
        return self._transceiver.check_addr(address)
    
    def encode(self, data: str) -> bytes:
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
        return self._transceiver.encode(data)
    
    def decode(self, data: Union[bytes, bytearray]) -> str:
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
        return self._transceiver.decode(data)
    
    def recv_raw(self) -> Tuple[TypeAddress, bytes]:
        """Receive raw data from wrapped transceiver.

        Returns
        -------
            Tuple[TypeAddress, bytes]
                Address which data is from, and raw data.
        """
        return self._transceiver.recv_raw()
    
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
        return self._transceiver.send_raw(address, data)
    
    def listen(self, timeout: Union[float, int] = -1.) -> Optional[CommSocket]:
        """Make the object be a server and wait a connection.
        
        This method sets the SocketTransceiver object the server mode. 
        In the server mode, the method waits a connection from any clients 
        and blocks execution. Once a connection is detected, this method 
        makes a socket assosiated with the client and returns it.
        
        If parameter 'timeout' is set and the time is passed, this method 
        may returns None. Otherwise, this method will return a CommSocket 
        object.
        
        Parameters
        ----------
            timeout : Union[float, int], default -1.
                Timeout to quit execution.

        Returns
        -------
            Optional[CommSocket]
                A socket assosiated with a client.
        """
        if not isinstance(timeout, (float, int)):
            raise TypeError(
                "'timeout' must be float or int."
            )
        
        time_init = time()
        while True:
            raw = self.recv_raw()
            if len(raw) == 2:
                break
            
            if timeout < 0.:
                continue
            
            if time() - time_init > timeout:
                return None
        
        addr, data = raw
        socket = self.create_socket(addr)
        socket._recv_stream.add(data)
        
        return socket
    
    def get_socket(self, address: TypeAddress) -> CommSocket:
        """Retreive a socket with the given address.

        Parameters
        ----------
            address : TypeAddress
                Address to be searched.

        Returns
        -------
            CommSocket
                Socket object with the given address.

        Raises
        ------
            ValueError
                Raised if the given address is invalid.
        """
        sock = self._Addr2Socket.get(address)
        if sock is None:
            raise ValueError(
                "A socket with given 'address' does not exist."
            )
        return sock
    
    def list(self) -> List[TypeAddress]:
        """Lists addresses associated with sockets still alive.

        Returns
        -------
            List[TypeAddress]
                Addresses associated with sockets still alive.
        """
        return list(self._Addr2Socket.keys())
        
    def load(self, size: int = -1, ignore: bool = False) -> None:
        """Update the buffers of sockets associated with the transceiver.

        Parameters
        ----------
            size : int, optional
                Number of packets to be loaded, by default -1
        """
        count = 0
        while True:
            is_success = self._load_single_data(ignore=ignore)
            if not is_success:
                break
            
            count += 1
            if count >= size:
                break
            
    def _load_single_data(self, ignore: bool = False) -> bool:
        raw = self._transceiver.recv_raw()
        if len(raw) == 2:
            addr, data = raw
            socket = self._Addr2Socket.get(addr)
            
            if socket is not None:
                socket._recv_stream.add(data)
            else:
                if not ignore:
                    new_socket = self.create_socket(addr)
                    new_socket._recv_stream.add(data)
                    
            return True
        else:
            return False
                
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
        
        scheduled: Deque[Tuple[TypeAddress, bytes]] = deque()
        
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
           
    def _flush_scheduled(self, 
                         scheduled: Deque[Tuple[TypeAddress, bytes]], 
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
        
    def _retreive_send_data(self, socket: CommSocket) -> Deque[Tuple[TypeAddress, bytes]]:
        que = deque()
        while True:
            data = socket._send_stream.pop(self._transceiver.Packet.MAX.value)
            if len(data) > 0:
                que.append((socket.addr_yours, data))
            else:
                break
        return que
        