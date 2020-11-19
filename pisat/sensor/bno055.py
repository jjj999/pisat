

from typing import Callable, Optional, Tuple, Union
from enum import Enum

from pisat.handler.handler_base import DataBrokenError
from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.handler.serial_handler_base import SerialHandlerBase
from pisat.model.datamodel import DataModelBase, loggable
from pisat.sensor.sensor_base import SensorBase
from pisat.util.deco import cached_property
from pisat.util.type import is_all_None

class Bno055Base(SensorBase):
    

    class DataModel(DataModelBase):
        
        def setup(self, 
                  acc: Tuple[float] = (None, None, None),
                  mag: Tuple[float] = (None, None, None),
                  gyro: Tuple[float] = (None, None, None),
                  euler: Tuple[float] = (None, None, None, None),
                  quat: Tuple[float] = (None, None, None),
                  acc_lin: Tuple[float] = (None, None, None),
                  acc_gra: Tuple[float] = (None, None, None),
                  temp: float = None):
                        
            self._acc = acc
            self._mag = mag
            self._gyro = gyro
            self._euler = euler
            self._quat = quat
            self._acc_lin = acc_lin
            self._acc_gra = acc_gra
            self._temp = temp
            
            def get_name(tag: str, coo: Tuple[str]):
                return [f"{self.publisher}-{tag}_{x}" for x in coo]
            
            self._name_acc = get_name("acc", ("X", "Y", "Z"))
            self._name_mag = get_name("mag", ("X", "Y", "Z"))
            self._name_gyro = get_name("gyro", ("X", "Y", "Z"))
            self._name_euler = get_name("euler", ("HEADING", "PITCH", "ROLL"))
            self._name_quat = get_name("quat", ("X", "Y", "Z", "W"))
            self._name_acc_lin = get_name("acc_lin", ("X", "Y", "Z"))
            self._name_acc_gra = get_name("acc_gra", ("X", "Y", "Z"))
            
        @loggable
        def acc(self):
            return self._acc
        
        @acc.formatter
        def acc(self):
            return {name: val for name, val in zip(self._name_acc, self._acc)}
        
        @loggable
        def mag(self):
            return self._mag
        
        @mag.formatter
        def mag(self):
            return {name: val for name, val in zip(self._name_mag, self._mag)}
        
        @loggable
        def gyro(self):
            return self._gyro
        
        @gyro.formatter
        def gyro(self):
            return {name: val for name, val in zip(self._name_gyro, self._gyro)}
        
        @loggable
        def euler(self):
            return self._euler
        
        @euler.formatter
        def euler(self):
            return {name: val for name, val in zip(self._name_euler, self._euler)}
        
        @loggable
        def quat(self):
            return self._quat
        
        @quat.formatter
        def quat(self):
            return {name: val for name, val in zip(self._name_quat, self._quat)}
        
        @loggable
        def acc_lin(self):
            return self._acc_lin
        
        @acc_lin.formatter
        def acc_lin(self):
            return {name: val for name, val in zip(self._name_acc_lin, self._acc_lin)}
        
        @loggable
        def acc_gra(self):
            return self._acc_gra
        
        @acc_gra.formatter
        def acc_gra(self):
            return {name: val for name, val in zip(self._name_acc_gra, self._acc_gra)}
                
        @loggable
        def temp(self):
            return self._temp


    # RESISTOR ADDRESS
    class RegPage0:
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
        SYS_CLK_STATUS = 0x38
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
        
        FIRST_LEN_DATA = 32
        SECOND_LEN_DATA = 13
        FIRST_DATA_REG = ACC_DATA_X_LSB
        SECOND_DATA_REG = LIA_DATA_X_LSB
    
        
    class RegPage1:
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
        DEFAULT = PAGE_0
        
        
    class CalibStat(Enum):
        DONE = 0b11 
        NOT_DONE = 0b00
        
        
    class SelfTestResult(Enum):
        PASS = 1
        FAILED = 0
        
    
    class OperationMode(Enum):
        CONFIG_MODE = 0b0000
        ACC_ONLY = 0b0001
        MAG_ONLY = 0b0010
        GYRO_ONLY = 0b0011
        ACC_MAG = 0b0100
        ACC_GYRO = 0b0101
        MAG_GYRO = 0b0110
        AMG = 0b0111
        
        IMU = 0b1000
        COMPASS = 0b1001
        M4G = 0b1010
        NDOF_FMC_OFF = 0b1011
        NDOF = 0b1100
        
        DEFAULT = CONFIG_MODE
    
    
    class PowerMode(Enum):
        NORMAL = 0b00
        LOW_POWER = 0b01
        SUSPEND = 0b10
        DEFAULT = NORMAL
        
        
    class Orientation(Enum):
        WINDOWS = 0
        ANDROID = 1
        DEFAULT = ANDROID
        
        
    class TempUnit(Enum):
        CELSIUS = 0
        FAHRENHEIT = 1
        DEFAULT = CELSIUS
        
        
    class EulerUnit(Enum):
        DEGREES = 0
        RADIANS = 1
        DEFAULT = DEGREES
        
        
    class GyroUnit(Enum):
        DPS = 0
        RPS = 1
        DEFAULT = DPS
        
        
    class AccUnit(Enum):
        MPS2 = 0
        MG = 1
        DEFAULT = MPS2
    
    
    class TempSource(Enum):
        ACC = 0b00
        GYRO = 0b01
    
        
    class Axis(Enum):
        X = 0b00
        Y = 0b01
        Z = 0b10
        
        
    class AxisSign(Enum):
        POSITIVE = 0b0
        NEGATIVE = 0b1
        
        
    class AccConfig:
        
        class Range(Enum):
            G_2 = 0b000_000_00
            G_4 = 0b000_000_01
            G_8 = 0b000_000_10
            G_16 = 0b000_000_11
            DEFAULT = G_4
        
        class BandWidth(Enum):
            Hz_7_81 = 0b000_000_00
            Hz_15_63 = 0b000_001_00
            Hz_31_25 = 0b000_010_00
            Hz_62_5 = 0b000_011_00
            Hz_125 = 0b000_100_00
            Hz_250 = 0b000_101_00
            Hz_500 = 0b000_110_00
            Hz_1000 = 0b000_111_00
            DEFAULT = Hz_62_5
            
        class OperationMode(Enum):
            NORMAL = 0b000_000_00
            SUSPEND = 0b001_000_00
            LOW_POWER_1 = 0b010_000_00
            STANDBY = 0b011_000_00
            LOW_POWER_2 = 0b100_000_00
            DEEP_SUSPEND = 0b101_000_00
            DEFAULT = NORMAL
            
        def __init__(self) -> None:
            self._range = self.Range.DEFAULT
            self._bandwidth = self.BandWidth.DEFAULT
            self._mode = self.OperationMode.DEFAULT
            
        @property
        def range(self):
            return self._range
        
        @property
        def bandwidth(self):
            return self._bandwidth
        
        @property
        def operation_mode(self):
            return self._mode
            
        @classmethod
        def build_byte(cls, range: Enum, bandwidth: Enum, mode: Enum) -> int:
            if not isinstance(range, cls.Range):
                TypeError(
                    "'range' must be Bno055.AccConfig.Range."
                )
            if not isinstance(bandwidth, cls.BandWidth):
                TypeError(
                    "'bandwidth' must be Bno055.AccConfig.BandWidth."
                )
            if not isinstance(mode, cls.OperationMode):
                TypeError(
                    "'mode' must be Bno055.AccConfig.OperationMode."
                )
                
            return mode.value | bandwidth.value | range.value
        
        def _build_byte(self, 
                        range: Optional[Enum] = None,
                        bandwidth: Optional[Enum] = None,
                        mode: Optional[Enum] = None) -> int:
            if range is not None:
                if not isinstance(range, self.Range):
                    TypeError(
                        "'range' must be Bno055.AccConfig.Range."
                    )
                self._range = range
            if bandwidth is not None:
                if not isinstance(bandwidth, self.BandWidth):
                    TypeError(
                        "'bandwidth' must be Bno055.AccConfig.BandWidth."
                    )
                self._bandwidth = bandwidth
            if mode is not None:
                if not isinstance(mode, self.OperationMode):
                    TypeError(
                        "'mode' must be Bno055.AccConfig.OperationMode."
                    )
                self._mode = mode
            
            return self.build_byte(self._range, self._bandwidth, self._mode)
        
        
    class GyroConfig:
        
        class Range(Enum):
            DPS_2000 = 0b00_000_000
            DPS_1000 = 0b00_000_001
            DPS_500 = 0b00_000_010
            DPS_250 = 0b00_000_011
            DPS_125 = 0b00_000_100
            DEFAULT = DPS_2000
        
        class BandWidth(Enum):
            Hz_523 = 0b00_000_000
            Hz_230 = 0b00_001_000
            Hz_116 = 0b00_010_000
            Hz_47 = 0b00_011_000
            Hz_23 = 0b00_100_000
            Hz_12 = 0b00_101_000
            Hz_64 = 0b00_110_000
            Hz_32 = 0b00_111_000
            DEFAULT = Hz_32
            
        class OperationMode(Enum):
            NORMAL = 0b00000_000
            FAST_POWER = 0b00000_001
            DEEP_SUSPEND = 0b00000_010
            SUSPEND = 0b00000_011
            ADVANCED_POWER_SAVE = 0b00000_100
            DEFAULT = NORMAL
            
        def __init__(self) -> None:
            self._range = self.Range.DEFAULT
            self._bandwidth = self.BandWidth.DEFAULT
            self._mode = self.OperationMode.DEFAULT
            
        @property
        def range(self):
            return self._range
        
        @property
        def bandwidth(self):
            return self._bandwidth
        
        @property
        def operation_mode(self):
            return self._mode
            
        @classmethod
        def build_bytes(cls, range: Enum, bandwidth: Enum, mode: Enum) -> Tuple[int]:
            if range not in cls.Range:
                TypeError(
                    "'range' must be Bno055.GyroConfig.Range."
                )
            if bandwidth not in cls.BandWidth:
                TypeError(
                    "'bandwidth' must be Bno055.GyroConfig.BandWidth."
                )
            if mode not in cls.OperationMode:
                TypeError(
                    "'mode' must be Bno055.GyroConfig.OperationMode."
                )
                
            return (bandwidth.value | range.value, mode.value)
        
        def _build_bytes(self,
                         range: Optional[Enum] = None,
                         bandwidth: Optional[Enum] = None,
                         mode: Optional[Enum] = None) -> Tuple[int]:
            if range is not None:
                if not isinstance(range, self.Range):
                    TypeError(
                        "'range' must be Bno055.GyroConfig.Range."
                    )
                self._range = range
            if bandwidth is not None:
                if not isinstance(bandwidth, self.BandWidth):
                    TypeError(
                        "'bandwidth' must be Bno055.GyroConfig.BandWidth."
                    )
                self._bandwidth = bandwidth
            if mode is not None:
                if not isinstance(mode, self.OperationMode):
                    TypeError(
                        "'mode' must be Bno055.GyroConfig.OperationMode."
                    )
                self._mode = mode
            
            return self.build_bytes(self._range, self._bandwidth, self._mode)
        
        
    class MagConfig:
        
        class Rate(Enum):
            HZ_2 = 0b0_00_00_000
            HZ_6 = 0b0_00_00_001
            HZ_8 = 0b0_00_00_010
            HZ_10 = 0b0_00_00_011
            HZ_15 = 0b0_00_00_100
            HZ_20 = 0b0_00_00_101
            HZ_25 = 0b0_00_00_110
            HZ_30 = 0b0_00_00_111
            DEFAULT = HZ_10
            
        class OperationMode(Enum):
            LOW_POWER = 0b0_00_00_000
            REGULAR = 0b0_00_01_000
            ENHANCED_REGULAR = 0b0_00_10_000
            HIGH_ACCURACY = 0b0_00_11_000
            DEFAULT = REGULAR
            
        class PowerMode(Enum):
            NORMAL = 0b0_00_00_000
            SLEEP = 0b0_01_00_000
            SUSPEND = 0b0_10_00_000
            FORCE = 0b0_11_00_000
            DEFAULT = NORMAL
            
        def __init__(self) -> None:
            self._rate = self.Rate.DEFAULT
            self._o_mode = self.OperationMode.DEFAULT
            self._p_mode = self.PowerMode.DEFAULT
            
        @property
        def data_output_rate(self):
            return self._rate
        
        @property
        def oparation_mode(self):
            return self._o_mode
        
        @property
        def power_mode(self):
            return self._p_mode
            
        @classmethod
        def build_byte(cls, rate: Enum, o_mode: Enum, p_mode: Enum) -> int:
            if rate not in cls.Rate:
                TypeError(
                    "'rate' must be Bno055.MagConfig.Rate."
                )
            if o_mode not in cls.OperationMode:
                TypeError(
                    "'o_mode' must be Bno055.MagConfig.OperationMode."
                )
            if p_mode not in cls.PowerMode:
                TypeError(
                    "'p_mode' must be Bno055.MagConfig.PowerMode."
                )
                
            return p_mode.value | o_mode.value | rate.value
        
        def _build_byte(self,
                        rate: Optional[Enum] = None,
                        o_mode: Optional[Enum] = None,
                        p_mode: Optional[Enum] = None) -> int:
            if rate is not None:
                if not isinstance(rate, self.Rate):
                    TypeError(
                        "'rate' must be Bno055.MagConfig.Rate."
                    )
                self._rate = rate
            if o_mode is not None:
                if not isinstance(o_mode, self.OperationMode):
                    TypeError(
                        "'o_mode' must be Bno055.MagConfig.OperationMode."
                    )
                self._o_mode = o_mode
            if p_mode is not None:
                if not isinstance(rate, self.PowerMode):
                    TypeError(
                        "'p_mode' must be Bno055.MagConfig.PowerMode."
                    )
                self._p_mode = p_mode
                
            return self.build_byte(self._rate, self._o_mode, self._p_mode)
            
            
    class AccSleep:
        
        class Duration(Enum):
            MS_0_5 = 0b0000_0
            MS_1 = 0b0110_0
            MS_2 = 0b0111_0
            MS_4 = 0b1000_0
            MS_6 = 0b1001_0
            MS_10 = 0b1010_0
            MS_25 = 0b1011_0
            MS_50 = 0b1100_0
            MS_100 = 0b1101_0
            MS_500 = 0b1110_0
            DEFAULT = MS_0_5
            
        class Mode(Enum):
            EVENT_DRIVEN = 0b0000_0
            EQUIDISTANT = 0b0000_1
            DEFAULT = EVENT_DRIVEN
            
        def __init__(self) -> None:
            self._duration = self.Duration.DEFAULT
            self._mode = self.Mode.DEFAULT
            
        @property
        def duration(self):
            return self._duration
        
        @property
        def mode(self):
            return self._mode
            
        @classmethod
        def build_byte(cls, duration: Enum, mode: Enum) -> int:
            if not isinstance(duration, cls.Duration):
                raise TypeError(
                    "'duration' must be Bno055.AccSleep.Duration."
                )
            if not isinstance(mode, cls.Mode):
                raise TypeError(
                    "'mode' must be Bno055."
                )
            
            return duration.value | mode.value
        
        def _build_byte(self,
                        duraiton: Optional[Enum] = None,
                        mode: Optional[Enum] = None) -> int:
            if duraiton is not None:
                if not isinstance(duraiton, self.Duration):
                    raise TypeError(
                        "'duration' must be Bno055.AccSleep.Duration."
                    )
                self._duration = duraiton
            if mode is not None:
                if not isinstance(mode, self.Mode):
                    raise TypeError(
                        "'mode' must be Bno055."
                    )
                self._mode = mode
                
            return self.build_byte(self._duration, self._mode)
        
        
    class GyroSleep:
        
        class AutoDuration(Enum):
            NOT_ALLOWED = 0b00_000_000
            MS_4 = 0b00_001_000
            MS_5 = 0b00_010_000
            MS_8 = 0b00_011_000
            MS_10 = 0b00_100_000
            MS_15 = 0b00_101_000
            MS_20 = 0b00_110_000
            MS_40 = 0b00_111_000
            DEFAULT = NOT_ALLOWED
            
        class Duration(Enum):
            MS_2 = 0b00_000_000
            MS_4 = 0b00_000_001
            MS_5 = 0b00_000_010
            MS_8 = 0b00_000_011
            MS_10 = 0b00_000_100
            MS_15 = 0b00_000_101
            MS_18 = 0b00_000_110
            MS_29 = 0b00_000_111
            DEFAULT = MS_2
            
        def __init__(self) -> None:
            self._auto_duration = self.AutoDuration.DEFAULT
            self._duration = self.AutoDuration.DEFAULT
            
        @property
        def auto_duration(self):
            return self._auto_duration
        
        @property
        def duration(self):
            return self._duration
            
        @classmethod
        def build_byte(cls, auto_duration: Enum, duration: Enum) -> int:
            if not isinstance(auto_duration, cls.AutoDuration):
                raise TypeError(
                    "'auto_duration' must be Bno055.GyroSleep.AutoDuration."
                )
            if not isinstance(duration, cls.Duration):
                raise TypeError(
                    "'duration' must be Bno055.GyroSleep.Duration."
                )
            return auto_duration.value | duration.value
        
        def _build_byte(self,
                        auto_duration: Optional[Enum] = None,
                        duration: Optional[Enum] = None) -> int:
            if auto_duration is not None:
                if not isinstance(auto_duration, self.AutoDuration):
                    raise TypeError(
                        "'auto_duration' must be Bno055.GyroSleep.AutoDuration."
                    )
                self._auto_duration = auto_duration
            if duration is not None:
                if not isinstance(duration, self.Duration):
                    raise TypeError(
                        "'duration' must be Bno055.GyroSleep.Duration."
                    )
                self._duration = duration
                
            return self.build_byte(self._auto_duration, self._duration)
            
            
    class InterruptEnabled:
            
        class State(Enum):
            ENABLED = 1
            DISABLED = 0
        
            @classmethod
            def build(cls,
                      acc_nm: Enum,
                      acc_am: Enum,
                      acc_hg: Enum,
                      gyro_hr: Enum,
                      gyro_am: Enum) -> int:
                for arg in locals().values()[1:]:
                    if not isinstance(arg, cls):
                        raise TypeError(
                            "The arguments must be Bno055.InterruptEnabled.State."
                        )
                
                return acc_nm.value << 7 | acc_am.value << 6 | acc_hg << 5 |\
                    gyro_hr.value << 3 | gyro_am.value << 2
        
        def __init__(self) -> None:
            self._acc_nm = self.State.DISABLED
            self._acc_am = self.State.DISABLED
            self._acc_hg = self.State.DISABLED
            self._gyro_hr = self.State.DISABLED
            self._gyro_am = self.State.DISABLED
            
        @classmethod
        def _set_state(cls, state, attr: Optional[bool] = None) -> None:
            if attr is not None:
                if isinstance(attr, bool):
                    if attr:
                        state = cls.State.ENABLED
                    else:
                        state = cls.State.DISABLED
                else:
                    TypeError(
                        "'attr' must be bool or None."
                    )
            
        def _build_byte(self,
                        acc_nm: Optional[bool] = None,
                        acc_am: Optional[bool] = None,
                        acc_hg: Optional[bool] = None,
                        gyro_hr: Optional[bool] = None,
                        gyro_am: Optional[bool] = None) -> int:
            for arg, state in zip((acc_nm, acc_am, acc_hg, gyro_hr, gyro_am),
                                  (self._acc_nm, self._acc_am, self._acc_hg, self._gyro_hr, self._gyro_am)):
                self._set_state(state, arg)
            return self.State.build(self._acc_nm, self._acc_am, self._acc_hg, self._gyro_hr, self._gyro_am)
            
        @property
        def acc_nm(self):
            return self._acc_nm
        
        @property
        def acc_am(self):
            return self._acc_am
        
        @property
        def acc_hg(self):
            return self._acc_hg
        
        @property
        def gyro_hr(self):
            return self._gyro_hr
        
        @property
        def gyro_am(self):
            return self._gyro_am
        
        
    class InterruptMask:
        
        class State(Enum):
            ENABLED = 1
            DISABLED = 0
        
            @classmethod
            def build(cls,
                      acc_nm: Enum,
                      acc_am: Enum,
                      acc_hg: Enum,
                      gyro_hr: Enum,
                      gyro_am: Enum) -> int:
                for arg in locals().values()[1:]:
                    if not isinstance(arg, cls):
                        raise TypeError(
                            "The arguments must be Bno055.InterruptMask.State."
                        )
                
                return acc_nm.value << 7 | acc_am.value << 6 | acc_hg << 5 |\
                    gyro_hr.value << 3 | gyro_am.value << 2
        
        def __init__(self) -> None:
            self._acc_nm = self.State.DISABLED
            self._acc_am = self.State.DISABLED
            self._acc_hg = self.State.DISABLED
            self._gyro_hr = self.State.DISABLED
            self._gyro_am = self.State.DISABLED
            
        @classmethod
        def _set_state(cls, state, attr: Optional[bool] = None) -> None:
            if attr is not None:
                if isinstance(attr, bool):
                    if attr:
                        state = cls.State.ENABLED
                    else:
                        state = cls.State.DISABLED
                else:
                    TypeError(
                        "'attr' must be bool or None."
                    )
            
        def _build_byte(self,
                        acc_nm: Optional[bool] = None,
                        acc_am: Optional[bool] = None,
                        acc_hg: Optional[bool] = None,
                        gyro_hr: Optional[bool] = None,
                        gyro_am: Optional[bool] = None) -> int:
            for arg, state in zip((acc_nm, acc_am, acc_hg, gyro_hr, gyro_am),
                                  (self._acc_nm, self._acc_am, self._acc_hg, self._gyro_hr, self._gyro_am)):
                self._set_state(state, arg)
            return self.State.build(self._acc_nm, self._acc_am, self._acc_hg, self._gyro_hr, self._gyro_am)
            
        @property
        def acc_nm(self):
            return self._acc_nm
        
        @property
        def acc_am(self):
            return self._acc_am
        
        @property
        def acc_hg(self):
            return self._acc_hg
        
        @property
        def gyro_hr(self):
            return self._gyro_hr
        
        @property
        def gyro_am(self):
            return self._gyro_am
        
            
    def __init__(self,
                 handler: Union[I2CHandlerBase, SerialHandlerBase],
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._handler = handler
        
        self._current_page = self.Page.DEFAULT
        
        # Calibration Status
        self._calib_stat_sys = self.CalibStat.NOT_DONE
        self._calib_stat_gyro = self.CalibStat.NOT_DONE
        self._calib_stat_acc = self.CalibStat.NOT_DONE
        self._calib_stat_mag = self.CalibStat.NOT_DONE
        
        # Self-Test Status
        self._sefltest_result_mcu = self.SelfTestResult.FAILED
        self._selftest_result_mag = self.SelfTestResult.FAILED
        self._selftest_result_gyro = self.SelfTestResult.FAILED
        self._sefltest_result_acc = self.SelfTestResult.FAILED
        
        # Mode
        self._operation_mode = self.OperationMode.DEFAULT
        self._power_mode = self.PowerMode.DEFAULT
        
        self._orientation = self.Orientation.DEFAULT
        self._unit_temp = self.TempUnit.DEFAULT
        self._unit_euler = self.EulerUnit.DEFAULT
        self._unit_gyro = self.GyroUnit.DEFAULT
        self._unit_acc = self.AccUnit.DEFAULT
        
        self._external_oscillator = False
        
        self._axis_x = self.Axis.X
        self._sign_x = self.AxisSign.POSITIVE
        self._axis_y = self.Axis.Y
        self._sign_y = self.AxisSign.POSITIVE
        self._axis_z = self.Axis.Z
        self._sign_z = self.AxisSign.POSITIVE
        
        self._config_acc = self.AccConfig()
        self._config_gyro = self.GyroConfig()
        self._config_mag = self.MagConfig()
        
        self._sleep_acc = self.AccSleep()
        self._sleep_gyro = self.GyroSleep()
        
        self._interrupt_enabled = self.InterruptEnabled()
        self._interrupt_mask = self.InterruptMask()
        
    # NOTE
    # This method should be called in __init__ of the subclasses.
    def setup(self) -> None:
        self._read_map_config()
        self._read_map_sign()
        
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   Abstract Method                                                         #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
        
    # NOTE To be overrided
    def _read_single_byte(self, reg: int) -> int:
        pass
    
    # NOTE To be overrided
    def _read_seq_bytes(self, reg: int, counts: int) -> bytes:
        pass
    
    # NOTE To be overrided
    def _write_single_byte(self, reg: int, data: bytes) -> None:
        pass
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   Reading Data                                                            #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    
    def read(self):
        raw = self._retreive_data()
        vec_acc = self._calc_vector(raw[:6], self._calc_acc)
        vec_mag = self._calc_vector(raw[6:12], self._calc_mag)
        vec_gyro = self._calc_vector(raw[12:18], self._calc_gyro)
        vec_euler = self._calc_vector(raw[18:24], self._calc_euler)
        vec_quaternion = self._calc_vector(raw[24:32], self._calc_quaternion)
        vec_lin_acc = self._calc_vector(raw[32:38], self._calc_acc)
        vec_grv_acc = self._calc_vector(raw[38:44], self._calc_acc)
        temp = self._calc_temp(raw[44])
        
        model = self.DataModel(self.name)
        model.setup(acc=vec_acc, mag=vec_mag, gyro=vec_gyro, euler=vec_euler,
                    quat=vec_quaternion, acc_lin=vec_lin_acc, acc_gra=vec_grv_acc, temp=temp)
        return model

    def _retreive_data(self) -> bytearray:
        raw = bytearray()
        raw.extend(self._read_seq_bytes(self.RegPage0.FIRST_DATA_REG, self.RegPage0.FIRST_LEN_DATA))
        raw.extend(self._read_seq_bytes(self.RegPage0.SECOND_DATA_REG, self.RegPage0.SECOND_LEN_DATA))
        return raw
    
    def _calc_vector(self, data: bytes, func: Callable[[int], Union[int, float]]) -> Tuple[float]:
        vector = []
        for i in range(len(data) // 2):
            element = data[i * 2 + 1] << 8 | data[i * 2]
            if (element & 0x8000):
                element -= 0xFFFF + 1
                
            vector.append(element)

        return tuple(map(func, vector))                
    
    def _calc_acc(self, data: int) -> float:
        # See datasheet page 31
        if self._unit_acc == self.AccUnit.MPS2:
            return data / 100
        else:
            return data
        
    def _calc_mag(self, data: int) -> float:
        # See datasheet page 32
        return data / 16
    
    def _calc_gyro(self, data: int) -> float:
        # See datasheet page 33
        if self._unit_gyro == self.GyroUnit.DPS:
            return data / 16
        else:
            return data / 900
        
    def _calc_euler(self, data: int) -> float:
        # See datasheet page 35
        if self._unit_euler == self.EulerUnit.DEGREES:
            return data / 16
        else:
            return data / 900
        
    def _calc_quaternion(self, data: int) -> float:
        # See datasheet page 35
        return data / (2 << 13)
    
    def _calc_temp(self, data: int) -> int:
        # See datasheet page 37
        if (data & 0x8000):
                data -= 0xFFFF + 1
        
        if self._unit_temp == self.TempUnit.CELSIUS:
            return data
        else:
            return data * 2
        
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   For Setting                                                             #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    
    class ConfigContext:
        
        def __init__(self, bno055) -> None:
            self._bno055 = bno055
            self._last_operation_mode = self._bno055.operation_mode
        
        def __enter__(self):
            self._bno055.change_operation_mode(self._bno055.OperationMode.CONFIG_MODE)
            return self._bno055

        def __exit__(self, exc_type, exc_value, traceback):
            self._bno055.change_operation_mode(self._last_operation_mode)
    
    @property
    def config(self):
        config = self.ConfigContext(self)
        return config
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   ID                                                                      #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
                
    @cached_property
    def chip_id(self):
        return self._read_single_byte(self.RegPage0.CHIP_ID)
    
    @cached_property
    def acc_id(self):
        return self._read_single_byte(self.RegPage0.ACC_ID)
    
    @cached_property
    def mag_id(self):
        return self._read_single_byte(self.RegPage0.MAG_ID)
    
    @cached_property
    def gyro_id(self):
        return self._read_single_byte(self.RegPage0.GYR_ID)
    
    @cached_property
    def sw_rev_id(self):
        return self._read_single_byte(self.RegPage0.SW_REC_ID_MSB) << 8 | \
                self._read_single_byte(self.RegPage0.SW_REV_ID_LSB)
                
    @cached_property
    def bootloader_rev_id(self):
        return self._read_single_byte(self.RegPage0.BL_REV_ID)
                
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   Page                                                                    #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #   
    
    def change_page(self) -> None:
        if self._current_page == self.Page.PAGE_0:
            self._write_single_byte(self.RegPage0.PAGE_ID, self.Page.PAGE_1.value)
        else:
            self._write_single_byte(self.RegPage1.PAGE_ID, self.Page.PAGE_0.value)
    
    @property
    def current_page_id(self):
        return self._current_page
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    #   Calibration
    #
    #   See datasheet Page 47 and 67.
    #   Calibration status is managed by CalibStatus object.
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -     
    
    def load_calib_stat(self) -> None:
        raw = self._read_single_byte(self.RegPage0.CALIB_STAT)
        
        sys = (raw & 0b11_00_00_00) >> 6
        gyro = (raw & 0b00_11_00_00) >> 4
        acc = (raw & 0b00_00_11_00) >> 2
        mag = raw & 0b00_00_00_11
        
        for status in self.CalibStat:
            if sys == status.value:
                self._calib_stat_sys = status
            if gyro == status.value:
                self._calib_stat_gyro = status
            if acc == status.value:
                self._calib_stat_acc = status
            if mag == status.value:
                self._calib_stat_mag = status
                    
    @property
    def calib_stat_sys(self):
        return self._calib_stat_sys
    
    @property
    def calib_stat_gyro(self):
        return self._calib_stat_gyro
    
    @property
    def calib_stat_acc(self):
        return self._calib_stat_acc
    
    @property
    def calib_stat_mag(self):
        return self._calib_stat_mag
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    #   Self-Test
    #
    #   See datasheet Page 46 and 67
    #   Self-Test result is managed by SelfTestResult object.
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
        
    def load_st_result(self) -> None:
        raw = self._read_single_byte(self.RegPage0.ST_RESULT)
        
        mcu = (raw & 0b0000_1000) >> 3
        gyro = (raw & 0b0000_0100) >> 2
        mag = (raw & 0b0000_0010) >> 1
        acc = raw & 0b0000_0001
        
        for status in self.SelfTestResult:
            if mcu == status.value:
                self._sefltest_result_mcu = status
            if gyro == status.value:
                self._selftest_result_gyro = status
            if mag == status.value:
                self._selftest_result_mag = status
            if acc == status.value:
                self._selftest_result_acc = status
    
    @property
    def result_self_test_mcu(self):
        return self._selftest_result_mcu
    
    @property
    def result_self_test_gyro(self):
        return self._selftest_result_gyro
    
    @property
    def result_self_test_mag(self):
        return self._selftest_result_mag
    
    @property
    def result_self_test_acc(self):
        return self._selftest_result_acc
    
    def trigger_selftest(self) -> None:
        if self._external_oscillator:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b11100000)
        else:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b01100000)
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    #   Operation Mode
    #
    #   See datasheet Page 20 ~ 23
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    def change_operation_mode(self, mode: Enum) -> None:
        if not isinstance(mode, self.OperationMode):
            raise TypeError(
                "'mode' must be Bno055.OperationMode."
            )
        self._write_single_byte(self.RegPage0.OPR_MODE, mode.value)
        self._operation_mode = mode
            
    @property
    def operation_mode(self):
        return self._operation_mode
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    #   Power Mode
    #
    #   See datasheet Page 18 ~ 20
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    def change_power_mode(self, mode: Enum) -> None:
        if not isinstance(mode, self.PowerMode):
            raise TypeError(
                "'mode' must be Bno055.PowerMode."
            )
        
        with self.config:
            self._write_single_byte(self.RegPage0.PWR_MODE, mode.value)
        self._power_mode = mode
        
    @property
    def power_mode(self):
        return self._power_mode
    
    # TODO
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    #   Interrupt
    #
    #   See datasheet Page 38 ~ 45
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    
    def _read_interrupt_status(self) -> Tuple[int]:
        data = self._read_single_byte(self.RegPage0.INT_STA)
        return (data & 0b10000000, data & 0b01000000, data & 0b00100000, data & 0b00001000, data & 0b00000100)
    
    @property
    def interrupt_status(self):
        return self._read_interrupt_status()
    
    @property
    def is_interrupted_acc_nomotion(self):
        return bool(self._read_interrupt_status()[0])
    
    @property
    def is_interrupted_acc_anymotion(self):
        return bool(self._read_interrupt_status()[1])
    
    @property
    def is_interrupted_acc_highG(self):
        return bool(self._read_interrupt_status()[2])
    
    @property
    def is_interrupted_gyro_highrate(self):
        return bool(self._read_interrupt_status()[3])
    
    @property
    def is_interrupted_gyro_anymotion(self):
        return bool(self._read_interrupt_status()[4])
    
    def reset_interrupt(self) -> None:
        if self._external_oscillator:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b10100001)
        else:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b00100001)
            
    def set_int_mask(self,
                     acc_nm: Optional[bool] = None,
                     acc_am: Optional[bool] = None,
                     acc_hg: Optional[bool] = None,
                     gyro_hr: Optional[bool] = None,
                     gyro_am: Optional[bool] = None) -> None:
        data = self._interrupt_mask._build_byte(acc_nm, acc_am, acc_hg, gyro_hr, gyro_am)
        self._write_single_byte(self.RegPage1.INT_MSK.value, data)
        
    @property
    def interrupt_mask(self):
        return self._interrupt_mask
        
    def set_int_enabled(self,
                        acc_nm: Optional[bool] = None,
                        acc_am: Optional[bool] = None,
                        acc_hg: Optional[bool] = None,
                        gyro_hr: Optional[bool] = None,
                        gyro_am: Optional[bool] = None) -> None:
        data = self._interrupt_enabled._build_byte(acc_nm, acc_am, acc_hg, gyro_hr, gyro_am)
        self._write_single_byte(self.RegPage1.INT_EN.value, data)
    
    @property
    def interrupt_enabled(self):
        return self._interrupt_enabled
    
    # TODO
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    #   Internal Status
    #
    #   See datasheet Page 38 ~ 45
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    
    @property
    def status_system_clock(self):
        return self._read_single_byte(self.RegPage0.SYS_CLK_STATUS) & 0b00000001
    
    @property
    def status_system(self):
        return self._read_single_byte(self.RegPage0.SYS_STATUS)
    
    @property
    def status_system_error(self):
        return self._read_single_byte(self.RegPage0.SYS_ERR)
    
    # TODO
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    #   Units
    #
    #   See datasheet Page 30 ~ 37
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
    
    def change_unit(self, 
                    orientation: Optional[Enum] = None,
                    temp: Optional[Enum] = None,
                    euler: Optional[Enum] = None,
                    gyro: Optional[Enum] = None,
                    acc: Optional[Enum] = None) -> None:
        data = 0
        if orientation is not None:
            if isinstance(orientation, self.Orientation):
                if orientation == self.Orientation.ANDROID:
                    data |= 1 << 7
                    self._orientation = self.Orientation.ANDROID
                else:
                    self._orientation = self.Orientation.WINDOWS
            else:
                raise TypeError(
                    "'orientation' must be Bno055.Orientation."
                )
        if temp is not None:
            if isinstance(temp, self.TempUnit):
                if temp == self.TempUnit.FAHRENHEIT:
                    self._unit_temp = self.TempUnit.FAHRENHEIT
                    data |= 1 << 4
                else:
                    self._unit_temp = self.TempUnit.CELSIUS
            else:
                raise TypeError(
                    "'temp' must be Bno055.TempUnit."
                )
        if euler is not None:
            if isinstance(euler, self.EulerUnit):
                if euler == self.EulerUnit.RADIANS:
                    data |= 1 << 2
                    self._unit_euler = self.EulerUnit.RADIANS
                else:
                    self._unit_euler = self.EulerUnit.DEGREES
            else:
                raise TypeError(
                    "'euler' must be Bno055.EulerUnit."
                )        
        if gyro is not None:
            if isinstance(gyro, self.GyroUnit):
                if gyro == self.GyroUnit.RPS:
                    data |= 1 << 1
                    self._unit_gyro = self.GyroUnit.RPS
                else:
                    self._unit_gyro = self.GyroUnit.DPS
            else:
                raise TypeError(
                    "'gyro' must be Bno055.GyroUnit."
                )
        if acc is not None:
            if isinstance(acc, self.AccUnit):
                if acc == self.AccUnit.MG:
                    data |= 1
                    self._unit_acc = self.AccUnit.MG
                else:
                    self._unit_acc = self.AccUnit.MPS2
            else:
                raise TypeError(
                    "'acc' must be Bno"
                )
    
    @property
    def orientation(self):
        return self._orientation
    
    @property
    def unit_temp(self):
        return self._unit_temp
    
    @property
    def unit_euler(self):
        return self._unit_euler
    
    @property
    def unit_gyro(self):
        return self._unit_gyro
    
    @property
    def unit_acc(self):
        return self._unit_acc
    
    # TODO
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   Sleep Configuration
    #
    #   See datasheet page 79 ~ 80
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   Axis Map                                                                #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
        
    def _configure_map_config(self,
                              x: Optional[Enum] = None,
                              y: Optional[Enum] = None,
                              z: Optional[Enum] = None) -> int:

        if x is not None:
            if not isinstance(x, self.Axis):
                TypeError(
                "'x' must be Bno055.Axis or None."
                )
            self._axis_x = x
          
        if y is not None:
            if not isinstance(y, self.Axis):
                TypeError(
                "'y' must be Bno055.Axis or None."
                )
            self._axis_y = y

        if z is not None:
            if not isinstance(z, self.Axis):
                TypeError(
                "'z' must be Bno055.Axis or None."
                )
            self._axis_z = z
            
        return self._axis_z.value << 4 | self._axis_y.value << 2 | self._axis_x.value
            
    def _configure_map_sign(self,
                            x_sign: Optional[Enum] = None,
                            y_sign: Optional[Enum] = None,
                            z_sign: Optional[Enum] = None) -> int:
 
        if x_sign is not None:
            if not isinstance(x_sign, self.AxisSign):
                TypeError(
                "'x_sign' must be Bno055.AxisSign or None."
                )
            self._sign_x = x_sign
            
        if y_sign is not None:
            if not isinstance(y_sign, self.AxisSign):
                TypeError(
                "'y_sign' must be Bno055.AxisSign or None."
                )
            self._sign_y = y_sign

        if z_sign is not None:
            if not isinstance(z_sign, self.AxisSign):
                TypeError(
                "'z_sign' must be Bno055.AxisSign or None."
                )
            self._sign_z = z_sign
        
        return self._sign_x.value << 2 | self._sign_y.value << 1 | self._sign_z.value
    
    def reset_axis(self) -> None:
        self.remap_axis(self.Axis.X, self.Axis.Y, self.Axis.Z)
        
    def remap_axis(self, 
                   x: Enum,
                   y: Enum,
                   z: Enum) -> None:
        
        if isinstance(x, self.Axis) and isinstance(y, self.Axis) and isinstance(z, self.Axis):
            if x != y and y != z and z != x:
                with self.config:
                    raw = self._configure_map_config(x, y, z)
                    self._write_single_byte(self.RegPage0.AXIS_MAP_CONFIG, raw)
            else:
                raise ValueError(
                    "'x', 'y' and 'z' must be all diffrent from each other."
                )
        else:
            raise TypeError(
                "'x', 'y' and 'z' must be Bno055.Axis.X, Y or Z."
            )
                    
    def reset_sign(self) -> None:
        self.remap_sign(self.AxisSign.POSITIVE, self.AxisSign.POSITIVE, self.AxisSign.POSITIVE)
            
    def remap_sign(self,
                   x: Optional[Enum] = None,
                   y: Optional[Enum] = None,
                   z: Optional[Enum] = None) -> None:
        if not is_all_None(x, y, z):
            with self.config:
                self._write_single_byte(self.RegPage0.AXIS_MAP_SIGN, self._configure_map_sign(x, y, z))
            
    def _read_map_config(self) -> None:
        raw = self._read_single_byte(self.RegPage0.AXIS_MAP_CONFIG)
        x = raw & 0b00_00_00_11
        y = (raw & 0b00_00_11_00) >> 2
        z = (raw & 0b00_11_00_00) >> 4
        
        for axis in self.Axis:
            if x == axis.value:
                self._axis_x = axis
            if y == axis.value:
                self._axis_y = axis
            if z == axis.value:
                self._axis_z = axis
                
    def _read_map_sign(self) -> None:
        raw = self._read_single_byte(self.RegPage0.AXIS_MAP_SIGN)
        x = (raw & 0b00000_1_0_0) >> 2
        y = (raw & 0b00000_0_1_0) >> 1
        z = raw & 0b00000_0_0_1
        
        for sign in self.AxisSign:
            if x == sign.value:
                self._sign_x = sign
            if y == sign.value:
                self._sign_y = sign
            if z == sign.value:
                self._sign_z = sign
            
    @property
    def axis_x(self):
        return self._axis_x
    
    @property
    def axis_y(self):
        return self._axis_y
    
    @property
    def axis_z(self):
        return self._axis_z
    
    @property
    def sign_x(self):
        return self._sign_x
    
    @property
    def sign_y(self):
        return self._sign_y
    
    @property
    def sign_z(self):
        return self._sign_z

    # TODO
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   Sensor Configuration
    #
    #   See datasheet page 26 ~ 29
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    def set_config_acc(self,
                       range: Optional[Enum] = None,
                       bandwidth: Optional[Enum] = None,
                       mode: Optional[Enum] = None) -> None:
        data = self._config_acc._build_byte(range, bandwidth, mode)
        self._write_single_byte(self.RegPage1.ACC_CONFIG.value, data)
        
    @property
    def config_acc(self):
        return self._config_acc
        
    def set_config_mag(self,
                       rate: Optional[Enum] = None,
                       o_mode: Optional[Enum] = None,
                       p_mode: Optional[Enum] = None) -> None:
        data = self._config_mag._build_byte(rate, o_mode, p_mode)
        self._write_single_byte(self.RegPage1.MAG_CONFIG.value, data)
        
    @property
    def config_mag(self):
        return self._config_mag
        
    def set_config_gyro(self,
                        range: Optional[Enum] = None,
                        bandwidth: Optional[Enum] = None,
                        mode: Optional[Enum] = None) -> None:
        data_0, data_1 = self._config_gyro._build_bytes(range, bandwidth, mode)
        self._write_single_byte(self.RegPage1.GYR_CONFIG_0.value, data_0)
        self._write_single_byte(self.RegPage1.GYR_CONFIG_1.value, data_1)
        
    @property
    def config_gyro(self):
        return self._config_gyro
    
    # TODO
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   Sleep Configuration
    #
    #   See datasheet page 79 ~ 80
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        
    def set_sleep_acc(self,
                      duration: Optional[Enum] = None,
                      mode: Optional[Enum] = None) -> None:
        data = self._sleep_acc.build_byte(duration, mode)
        self._write_single_byte(self.RegPage1.ACC_SLEEP_CONFIG.value, data)
        
    @property
    def sleep_acc(self):
        return self._sleep_acc
    
    def set_sleep_gyro(self,
                       auto_duration: Optional[Enum] = None,
                       duration: Optional[Enum] = None) -> None:
        data = self._sleep_gyro.build_byte(auto_duration, duration)
        self._write_single_byte(self.RegPage1.GYR_SLEEP_CONFIG.value, data)
        
    @property
    def sleep_gyro(self):
        return self._sleep_gyro
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   Others
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    def change_oscillator(self, external: bool = False) -> None:
        if external and not self._external_oscillator:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b11100001)
        elif not external and self._external_oscillator:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b01100001)
            
    def reset_system(self) -> None:
        if self._external_oscillator:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b11000001)
        else:
            self._write_single_byte(self.RegPage0.SYS_TRIGGER, 0b01000001)
        
    def change_temp_source(self, src: Enum) -> None:
        if not isinstance(src, self.TempSource):
            raise TypeError(
                "'src' must be Bno055.TempSource."
            )
        self._write_single_byte(self.RegPage0.TEMP_SOURCE, src.value)
    

