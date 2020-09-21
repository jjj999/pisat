
from collections import deque
from enum import Enum, auto
import codecs
from time import time
from pisat.handler.pyserial_serial_handler import PyserialSerialHandler
from typing import Deque, List, Optional, Set, Tuple, Any, Union

from pisat.comm.transceiver.transceiver_base import TransceiverBase
from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.util.cached_property import cached_property


class Im920(TransceiverBase):
    
    class DataType(Enum):
        TRANSMIT = auto()
        CONFIG = auto()
        EVIDENCE = ord(b":")

    class Packet(Enum):
        
        MAX = 64
        
        TERMINATOR = "\r\n".encode("ascii")
        LEN_TERMINATOR = 2
        
        ENCODING_BASE = "ascii"
        ENCODING_TRANSMIT = "hex_codec"
        
        INDEX_LAST_ADDR = 10
        INDEX_HEAD_TRANSIMIT = 11
        
        SEPARATOR_ADDR = ","
        SIZE_ADDR = 3
        
        LEN_REC_ID = 4
        FORMAT_REC_ID = "04X"

    class Baudrate(Enum):
        RATE_1200 = "0"
        RATE_2400 = "1"
        RATE_4800 = "2"
        RATE_9600 = "3"
        RATE_19200 = "4"
        RATE_38400 = "5"
        RATE_57600 = "6"
        RATE_115200 = "7"
        RATE_230400 = "8"
        RATE_460800 = "9"
        
    class Node(Enum):
        MAX = 255
        MIN = 0
        
        @classmethod
        def is_valid(cls, node: int) -> bool:
            if cls.MIN.value <= node <= cls.MAX.value:
                return True
            else:
                return False
            
        @classmethod
        def is_valid_hex(cls, node: str) -> bool:
            return cls.is_valid(int(node, 16))

    class Command(Enum):

        ENABLE_WRITE_PARAM = "ENWR"             # (,)
        DISABLE_WRITE_PARAM = "DSWR"            # (,)

        READ_UNIQUE_ID = "RDID"                 # (,)

        SET_NODE_NUM = "STNN"                   # (,)
        READ_NODE_NUM = "RDNN"                  # (,)

        SET_COMM_CHANNEL = "STCH"               # (,)
        READ_COMM_CHANNEL = "RDCH"              # (,)

        ENABLE_CHAR_IO = "ECIO"                 # (1.26,)
        DISABLE_CHAR_IO = "DCIO"                # (1.26,), DEFAULT

        TRANSMIT_DATA_FIXED = "TXDT"            # (,)
        TRANSMIT_DATA_VARIABLE = "TXDA"         # (,)

        READ_RSSI_VALUE = "RDRS"                # (,)

        SET_TRANSMIT_POW = "STPO"               # (,)
        READ_TRANSMIT_POW = "RDPO"              # (,)

        READ_PRODUCT_VERSION = "RDVR"           # (,)

        SET_BAUD_RATE = "SBRT"                  # (1.26,)

        DISABLE_READ_DATA = "DSRX"              # (1.11, 1.03)
        ENABLE_READ_DATA = "ENRX"               # (1.11, 1.03), DEFAULT

        SET_SLEEP_TIME = "SSTM"                 # (1.13, 1.03)
        READ_SLEEP_TIME = "RSTM"                # (1.13, 1.03)

        SET_INTERMITTENT_TIME = "SWTM"          # (1.13, 1.03)
        READ_INTERMITTENT_TIME = "RWTM"         # (1.13, 1.03)

        READ_ALL_PARAMS = "RPRM"                # (1.24,)

        REBOOT = "SRST"                         # (,)
        INITIALIZE = "PCLR"                     # (,)

        SET_RECEIVE_ID = "SRID"                 # ALL
        READ_RECEIVE_ID = "RRID"                # ALL
        ERASE_RECIEVE_ID = "ERID"               # ALL

        SET_COMM_SPEED = "STRT"                 # ALL
        READ_COMM_SPEED = "RDRT"                # ALL

        ENABLE_ANSWER_BACK = "EABK"             # 1.24
        DISABLE_ANSWER_BACK = "DABK"            # 1.24

        ENABLE_COMM_PORT = "ERPT"               # 1.29
        DISABLE_COMM_PORT = "DRPT"              # 1.29

    def __init__(self,
                 handler: PyserialSerialHandler,
                 name: Optional[str] = None) -> None:
        if not isinstance(handler, PyserialSerialHandler):
            raise TypeError(
                "'handler' must have the interfaces of PyserialSerialHandler."
            )
        
        super().__init__(handler=handler, address=None, name=name)
        
        self._handler: PyserialSerialHandler = handler
        self._buf: Deque[Tuple[Tuple[str], bytes]] = deque()
        self._rec_id: Set[str] = set()
        
        self._update_rec_id()

    @classmethod
    def check_addr(cls, address: Tuple[str]) -> bool:
        if len(address) == cls.Packet.SIZE_ADDR.value:
            for val in address:
                if not isinstance(val, str):
                    return False
            return True
        else:
            return False
        
    @property
    def buf(self):
        self._update_buf()
        return self._buf

    def recv_raw(self) -> Tuple[Tuple[str], bytes]:
        self._update_buf()
        if not len(self._buf):
            return ()
        return self._buf.pop()

    def send_raw(self, address: Tuple[str], data: Union[bytes, bytearray]) -> None:
        self._send_formatted(self.Command.TRANSMIT_DATA_VARIABLE.value, data)
    
    @classmethod
    def encode(cls, data: str) -> bytes:
        data_ascii = data.encode(cls.Packet.ENCODING_BASE.value)
        return codecs.encode(data_ascii, cls.Packet.ENCODING_TRANSMIT.value)
    
    @classmethod
    def decode(cls, data: Union[bytes, bytearray]) -> str:
        data_ascii = codecs.decode(bytes(data), cls.Packet.ENCODING_TRANSMIT.value)
        return data_ascii.decode()
    
    @classmethod
    def decode_addr(cls, data: Union[bytes, bytearray]) -> Tuple[str]:
        return tuple(data.decode().split(cls.Packet.SEPARATOR_ADDR.value))
    
    def _recv_separate_type(self) -> Tuple[Enum, bytes]:
        # remove terminator
        raw = self._handler.readline(end=self.Packet.TERMINATOR.value)
        
        if self.DataType.EVIDENCE.value in raw:
            return (self.DataType.EVIDENCE, raw)
        else:
            return (self.DataType.CONFIG, raw)
        
    def _send_formatted(self, command: str, data: bytes = b'') -> None:
        formatted = bytearray()
        formatted.extend(command.encode(self.Packet.ENCODING_BASE.value))
        formatted.extend(data)
        formatted.extend(self.Packet.TERMINATOR.value)

        self._handler.write(formatted)
        self._handler.flush()
        
    def _update_buf(self) -> None:
        while self._handler.counts_readable:
            dtype, data = self._recv_separate_type()
            if dtype == self.DataType.CONFIG:
                continue
            
            addr, transmit = data[:self.Packet.INDEX_LAST_ADDR.value], data[self.Packet.INDEX_HEAD_TRANSIMIT.value:]
            self._buf.appendleft((self.decode_addr(addr), transmit))
    
    def _get_params(self, command: str) -> str:
        self._update_buf()
        self._send_formatted(command)
        
        def get_result() -> bytes:
            while not self._handler.counts_readable:
                pass
            
            dtype, data = self._recv_separate_type()
            if dtype == self.DataType.CONFIG:
                return data
            else:
                addr, transmit = data[:self.Packet.INDEX_LAST_ADDR.value], data[self.Packet.INDEX_HEAD_TRANSIMIT.value:]
                self._buf.appendleft((self.decode_addr(addr), self.decode(transmit)))
                get_result()
                
        return get_result()
    
    def _set_params(self, command: str, value: bytes = b''):
        self._send_formatted(self.Command.ENABLE_WRITE_PARAM.value)
        self._send_formatted(command, value)
        self._send_formatted(self.Command.DISABLE_WRITE_PARAM.value)
        
    def _update_rec_id(self):
        self._update_buf()
        self._send_formatted(self.Command.READ_RECEIVE_ID.value)
        
        def parse_result():
            while not self._handler.counts_readable:
                pass
            dtype, data = self._recv_separate_type()
            if dtype == self.DataType.CONFIG:
                if len(data) == self.Packet.LEN_REC_ID.value:
                    self._rec_id.add(data)
                    parse_result()
                else:
                    pass
            else:
                addr, transmit = data[:self.Packet.INDEX_LAST_ADDR.value], data[self.Packet.INDEX_HEAD_TRANSIMIT.value:]
                self._buf.appendleft((self.decode_addr(addr), self.decode(transmit)))
                parse_result()
                
        return parse_result()
    
    def add_rec_id(self, rec_id: str, is_hex: bool = False) -> None:
        if not is_hex:
            rec_id = format(int(rec_id), self.Packet.FORMAT_REC_ID.value)

        # confirm if already exists
        if rec_id in self._rec_id:
            pass
        else:
            self._send_formatted(self.Command.SET_RECEIVE_ID.value, rec_id.encode(self.Packet.ENCODING_BASE.value))
            self._rec_id.add(rec_id)
            
    def clear_rec_id(self) -> None:
        self._set_params(self.Command.ERASE_RECIEVE_ID.value)
        self._rec_id.clear()
        
    def answerback_on(self) -> None:
        self._send_formatted(self.Command.ENABLE_ANSWER_BACK.value)
        
    def answerback_off(self) -> None:
        self._send_formatted(self.Command.DISABLE_ANSWER_BACK.value)
        
    def port_on(self) -> None:
        self._send_formatted(self.Command.ENABLE_COMM_PORT.value)
        
    def port_off(self) -> None:
        self._send_formatted(self.Command.DISABLE_COMM_PORT.value)
            
    @cached_property
    def id(self):
        return self._get_params(self.Command.READ_UNIQUE_ID.value)
    
    @cached_property
    def node(self):
        return self._get_params(self.Command.READ_NODE_NUM.value)
    
    @property
    def rec_id(self):
        return tuple(self._rec_id)
    
    @cached_property
    def comm_channel(self):
        return self._get_params(self.Command.READ_COMM_CHANNEL.value)
    
    @cached_property
    def rssi(self):
        return self._get_params(self.Command.READ_RSSI_VALUE.value)
    
    @cached_property
    def trans_pow(self):
        return self._get_params(self.Command.READ_TRANSMIT_POW.value)
    
    @cached_property
    def version(self):
        return self._get_params(self.Command.READ_PRODUCT_VERSION.value)
        
    @cached_property
    def baud_rate(self):
        return self.Baudrate.RATE_19200.value
    
    @cached_property
    def sleep_time(self):
        return self._get_params(self.Command.READ_SLEEP_TIME.value)
    
    @cached_property
    def intermittent_time(self):
        return self._get_params(self.Command.READ_INTERMITTENT_TIME.value)
    
    @cached_property
    def comm_speed(self):
        return self._get_params(self.Command.READ_COMM_SPEED.value)
