

from typing import Dict, List, Optional, Tuple, Union

from pisat.config.type import Logable
from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.sensor.sensor_base import SensorBase
from pisat.util.cached_property import cached_property
from pisat.util.deco import restricted_setter, restricted_range_setter


class Opt3002(SensorBase):
    
    DATA_NAMES: Tuple[str] = ("IRRADIANCE")
    DEFAULT_VALUES: Dict[str, Logable] = {}
    
    class AddrI2C:
        GND = 0b1000100
        VDD = 0b1000101
        SDA = 0b1000110
        SCL = 0b1000111
    
    class Reg:
        RESULT = 0x00
        CONFIG = 0x01
        LIMIT_LOW = 0x02
        LIMIT_HIGH = 0x03
        ID = 0x7E
        
        LEN_BYTE = 2
    
    class Data:
        MAX_EXPONENT = 0b1111
        MIN_EXPONENT = 0b0000
        MAX_MANTISSA = 0b1111_1111_1111
        MIN_MANTISSA = 0b0000_0000_0000

        BIT_EXPONENT = 0b1111_0000_0000_0000
        BIT_MANTISSA_MSB = 0b0000_1111_0000_0000
        BIT_MANTISSA_LSB = 0b0000_0000_1111_1111
        
        # nW/cm^2
        WEIGHT_OPTICAL_POWER = 1.2
        
        @classmethod
        def calc_optical_power(cls, exponent: int, mantissa: int) -> float:
            return 2**exponent * mantissa * cls.WEIGHT_OPTICAL_POWER
        
        @classmethod
        def parse_optical_power(cls, data: float) -> Tuple[int]:
            data = cls.WEIGHT_OPTICAL_POWER
            
            # decide exponent
            exponent = cls.MIN_EXPONENT
            while True:
                assessed = data / (1 << exponent)
                if cls.check_mantissa(assessed):
                    break
                
                exponent += 1
                if not cls.check_exponent(exponent):
                    raise ValueError(
                        "'data' is invalid as a optical power of OPT3002."
                    )
                    
            # decide mantissa
            mantissa = int(assessed)
            
            return (exponent, mantissa)
        
        @classmethod
        def parse_raw_data(cls, data: Union[bytes, bytearray]) -> Tuple[int]:
            raw_data = data[0] << 8 | data[1]
            exponent = raw_data & cls.BIT_EXPONENT
            mantissa = raw_data & (cls.BIT_MANTISSA_MSB | cls.BIT_MANTISSA_LSB)
            return (exponent, mantissa)
        
        @classmethod
        def make_raw_data(cls, data: float) -> bytes:
            exponent, mantissa = cls.parse_optical_power(data)
            
            data_sending = bytearray()
            data_sending.append(exponent << 4 | (mantissa & cls.BIT_MANTISSA_MSB) >> 8)
            data_sending.append(mantissa & cls.BIT_MANTISSA_LSB)
            
            return bytes(data_sending)
            
        @classmethod
        def check_exponent(cls, val: int) -> bool:
            return cls.MIN_EXPONENT <= val <= cls.MAX_EXPONENT
        
        @classmethod
        def check_mantissa(cls, val: int) -> bool:
            return cls.MIN_MANTISSA <= val <= cls.MAX_MANTISSA
    
    class Config:
        
        CONVERSION_TIME_100 = 0
        CONVERSION_TIME_800 = 1
        
        CONVERSION_MODE_SHUTDOWN = 0b00
        CONVERSION_MODE_SINGLE_SHOT = 0b01
        CONVERSION_MODE_CONTINUOUS_0 = 0b10
        CONVERSION_MODE_CONTINUOUS_1 = 0b11
        
        LATCH_HYSTERESIS = 0
        LATCH_WINDOW = 1
        
        POLARITY_ACTIVE_LOW = 0
        POLARITY_ACTIVE_HIGH = 1
        
        FAULT_COUNT_1 = 0b00
        FAULT_COUNT_2 = 0b01
        FAULT_COUNT_4 = 0b10
        FAULT_COUNT_8 = 0b11
        
        def __init__(self) -> None:            
            self._range_number: int = 0
            self._conversion_time: int = 0
            self._conversion_ope_mode: int = 0
            self._flag_overflow: int = 0
            self._conversion_ready: int = 0
            self._flag_high: int = 0
            self._flag_low: int = 0
            self._latch: int = 0
            self._polarity: int = 0
            self._mask_exponent: int = 0
            self._fault_count: int = 0
            
        def _update(self, raw: bytes):
            upper = raw[0]
            lower = raw[1]
            
            # upper byte
            self._range_number = (upper & 0b1111_0000) >> 4
            self._conversion_time = (upper & 0b0000_1000) >> 3
            self._conversion_ope_mode = (upper & 0b0000_0110) >> 1
            self._flag_overflow = upper & 0b0000_0001
            
            # lower byte
            self._conversion_ready = (lower & 0b1000_0000) >> 7
            self._flag_high = (lower & 0b0100_0000) >> 6
            self._flag_low = (lower & 0b0010_0000) >> 5
            self._latch = (lower & 0b0001_0000) >> 4
            self._polarity = (lower & 0b0000_1000) >> 3
            self._mask_exponent = (lower & 0b0000_0100) >> 2
            self._fault_count = lower & 0b0000_0011
            
        def make_config(self) -> bytes:
            upper = 0
            lower = 0
            
            # make byte of upper
            upper |= self._range_number << 4
            upper |= self._conversion_time << 2
            upper |= self._conversion_ope_mode << 1
            upper |= self._flag_overflow
            
            # make byte of lower
            lower |= self._conversion_ready << 7
            lower |= self._flag_high << 6
            lower |= self._flag_low << 5
            lower |= self._latch << 4
            lower |= self._polarity << 3
            lower |= self._mask_exponent << 2
            lower |= self._fault_count
            
            return bytes((upper, lower))
            
        @property
        def range_number(self) -> int:
            return self._range_number
        
        @range_number.setter
        @restricted_range_setter(0b0000, 0b1011)
        def range_number(self, val: int):
            self._range_number = val
        
        @property
        def conversion_time(self) -> int:
            return self._conversion_time
        
        @conversion_time.setter
        @restricted_setter(0, 1)
        def conversion_time(self, val: int):
            self._conversion_time = val
        
        @property
        def conversion_ope_mode(self) -> int:
            return self._conversion_ope_mode
        
        @conversion_ope_mode.setter
        @restricted_setter(0, 1, 2, 3)
        def conversion_ope_mode(self, val: int):
            self._conversion_ope_mode = val
        
        @property
        def flag_overflow(self) -> int:
            return self._flag_overflow
        
        @property
        def conversion_ready(self) -> int:
            return self._conversion_ready
        
        @property
        def flag_high(self) -> int:
            return self._flag_high
        
        @property
        def flag_low(self) -> int:
            return self._flag_low
        
        @property
        def latch(self) -> int:
            return self._latch
        
        @latch.setter
        @restricted_setter(0, 1)
        def latch(self, val: int):
            self._latch = val
        
        @property
        def polarity(self) -> int:
            return self._polarity
        
        @polarity.setter
        @restricted_setter(0, 1)
        def polarity(self, val: int):
            self._polarity = val
        
        @property
        def mask_exponent(self) -> int:
            return self._mask_exponent
        
        @mask_exponent.setter
        @restricted_setter(0, 1)
        def mask_exponent(self, val: int):
            self._mask_exponent = val
        
        @property
        def fault_count(self) -> int:
            return self._fault_count
        
        @fault_count.setter
        @restricted_setter(0, 1, 2, 3)
        def fault_count(self, val: int):
            self._fault_count = val
    
    def __init__(self,
                 handler: Optional[I2CHandlerBase],
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(handler=handler, debug=debug, name=name)
        
        self._handler: Optional[I2CHandlerBase] = handler
        self._config = self.Config()
        
    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        pass
    
    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        pass
    
    @cached_property
    def id(self) -> int:
        while True:
            count, data = self._handler.read(self.Reg.ID, self.Reg.LEN_BYTE)
            if count == 2:
                break
            
        return (data[0] << 7) | data[1]
    
    def _read_raw_data(self) -> Tuple[int]:
        count, data = self._handler.read(self.Reg.RESULT, self.Reg.LEN_BYTE)
        return self.Data.parse_raw_data(data)
    
    def _read_config(self):
        pass
    
    def set_high_limit(self, data: float) -> None:
        self._set_limit(self.Reg.LIMIT_HIGH, data)
        
    def set_low_limit(self, data: float) -> None:
        self._set_limit(self.Reg.LIMIT_LOW, data)
        
    def _set_limit(self, reg: int, data: float) -> None:
        data_sending = self.Data.make_raw_data(data)
        self._handler.write(reg, data_sending)
        
    def load_config(self):
        count, data = self._handler.read(self.Reg.CONFIG, self.Reg.LEN_BYTE)
        self._config._update(data)
        return self._config
    
    def set_config(self,
                   range_number: Optional[int] = None,
                   conv_time: Optional[int] = None,
                   conv_mode: Optional[int] = None,
                   latche: Optional[int] = None,
                   polarity: Optional[int] = None,
                   mask: Optional[int] = None,
                   fault_count: Optional[int] = None):
        if range_number is not None:
            self._config.range_number = range_number
        if conv_time is not None:
            self._config.conversion_time = conv_time
        if conv_mode is not None:
            self._config.conversion_ope_mode = conv_mode
        if latche is not None:
            self._config.latch = latche
        if polarity is not None:
            self._config.polarity = polarity
        if mask is not None:
            self._config.mask_exponent = mask
        if fault_count is not None:
            self._config.fault_count = fault_count
            
        data_sending = self._config.make_config()
        self._handler.write(self.Reg.CONFIG, data_sending)
    