class I2CBno055(Bno055Base):
    
    def __init__(self,
                 handler: I2CHandlerBase,
                 name: Optional[str] = None) -> None:
        super().__init__(handler, name=name)
        
        self._handler: I2CHandlerBase = handler
        
    def _read_single_byte(self, reg: int) -> int:
        while True:
            count, data = self._handler.read(reg, 1)
            if count:
                break
        return data[0]

    def _read_seq_bytes(self, reg: int, counts: int) -> bytes:
        count, raw = self._handler.read(reg, counts)
        return bytes(raw)
        
    def _write_single_byte(self, reg: int, data: int) -> None:
        if not(0 <= data <= 0xFF):
            raise ValueError(
                f"'data' must be 0 <= 'data' <= {0xFF}"
            )
        self._handler.write(reg, data)
        
        
class UARTBno055(Bno055Base):
    
    class Protocol(Enum):
        BAUDRATE = 115200
        START_BYTE = 0xAA
        WRITE_BYTE = 0x00
        READ_BYTE = 0x01
        READ_RESPONSE = 0xBB
        RESPONSE_HEADER = 0xEE
    
    class StatusWrite(Enum):
        SUCCESS = 0x01
        FAIL = 0x03
        REGMAP_INVALID_ADDRESS = 0x04
        REGMAP_WRITE_DISABLED = 0x05
        WRONG_START_BYTE = 0x06
        BUS_OVER_RUN_ERROR = 0x07
        MAX_LENGTH_ERROR = 0x08
        MIN_LENGTH_ERROR = 0x09
        RECEIVE_CHARACTER_TIMEOUT = 0x0A
        
    class StatusRead(Enum):
        FAIL = 0x02
        REGMAP_INVALID_ADDRESS = 0x04
        REGMAP_WRITE_DISABLED = 0x05
        WRONG_START_BYTE = 0x06
        BUS_OVER_RUN_ERROR = 0x07
        MAX_LENGTH_ERROR = 0x08
        MIN_LENGTH_ERROR = 0x09
        RECEIVE_CHARACTER_TIMEOUT = 0x0A
    
    def __init__(self,
                 handler: SerialHandlerBase,
                 name: Optional[str] = None) -> None:
        super().__init__(handler, name=name)

        self._handler: Optional[SerialHandlerBase] = handler
        self._clear_buf()
        
    def _clear_buf(self):
        while self._handler.counts_readable:
            self._handler.read(1)
        
    def _read_single_byte(self, reg: int) -> int:
        return self._read_seq_bytes(reg, 1)[0]
    
    def _read_seq_bytes(self, reg: int, counts: int) -> bytes:
        # send command to read
        raw = bytearray()
        raw.append(self.Protocol.START_BYTE.value)
        raw.append(self.Protocol.READ_BYTE.value)
        raw.append(reg)
        raw.append(counts)
        self._handler.write(raw)
        
        # wait response
        while self._handler.counts_readable < 2:
            pass
        
        # response handling
        _, response = self._handler.read(2)
        if response[0] == self.Protocol.READ_RESPONSE.value:
            pass
        elif response[0] == self.Protocol.RESPONSE_HEADER.value:
            if response[1] == self.StatusRead.FAIL.value:
                self._read_seq_bytes(reg, counts)
            else:
                for status in self.StatusRead:
                    if response[1] == status.value:
                        raise DataBrokenError(
                            "Reading register has failed. STATUS: {}"
                            .format(status)
                        )
        else:
            raise DataBrokenError(
                "Found data read was broken."
            )

        length = response[1]
        while self._handler.counts_readable < length:
            pass

        recv_count, data = self._handler.read(length)
        if recv_count != length:
            raise DataBrokenError(
                "Found data read was broken."
            )
            
        return data
    
    def _write_single_byte(self, reg: int, data: bytes) -> None:
        # send command to write
        raw = bytearray()
        raw.append(self.Protocol.START_BYTE.value)
        raw.append(self.Protocol.WRITE_BYTE.value)
        raw.append(reg)
        raw.append(len(data))
        raw.extend(data)
        self._handler.write(raw)
        
        # wait response
        while self._handler.counts_readable < 2:
            pass
        
        # response handling
        _, response = self._handler.read(2)
        if response[0] == self.Protocol.RESPONSE_HEADER.value:
            if response[1] == self.StatusWrite.SUCCESS.value:
                pass
            elif response[1] == self.StatusWrite.FAIL.value:
                # try agin
                self._write_single_byte(self, reg, data)
            else:
                for status in self.StatusWrite:
                    if response[1] == status.value:
                        raise DataBrokenError(
                            "Writing register has failed. STATUS: {}"
                            .format(status)
                        )
                else:
                    raise DataBrokenError(
                        "Writing register has faild and any status has not been found."
                    )
        else:
            raise DataBrokenError(
                "Found data read was broken."
            )
            
    
class Bno055(Bno055Base):
    
    def __init__(self,
                 handler: Union[I2CHandlerBase, SerialHandlerBase],
                 name: Optional[str] = None) -> None:
        super().__init__(handler, name=name)
    
        self._base: Optional[Bno055Base] = None
        
        if isinstance(handler, I2CHandlerBase):
            self._base = I2CBno055(handler, name=name)
        elif isinstance(handler, SerialHandlerBase):
            self._base = SerialHandlerBase(handler, name=name)
            
        self._read_single_byte = self._base._read_single_byte
        self._read_seq_bytes = self._base._read_seq_bytes
        self._write_single_byte = self._base._write_single_byte
        
        self.setup()
    