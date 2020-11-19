#! python3

"""

pisat.sensor.sensor.apds9301
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sensor class of APDS280 compatible with the pisat system.
This module works completely, regardless of whether using the pisat system or not.

[info]
APDS9301 datasheet
    https://datasheetspdf.com/datasheet/APDS-9301.html

TODO    interrupt settings, debug, docstring
"""

import math
from typing import Optional, Tuple

from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.model.datamodel import DataModelBase, loggable
from pisat.sensor.sensor_base import HandlerMismatchError, HandlerNotSetError
from pisat.sensor.sensor_base import SensorBase


class Apds9301(SensorBase):
    
    ADDRESS_I2C_GND             = 0x29
    ADDRESS_I2C_FLOAT           = 0x39
    ADDRESS_I2C_VDD             = 0x49
    
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   NOTE
    #
    #       1.  Each Registers are represented as compination of 
    #           the bits of command fields and one of the bits
    #           of register address.
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    #   BITS OF COMMAND FIELD
    BITS_COMMAND_CMD                = 0b10000000
    BITS_COMMAND_CLEAR              = 0b01000000
    BITS_COMMAND_WORD               = 0b00100000

    #   BITS OF RESISTOR ADDRESS
    BITS_REG_CTRL                   = 0x0
    BITS_REG_TIMING                 = 0x1
    BITS_REG_THRESH_LOW_LOW         = 0x2
    BITS_REG_THRESH_LOW_HIGH        = 0x3
    BITS_REG_THRESH_HIGH_LOW        = 0x4
    BITS_REG_THRESH_HIGH_HIGH       = 0x5
    BITS_REG_INTERRUPT              = 0x6
    BITS_REG_ID                     = 0xA
    BITS_REG_DATA0                  = (0xC, 0xD)
    BITS_REG_DATA1                  = (0xE, 0xF)
    
    #   BITS ABOUT CONTROL REGISTER
    BITS_POW_UP                     = 0x03
    BITS_POW_DOWN                   = 0x00
    
    #   BITS ABOUT TIMING REGISTER
    BITS_TIMING_GAIN_HIGH           = 0b00010000
    BITS_TIMING_GAIN_LOW            = 0b00000000
    BITS_TIMING_MANUAL_START        = 0b00001000
    BITS_TIMING_MANUAL_STOP         = 0b00000000
    BITS_TIMING_INTEGRATION_0       = 0b00000000
    BITS_TIMING_INTEGRATION_1       = 0b00000001
    BITS_TIMING_INTEGRATION_2       = 0b00000010
    BITS_TIMING_INTEGRATION_MANUAL  = 0b00000011
    
    #   BITS ABOUT INTERRUPT CONTROL REGISTER
    BITS_INTR_LEVEL_DISABLED        = 0b00000000
    BITS_INTR_LEVEL_ENABLED         = 0b00010000

    #   CONSTANT VALUES ABOUT REGISTORS
    SIZE_BYTES_REG_DATA             = 4
    BITS_TIMING_INTEG_DEFAULT       = BITS_TIMING_INTEGRATION_2
    BITS_THRESHOLD_DEFAULT          = 0x0000
    THRESHOLD_MAX                   = 0xFFFF
    THRESHOLD_MIN                   = 0x0000
    PERSISTENCE_MAX                 = 0xF
    PERSISTENCE_MIN                 = 0x0
    
    ID_ON_DEBUG                     = -1

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   OPTIONS
    #
    #   * Gain
    #       value   |      mode
    #   -----------------------------
    #         0     | high gain mode
    #         1     |  low gain mode
    #
    #   * Manual Timing Control
    #       value   |           feature
    #   -----------------------------------------
    #         0     | stop an integration cycle
    #         1     | begin an integration cycle
    #   NOTE
    #       The Manual Timing Control option will work only when INTEG
    #       is set as 0x11.
    #
    #   * INTEG
    #       value   |  nominal integration time
    #   -----------------------------------------
    #        00     |           13.7 ms
    #        01     |           101  ms
    #        10     |           402  ms
    #        11     |           N/A
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    
    class DataModel(DataModelBase):
        
        def setup(self, illum):
            self._illum = illum
            
        @loggable
        def illuminance(self):
            return self._illum


    def __init__(self,
                 handler: I2CHandlerBase,
                 name: Optional[str] = None) -> None:
        
        if not isinstance(handler, I2CHandlerBase):
            raise HandlerMismatchError(
                "'handler' must be HandlerI2C."
            )
        
        super().__init__(name)
        
        self._handler: Optional[I2CHandlerBase] = handler
        
        self._gain: int = self.BITS_TIMING_GAIN_LOW
        self._manual: int = self.BITS_TIMING_MANUAL_STOP
        self._integ: int = self.BITS_TIMING_INTEG_DEFAULT
        self._id: int = self.ID_ON_DEBUG
        self._threshold_low: int = self.BITS_THRESHOLD_DEFAULT
        self._threshold_high: int = self.BITS_THRESHOLD_DEFAULT
        self._level: int = self.BITS_INTR_LEVEL_DISABLED
        self._persistence: int = 0
        
        # setup device when a HandlerI2C is given.
        self.power_up()
        self._id: int = self._read_id()

    def read(self):
        ch0, ch1 = self._read_raw_data()
        illum = self.calc_illum(ch0, ch1)
        
        model = self.DataModel(self.name)
        model.setup(illum)
        return model
    
    @classmethod
    def calc_illum(cls, ch0, ch1) -> float:
        p = ch1 / ch0
        lux = 0.

        if 0 < p <= 0.5:
            lux = 0.0304 * ch0 - 0.062 * ch0 * math.pow(p, 1.4)
        elif p <= 0.61:
            lux = 0.0224 * ch0 - 0.031 * ch1
        elif p <= 0.80:
            lux = 0.0128 * ch0 - 0.0153 * ch1
        elif p <= 1.30:
            lux = 0.00146 * ch0 - 0.00112 * ch1

        return lux
    
    @property
    def id(self):
        return self._id
    
    def power_up(self):
        self._check_handler()
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_CTRL, 
                            self.BITS_POW_UP)
        
    def power_down(self):
        self._check_handler()
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_CTRL, 
                            self.BITS_POW_DOWN)
        
    def set_timing(self, 
                   highgain: Optional[bool] = None,
                   manual: Optional[bool] = None,
                   integ: Optional[int] = None):
        self._check_handler()
        
        if highgain is not None:
            if isinstance(highgain, bool):
                if highgain:
                    self._gain = self.BITS_TIMING_GAIN_HIGH
                else:
                    self._gain = self.BITS_TIMING_GAIN_LOW
            else:
                raise TypeError(
                    "'highgain' must be bool."
                )
                    
        if manual is not None:
            if isinstance(manual, bool):
                if manual:
                    self._manual = self.BITS_TIMING_MANUAL_START
                else:
                    self._manual = self.BITS_TIMING_MANUAL_STOP
            else:
                raise TypeError(
                    "'manual' must be bool."
                )
                
        if integ is not None:
            if self.BITS_TIMING_INTEGRATION_0 <= integ <= self.BITS_TIMING_INTEGRATION_MANUAL:                        
                self._integ = integ
            else:
                raise ValueError(
                    "'integ' must be int and no less than 0 and no more than 3."
                )
                
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_TIMING,
                            self._gain | self._manual | self._integ)
            
    def start_manual_integ(self):
        self._check_handler()
        self.set_timing(manual=True, integ=self.BITS_TIMING_INTEGRATION_MANUAL)
        
    def stop_manual_integ(self):
        self._check_handler()
        self.set_timing(manual=False, integ=self.BITS_TIMING_INTEGRATION_MANUAL)
        
    def clear_interrupt(self):
        self._handler.read(self.BITS_COMMAND_CMD | self.BITS_COMMAND_CLEAR | self.BITS_REG_ID, 1)
        
    def set_interrupt(self,
                      low: Optional[int] = None,
                      high: Optional[int] = None,
                      islevel: Optional[int] = None,
                      persistence: Optional[int] = None):
        
        if low is not None:
            if self.THRESHOLD_MIN <= low <= self.THRESHOLD_MIN:
                self._threshold_low = low
                lower = low & 0x00FF
                upper = low & 0xFF00
                self._set_threshold_low(lower, upper)
            else:
                raise ValueError(
                    "'low' must be int and in {} ~ {}"
                    .format(self.THRESHOLD_MIN, self.THRESHOLD_MAX)
                )
                
        if high is not None:
            if self.THRESHOLD_MIN <= high <= self.THRESHOLD_MIN:
                self._threshold_high = high
                lower = high & 0x00FF
                upper = high & 0xFF00
                self._set_threshold_high(lower, upper)
            else:
                raise ValueError(
                    "'high' must be int and in {} ~ {}"
                    .format(self.THRESHOLD_MIN, self.THRESHOLD_MAX)
                )
                
        if islevel is not None:
            if isinstance(islevel, bool):
                if islevel:
                    self._level = self.BITS_INTR_LEVEL_ENABLED
                else:
                    self._level = self.BITS_INTR_LEVEL_DISABLED
            else:
                raise TypeError(
                    "'islevel' must be bool."
                )
                
        if persistence is not None:
            if self.PERSISTENCE_MIN <= persistence <= self.PERSISTENCE_MAX:
                self._persistence = persistence
            else:
                raise ValueError(
                    "'persistance' must be int and in {} ~ {}"
                    .format(self.PERSISTENCE_MIN, self.PERSISTENCE_MAX)
                )
                
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_INTERRUPT,
                            self._level | self._persistence)
        
    def _check_handler(self):
        if self._handler is None:
            raise HandlerNotSetError(
                "A hanlder must be set for executing this method."
            )

    def _read_raw_data(self) -> Tuple[int]:
        _, raw = self._handler.read(self.BITS_COMMAND_CMD | self.BITS_REG_DATA0[0], 
                                    self.SIZE_BYTES_REG_DATA)
        return (raw[1] << 8 | raw[0], raw[3] << 8 | raw[2])

    def _read_id(self) -> int:
        _, raw = self._handler.read(self.BITS_COMMAND_CMD | self.BITS_REG_ID, 1)
        return raw[0]

    def _set_threshold_low(self, lower: int, upper: int):
        self._check_handler()
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_THRESH_LOW_LOW, lower)
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_THRESH_LOW_HIGH, upper)
    
    def _set_threshold_high(self, lower: int, upper: int):
        self._check_handler()
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_THRESH_HIGH_LOW, lower)
        self._handler.write(self.BITS_COMMAND_CMD | self.BITS_REG_THRESH_HIGH_HIGH, upper)
