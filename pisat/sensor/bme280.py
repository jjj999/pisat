#! python3

"""

pisat.sensor.sensor.bme280
~~~~~~~~~~~~~~~~~~~~~~~~~~
Sensor class of BME280 compatible with the pisat system.
This module works completely, regardless of whether using the pisat system or not.

[info]
BME280 datasheet
    https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf

TODO    docstring
"""

from typing import Optional, Tuple, Union

from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.handler.spi_handler_base import SPIHandlerBase
from pisat.model.datamodel import loggable, DataModelBase
from pisat.sensor.sensor_base import HandlerMismatchError
from pisat.sensor.sensor_base import SensorBase


class Bme280(SensorBase):

    """Sensor class of BME280.

    An object of the class comletely works, regardless of wheter using the pisat system or not.
    This class is implemented as a subclass of the SensorAdditional class.
    """

    #   I2C ADDRESS
    ADDRESS_I2C_GND         = 0x76
    ADDRESS_I2C_VDD         = 0x77

    #   RESISTOR ADDRESS
    REG_ID                  = 0xD0
    REG_RESET               = 0xE0
    REG_CTRL_HUM            = 0xF2
    REG_STATUS              = 0xF3
    REG_CTRL_MEAS           = 0xF4
    REG_CONFIG              = 0xF5
    REG_CALIB_PARAMS        = tuple([0x88 + i for i in range(24)]) + \
                                (0xA1,) + tuple([0xE1 + i for i in range(7)])
    REG_PRESS               = (0xF7, 0xF8, 0xF9)
    REG_TEMP                = (0xFA, 0xFB, 0xFC)
    REG_HUM                 = (0xFD, 0xFE)

    #   CONSISTANT VALUE ABOUT REGISTORS
    SIZE_BYTES_REG_DATA     = 8
    VALUE_RESET             = 0xB6
    
    OPTION_OSRS_P_DEFAILT   = 0b101
    OPTION_OSRS_T_DEFAILT   = 0b101
    OPTION_OSRS_H_DEFAILT   = 0b101
    OPTION_MODE_DEFAILT     = 0b11
    OPTION_T_SB_DEFAILT     = 0b000
    OPTION_FILTER_DEFAILT   = 0b100
    OPTION_SPI3W_EN_DEFAILT = 0b0

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   OPTIONS
    #
    #   * osrs_p, osrs_t, osrs_h
    #       value   |   oversampling
    #   ---------------------------------
    #       000     |   sampling skipped
    #       001     |   oversampling * 1
    #       010     |   oversampling * 2
    #       011     |   oversampling * 4
    #       100     |   oversampling * 8
    #   101, others |   oversampling * 16
    #
    #   * mode
    #       value   |   mode
    #   ----------------------------
    #        00     |   Sleep mode
    #      01, 10   |   Forced mode
    #        11     |   Normal mode
    #
    #   * t_sb
    #       value   |   t_{standby} [ms]
    #   --------------------------------
    #        000    |       0.5
    #        001    |       62.5
    #        010    |       125
    #        011    |       250
    #        100    |       500
    #        101    |       1000
    #        110    |       10
    #        111    |       20
    #
    #   * filter
    #       value   |   filter coefficient
    #   ---------------------------------------
    #        000    |   filter off
    #        001    |       2
    #        010    |       4
    #        011    |       8
    #   100, others |       16
    #
    #   * spi3w_en
    #   Enables 3-wire SPI interface when set to 1 (0b1).
    #   When set to 0 (0b0), enables 4-wire one.
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    class DataModel(DataModelBase):
        
        def setup(self, press: float, temp: float, hum: float):
            self._press = press
            self._temp = temp
            self._hum = hum
        
        @loggable
        def press(self):
            return self._press
        
        @loggable
        def temp(self):
            return self._temp
        
        @loggable
        def hum(self):
            return self._hum
            
            
    def __init__(self,
                 handler: Union[I2CHandlerBase, SPIHandlerBase],
                 name: Optional[str] = None,
                 osrs_p=0b101,
                 osrs_t=0b101,
                 osrs_h=0b101,
                 mode=0b11,
                 t_sb=0b000,
                 m_filter=0b100,
                 spi3w_en=0b0):

        super().__init__(handler, name=name)

        self._temp_fine: int = 0
        self._dig_temp: tuple = None
        self._dig_press: tuple = None
        self._dig_hum: tuple = None

        self._chip_id: int = 0
        self._status_measuring: int = 0
        self._status_im_update: int = 0
        self._osrs_p: int = osrs_p
        self._osrs_t: int = osrs_t
        self._osrs_h: int = osrs_h
        self._mode: int = mode
        self._t_sb: int = t_sb
        self._m_filter: int = m_filter
        self._spi3w_en: int = spi3w_en

        if not isinstance(handler, (I2CHandlerBase, SPIHandlerBase)):
            raise HandlerMismatchError(
                "Given handler object is not supported in the class.")

        # read device-unique properties
        self._chip_id = self._read_id()
        self._status_measuring, self._status_im_update = self._read_status()

        # write options
        if self._parse_options(osrs_p, osrs_t, osrs_h, mode, t_sb, m_filter, spi3w_en):
            self._write_ctrl_hum(self._osrs_h)
            self._write_ctrl_meas(self._osrs_t, self._osrs_p, self._mode)
            self._write_config(self._t_sb, self._m_filter, self._spi3w_en)
        else:
            raise ValueError(
                "Given Arguments include not supported values. Check the datasheet.")

        # get calibration params and setup temp_fine
        self._dig_temp, self._dig_press, self._dig_hum = \
            Bme280.parse_calib_params(self._read_calib_params())
        _ = self.read_temp
        _ = self.read()

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   PROPERTIES
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    @property
    def dnames(self):
        return Bme280.DATA_NAMES

    @property
    def id(self):
        return self._chip_id

    @property
    def measuring(self):
        return self._status_measuring

    @property
    def im_update(self):
        return self._status_im_update

    @property
    def osrs_p(self):
        return self._osrs_p

    @property
    def osrs_t(self):
        return self._osrs_t

    @property
    def osrs_h(self):
        return self._osrs_h

    @property
    def mode(self):
        return self._mode

    @property
    def t_sb(self):
        return self._t_sb

    @property
    def filter(self):
        return self._m_filter

    @property
    def spi3w_en(self):
        return self._spi3w_en

    @property
    def dig_temp(self):
        return self._dig_temp

    @property
    def dig_press(self):
        return self._dig_press

    @property
    def dig_hum(self):
        return self._dig_hum

    def read(self):
        raw_press, raw_temp, raw_hum = self._read_raw_data()
        press = self.calc_press(raw_press)
        temp = self.calc_temp(raw_temp)
        hum = self.calc_hum(raw_hum)
        
        model = self.DataModel(self.name)
        model.setup(press, temp, hum)
        return model

    def set_options(self,
                    osrs_p=None,
                    osrs_t=None,
                    osrs_h=None,
                    mode=None,
                    t_sb=None,
                    m_filter=None,
                    spi3w_en=None) -> None:

        if osrs_h is not None and self._parse_options(osrs_h=osrs_h):
            self._osrs_h = osrs_h
            self._write_ctrl_hum(self._osrs_h)

        if [osrs_t, osrs_p, mode].count(None) < 3 \
                and self._parse_options(osrs_t=osrs_t, osrs_p=osrs_p, mode=mode):
            if osrs_t is not None:
                self._osrs_t = osrs_t
            if osrs_p is not None:
                self._osrs_p = osrs_p
            if mode is not None:
                self._mode = mode
            self._write_ctrl_meas(self._osrs_t, self._osrs_p, self._mode)

        if [t_sb, m_filter, spi3w_en].count(None) < 3 \
                and self._parse_options(t_sb=t_sb, m_filter=m_filter, spi3w_en=spi3w_en):
            if t_sb is not None:
                self._t_sb = t_sb
            if m_filter is not None:
                self._m_filter = m_filter
            if spi3w_en is not None:
                self._spi3w_en = spi3w_en
            self._write_config(self._t_sb, self._m_filter, self._spi3w_en)

    @classmethod
    def parse_calib_params(cls, params) -> Tuple[tuple]:

        # params index
        #  0 ~ 23 : 0x88 ~ 0x9F
        #    24   : 0xA1
        # 25 ~ 31 : 0xE1 ~ 0xE7
        dig_temp = [params[i + 1] << 8 | params[i] for i in range(0, 5, 2)]
        dig_press = [params[i + 1] << 8 | params[i] for i in range(6, 24, 2)]
        dig_hum = [params[24],
                   params[26] << 8 | params[25],
                   params[27],
                   params[28] << 4 | params[29] & 0b00001111,
                   params[30] << 4 | (params[29] & 0b11110000) >> 4,
                   params[31]]

        # Convert signed number if required.
        # See the datasheet p24.
        #
        # dig index
        # digT : 0 ~ 2
        # digP : 0 ~ 8
        # digH : 0 ~ 5
        for i, val in enumerate(dig_temp):
            if i in (1, 2) and val & 0x8000:
                dig_temp[i] = (- val ^ 0xFFFF) + 1

        for i, val in enumerate(dig_press):
            if i in (1, 2, 3, 4, 5, 6, 7, 8) and val & 0x8000:
                dig_press[i] = (- val ^ 0xFFFF) + 1

        for i, val in enumerate(dig_hum):

            # 16 bits
            if i in (1, ) and val & 0x8000:
                dig_hum[i] = (- val ^ 0xFFFF) + 1

            # 12 bits
            elif i in (3, 4) and val & 0x800:
                dig_hum[i] = (- val ^ 0xFFF) + 1

            # 8 bits
            elif i in (5, ) and val & 0x80:
                dig_hum[i] = (- val ^ 0xFF) + 1

        return tuple(dig_temp), tuple(dig_press), tuple(dig_hum)

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   Read Compensated Values
    #
    #   NOTE
    #   *   If wants information about the calculation, see the datasheet p25 ~ p26.
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    # [deg C]
    def calc_temp(self, raw: int) -> float:
        var1 = ((raw / 8 - self._dig_temp[0] * 2) * self._dig_temp[1]) / 2048
        var2 = (raw / 16 - self._dig_temp[0]
                ) ** 2 * self._dig_temp[2] / 67108864
        self._temp_fine = int(var1 + var2)

        return ((var1 + var2) * 5 + 128) / 25600

    # [hPa]
    def calc_press(self, raw: int) -> float:
        var1 = self._temp_fine - 128000
        var2 = var1 ** 2 * self._dig_press[5] \
            + ((var1 * self._dig_press[4]) << 17) \
            + (self._dig_press[3] << 35)
        var1 = (((var1 ** 2 * self._dig_press[2]) >> 8)
                + ((var1 * self._dig_press[1]) << 12))
        var1 = (((1 << 47) + var1) * self._dig_press[0]) >> 33

        if var1 == 0:
            return 0.       # CAUTION
        else:
            p = 1048576 - raw
            p = (((p << 31) - var2) * 3125) // var1
            var1 = (self._dig_press[8] * (p >> 13) ** 2) >> 25
            var2 = (self._dig_press[7] * p) >> 19
            return ((p + var1 + var2) / 256 + (self._dig_press[6] * 16.0)) / 25600

    # [%]
    def calc_hum(self, raw: int) -> float:
        h = self._temp_fine - 76800
        h = (((((raw << 14) - (self._dig_hum[3] << 20) - self._dig_hum[4] * h) + 16384) >> 15)
             * ((((((h * self._dig_hum[5] >> 10) * ((h * self._dig_hum[2] >> 11) + 32768)) >> 10) + 2097152)
                 * self._dig_hum[1] + 8192) >> 14))
        h = h - ((((h >> 15) * (h >> 15)) >> 7) * self._dig_hum[0] >> 4)

        h = 0 if h < 0 else h
        h = 419430400 if h > 419430400 else h
        return h / 4194304

    def _read_calib_params(self) -> bytearray:
        return self._handler.read_seq_byte(*Bme280.REG_CALIB_PARAMS)

    def _byte2int_press_temp(self, b0, b1, b2) -> int:
        return b0 << 12 | b1 << 4 | b2 >> 4

    def _byte2int_hum(self, b0, b1) -> int:
        return b0 << 8 | b1

    def _read_raw_data(self) -> Tuple[int]:
        count, raw = self._handler.read(
            Bme280.REG_PRESS[0], Bme280.SIZE_BYTES_REG_DATA)
        if count == Bme280.SIZE_BYTES_REG_DATA:
            return (self._byte2int_press_temp(raw[0], raw[1], raw[2]),
                    self._byte2int_press_temp(raw[3], raw[4], raw[5]),
                    self._byte2int_hum(raw[6], raw[7]))

    def _read_raw_press(self) -> int:
        raw = self._handler.read_seq_byte(*Bme280.REG_PRESS)
        return self._byte2int_press_temp(raw[0], raw[1], raw[2])

    def _read_raw_temp(self) -> int:
        raw = self._handler.read_seq_byte(*Bme280.REG_TEMP)
        return self._byte2int_press_temp(raw[0], raw[1], raw[2])

    def _read_raw_hum(self) -> int:
        raw = self._handler.read_seq_byte(*Bme280.REG_HUM)
        return self._byte2int_hum(raw[0], raw[1])

    # chip_id

    def _read_id(self) -> int:
        return self._handler.read_seq_byte(Bme280.REG_ID)[0]

    # osrs_h

    def _read_ctrl_hum(self) -> int:
        raw = self._handler.read_seq_byte(Bme280.REG_CTRL_HUM)[0]
        return raw & 0b00000111

    # measuring, im_update

    def _read_status(self) -> Tuple[int]:
        raw = self._handler.read_seq_byte(Bme280.REG_STATUS)[0]
        return (raw & 0b00001000) >> 3, raw & 0b00000001

    # osrs_t, osrt_p, mode

    def _read_ctrl_meas(self) -> Tuple[int]:
        raw = self._handler.read_seq_byte(Bme280.REG_CTRL_MEAS)[0]
        return (raw & 0b11100000) >> 5, (raw & 0b00011100) >> 2, raw & 0b00000011

    # t_sb, filter, spi3w_en

    def _read_config(self) -> bytearray:
        raw = self._handler.read_seq_byte(Bme280.REG_CONFIG)[0]
        return (raw & 0b11100000) >> 5, (raw & 0b00011100) >> 2, raw & 0b00000001

    def _write_reset(self) -> None:
        self._handler.write(Bme280.REG_RESET, Bme280.VALUE_RESET)

    def _write_ctrl_hum(self, osrs_h: int) -> None:
        self._handler.write(Bme280.REG_CTRL_HUM, osrs_h)

    def _write_ctrl_meas(self, osrs_t: int, osrs_p: int, mode: int) -> None:
        self._handler.write(Bme280.REG_CTRL_MEAS, osrs_t <<
                            5 | osrs_p << 2 | mode)

    def _write_config(self, t_sb: int, m_filter: int, spi3w_en: int) -> None:
        self._handler.write(Bme280.REG_CONFIG, t_sb <<
                            5 | m_filter << 2 | spi3w_en)

    def _parse_options(self,
                       osrs_p=None,
                       osrs_t=None,
                       osrs_h=None,
                       mode=None,
                       t_sb=None,
                       m_filter=None,
                       spi3w_en=None) -> bool:

        def parse_x_bits(x, d):
            if x is None:
                return True
            else:
                if 0 <= x <= 2 ** d - 1:
                    return True
                else:
                    return False

        # parsing the arguments' bits using the function above
        if not parse_x_bits(osrs_p, 3):
            return False
        if not parse_x_bits(osrs_t, 3):
            return False
        if not parse_x_bits(osrs_h, 3):
            return False
        if not parse_x_bits(mode, 2):
            return False
        if not parse_x_bits(t_sb, 3):
            return False
        if not parse_x_bits(m_filter, 3):
            return False
        if not parse_x_bits(spi3w_en, 1):
            return False

        return True
    