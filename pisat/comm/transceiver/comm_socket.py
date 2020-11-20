#! python3

"""

pisat.comm.transceiver.comm_socket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Socket to communicate pear to pear via transceiver.
This class represents object like the socket of python, 
whose has a single connection. 

This class is not instanciated by users, but by a
SocketTransceiver object.

"""

from typing import Optional, Union

from pisat.base.component import Component
from pisat.comm.transceiver.comm_stream import CommBytesStream
from pisat.comm.transceiver.transceiver_base import TypeAddress


class CommSocket(Component):
    """Socket to communicate pear to pear via transceiver.
    
    This class represents object like the socket of python, 
    whose has a single connection. 
    
    This class is not instanciated by users, but by a
    SocketTransceiver object.
    """

    # NOTE this transceiver must be SocketTransceiver
    def __init__(self, 
                 transceiver,
                 recv_stream: CommBytesStream,
                 send_stream: CommBytesStream,
                 address_mine: TypeAddress,
                 address_yours: TypeAddress,
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            transceiver : SocketTransceiver
                SocketTransceiver which generates this object.
            recv_stream : CommBytesStream
                Internal stream for receiveing data.
            send_stream : CommBytesStream
                Internal stream for sending data.
            address_mine : TypeAddress
                Logical address of this socket.
            address_yours : TypeAddress
                Logical address of the other socket to communicate.
            name : Optional[str], optional
                Name of this component, by default None
        """
        super().__init__(name=name)

        self._transceiver = transceiver
        self._recv_stream: CommBytesStream = recv_stream
        self._send_stream: CommBytesStream = send_stream
        self._addr_mine: TypeAddress = address_mine
        self._addr_yours: TypeAddress = address_yours
        
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
    
    @property
    def period(self):
        return self._transceiver.period
        
    @property
    def certain(self):
        return self._transceiver.certain
    
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
    
    def close(self) -> None:
        """Close this socket.
        
        This method deletes the object. After execution of the method, 
        the object will not be accessed.
        """
        self._transceiver.closes(self)
    
    def recv(self, count: int, load: bool = True, ignore: bool = False) -> bytes:
        """Receive data from the other socket.

        Parameters
        ----------
            count : int
                Size of bytes to be received.
            load : bool, optional
                If loads internal buffer for receiving, by default True

        Returns
        -------
            bytes
                Data which is received successfully.
            
        Notes
        -----
            Returned data may have smaller size than specified because 
            data is not be retreived further more.
        """
        if load:
            self._transceiver.load(ignore=ignore)
        return self._recv_stream.pop(count)
    
    def send_later(self, data: Union[bytes, bytearray]) -> None:
        """Add data into the internal buffer as reserved data.
        
        This method add data into the internal buffer but the 
        data is not sended until the buffer is flushed. If you 
        want to send after this method, then you can use the 
        'flush' method to flush the internal buffer.

        Parameters
        ----------
            data : Union[bytes, bytearray]
                Data to be send in the future.
                
        Notes
        -----
            If you want to send earlier, consider using the 'send' 
            method.
        """
        self._send_stream.add(data)
        
    def flush(self, 
              blocking: bool = True, 
              period: Optional[float] = None,
              certain: Optional[bool] = None) -> None:
        """Flush internal sending-buffer of the socket.

        Parameters
        ----------
            blocking : bool, optional
                If blocks and flushes, by default True
            period : Optional[float], optional
                Period for sending, by default None
            certain : Optional[bool], optional
                If the transceiver sends data certainly, by default None
                
        Notes
        -----
            If period is None, then the method uses the value of 
            CommSocket.period property as the parameter of period.
            
            If the 'blocking' is False, then this method executes 
            the task of sending in another thread.
            
            If certain is None, then the method uses the value of 
            CommSocket.certain property as the parameter of certain.
        """
        self._transceiver.flush(socket=self, blocking=blocking, period=period, certain=certain)
    
    def send(self, 
             data: Union[bytes, bytearray],
             blocking: bool = True,
             period: Optional[float] = None,
             certain: Optional[bool] = None) -> None:
        """Send data to the other socket.
        
        Calling this method is same as calling the 'send_later' method 
        and the 'flush' method in a row.

        Parameters
        ----------
            data : Union[bytes, bytearray]
                Data to be send.
            blocking : bool, optional
                If blocks and flushes, by default True
            period : Optional[float], optional
                Period for sending, by default None
            certain : Optional[bool], optional
                If the transceiver sends data certainly, by default None
                
        Notes
        -----
            If period is None, then the method uses the value of 
            CommSocket.period property as the parameter of period.
            
            If the 'blocking' is False, then this method executes 
            the task of sending in another thread.
            
            If certain is None, then the method uses the value of 
            CommSocket.certain property as the parameter of certain.
        """
        self._send_stream.add(data)
        self.flush(blocking=blocking, period=period, certain=certain)
