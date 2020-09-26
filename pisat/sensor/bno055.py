

from pisat.handler.serial_handler_base import SerialHandlerBase
from typing import Dict, Optional, Tuple, Union, ValuesView
from enum import Enum, auto

from pisat.config.type import Logable
from pisat.config.dname import *
from pisat.util.cached_property import cached_property
from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.sensor.sensor_base import SensorBase


class Bno055Base(SensorBase):
    
    DATA_NAMES: Tuple[str] = ()
    DEFAULT_VALUES: Dict[str, Logable] = {}
    
    #   RESISTOR ADDRESS
    class RegPage0(Enum):
        CHIP_ID = 0x00
        ACC_ID = 0x01
        MAG_ID = 0x02
        GYR_ID = 0x03
        SW_REV_ID_LSB = 0x04
        SW_REC_ID_MSB = 0x05
        BL_REV_ID = 0x06
        PAGE_ID = 0x07
        
        ACC_DATA_X_LSB = 0x08
        ACC_DATA_X_MSB = 0x09
        ACC_DATA_Y_LSB = 0x0A
        ACC_DATA_Y_MSB = 0x0B
        ACC_DATA_Z_LSB = 0x0C
        ACC_DATA_Z_MSB = 0x0D
        MAG_DATA_X_LSB = 0x0E
        MAG_DATA_X_MSB = 0x0F
        MAG_DATA_Y_LSB = 0x10
        MAG_DATA_Y_MSB = 0x11
        MAG_DATA_Z_LSB = 0x12
        MAG_DATA_Z_MSB = 0x13
        GYR_DATA_X_LSB = 0x14
        GYR_DATA_X_MSB = 0x15
        GYR_DATA_Y_LSB = 0x16
        GYR_DATA_Y_MSB = 0x17
        GYR_DATA_Z_LSB = 0x18
        GYR_DATA_Z_MSB = 0x19
        
        EUL_HEADING_LSB = 0x1A
        EUL_HEADING_MSB = 0x1B
        EUL_ROLL_LSB = 0x1C
        EUL_ROLL_MSB = 0x1D
        EUL_PITCH_LSB = 0x1E
        EUL_PITCH_MSB = 0x1F
        QUA_DATA_W_LSB = 0x20
        QUA_DATA_W_MSB = 0x21
        QUA_DATA_X_LSB = 0x22
        QUA_DATA_X_MSB = 0x23
        QUA_DATA_Y_LSB = 0x24
        QUA_DATA_Y_MSB = 0x25
        QUA_DATA_Z_LSB = 0x26
        QUA_DATA_Z_MSB = 0x27
        LIA_DATA_X_LSB = 0x28
        LIA_DATA_X_MSB = 0x29
        LIA_DATA_Y_LSB = 0x2A
        LIA_DATA_Y_MSB = 0x2B
        LIA_DATA_Z_LSB = 0x2C
        LIA_DATA_Z_MSB = 0x2D
        GRV_DATA_X_LSB = 0x2E
        GRV_DATA_X_MSB = 0x2F
        GRV_DATA_Y_LSB = 0x30
        GRV_DATA_Y_MSB = 0x31
        GRV_DATA_Z_LSB = 0x32
        GRV_DATA_Z_MSB = 0x33
        TEMP = 0x34
        
        CALIB_STAT = 0x35
        ST_RESULT = 0x36
        INT_STA = 0x37
        SYS_CLK_STA_TUS = 0x38
        SYS_STATUS = 0x39
        SYS_ERR = 0x3A
        UNIT_SEL = 0x3B
        
        OPR_MODE = 0x3D
        PWR_MODE = 0x3E
        SYS_TRIGGER = 0x3F
        TEMP_SOURCE = 0x40
        AXIS_MAP_CONFIG = 0x41
        AXIS_MAP_SIGN = 0x42
        
        ACC_OFFSET_X_LSB = 0x55
        ACC_OFFSET_X_MSB = 0x56
        ACC_OFFSET_Y_LSB = 0x57
        ACC_OFFSET_Y_MSB = 0x58
        ACC_OFFSET_Z_LSB = 0x59
        ACC_OFFSET_Z_MSB = 0x5A
        MAG_OFFSET_X_LSB = 0x5B
        MAG_OFFSET_X_MSB = 0x5C
        MAG_OFFSET_Y_LSB = 0x5D
        MAG_OFFSET_Y_MSB = 0x5E
        MAG_OFFSET_Z_LSB = 0x5F
        MAG_OFFSET_Z_MSB = 0x60
        GYR_OFFSET_X_LSB = 0x61
        GYR_OFFSET_X_MSB = 0x62
        GYR_OFFSET_Y_LSB = 0x63
        GYR_OFFSET_Y_MSB = 0x64
        GYR_OFFSET_Z_LSB = 0x65
        GYR_OFFSET_Z_MSB = 0x66
        ACC_RADIUS_LSB = 0x67
        ACC_RADIUS_MSB = 0x68
        MAG_RADIUS_LSB = 0x69
        MAG_RADIUS_MSB = 0x6A
        
    class RegPage1(Enum):
        PAGE_ID = 0x07
        
        ACC_CONFIG = 0x08
        MAG_CONFIG = 0x09
        GYR_CONFIG_0 = 0x0A
        GYR_CONFIG_1 = 0x0B
        ACC_SLEEP_CONFIG = 0x0C
        GYR_SLEEP_CONFIG = 0x0D
        
        INT_MSK = 0x0F
        INT_EN = 0x10
        
        ACC_AM_THRES = 0x11
        ACC_INT_SETTINGS = 0x12
        ACC_HG_DURATION = 0x13
        ACC_HG_THRES = 0x14
        ACC_NM_THRES = 0x15
        ACC_NM_SET = 0x16
        GYR_INT_SETTING = 0x17
        GYR_HR_X_SET = 0x18
        GYR_DUR_X = 0x19
        GYR_HR_Y_SET = 0x1A
        GYR_DUR_Y = 0x1B
        GYR_HR_Z_SET = 0x1C
        GYR_DUR_Z = 0x1D
        GYR_AM_THRES = 0x1E
        GYR_AN_SET = 0x1F
        
    class Page(Enum):
        PAGE_0 = 0x00
        PAGE_1 = 0x01
        
    class Orientation(Enum):
        WINDOWS = 0
        ANDRROID = 1
        
    class TempUnit(Enum):
        CELSIUS = 0
        FAHRENHEIT = 1
        
    class EulerUnit(Enum):
        DEGREES = 0
        RADIANS = 1
        
    class GyroUnit(Enum):
        DPS = 0
        RPS = 1
        
    class AccUnit(Enum):
        MPS2 = 0
        MG = 1
    
    def __init__(self,
                 handler: Optional[Union[I2CHandlerBase, SerialHandlerBase]] = None,
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(handler=handler, debug=debug, name=name)
        if debug:
            return
        
        self._current_page_id = self.Page.PAGE_0.value
        
    def _read_single_byte(self, reg: int) -> int:
        pass
    
    def _write_single_byte(self, reg: int, data: bytes) -> None:
        pass
    
    def change_page(self) -> None:
        if self._current_page_id == self.Page.PAGE_0.value:
            self._write_single_byte(self.RegPage0.PAGE_ID.value, self.Page.PAGE_1.value)
        else:
            self._write_single_byte(self.RegPage1.PAGE_ID.value, self.Page.PAGE_0.value)
    
    @property
    def current_page_id(self):
        return self._current_page_id
    
    def change_unit(self, 
                    orientation: Optional[Enum] = None,
                    temp: Optional[Enum] = None,
                    euler: Optional[Enum] = None,
                    gyro: Optional[Enum] = None,
                    acc: Optional[Enum] = None) -> None:
        data = 0
        if orientation is not None:
            if isinstance(orientation, self.Orientation):
                if orientation == self.Orientation.ANDRROID:
                    data |= 1 << 7
            else:
                raise TypeError(
                    "'orientation' must be Bno055.Orientation."
                )
        if temp is not None:
            if isinstance(temp, self.TempUnit):
                if temp == self.TempUnit.FAHRENHEIT:
                    data |= 1 << 4
            else:
                raise TypeError(
                    "'temp' must be Bno055.TempUnit."
                )
        if euler is not None:
            if isinstance(euler, self.EulerUnit):
                if euler == self.EulerUnit.RADIANS:
                    data |= 1 << 2
            else:
                raise TypeError(
                    "'euler' must be Bno055.EulerUnit."
                )        
        if gyro is not None:
            if isinstance(gyro, self.GyroUnit):
                if gyro == self.GyroUnit.RPS:
                    data |= 1 << 1
            else:
                raise TypeError(
                    "'gyro' must be Bno055.GyroUnit."
                )
        if acc is not None:
            if isinstance(acc, self.AccUnit):
                if acc == self.AccUnit.MG:
                    data |= 1
            else:
                raise TypeError(
                    "'acc' must be Bno"
                )
    
    
class I2CBno055(Bno055Base):
    
    def __init__(self,
                 handler: Optional[I2CHandlerBase] = None,
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(handler=handler, debug=debug, name=name)
        if debug:
            return
        
        self._handler: Optional[I2CHandlerBase] = handler
        
    def _read_single_byte(self, reg: int) -> int:
        while True:
            count, data = self._handler.read(reg, 1)
            if count:
                break
        return data[0]
        
    @cached_property
    def chip_id(self):
        return self._read_single_byte(self.RegPage0.CHIP_ID.value)
    
    @cached_property
    def acc_id(self):
        return self._read_single_byte(self.RegPage0.ACC_ID.value)
    
    @cached_property
    def mag_id(self):
        return self._read_single_byte(self.RegPage0.MAG_ID.value)
    
    @cached_property
    def gyro_id(self):
        return self._read_single_byte(self.RegPage0.GYR_ID.value)
    
    @cached_property
    def sw_rev_id(self):
        return self._read_single_byte(self.RegPage0.SW_REC_ID_MSB.value) << 8 | \
                self._read_single_byte(self.RegPage0.SW_REV_ID_LSB.value)
                
    @cached_property
    def bl_rev_id(self):
        return self._read_single_byte(self.RegPage0.BL_REV_ID.value)
    