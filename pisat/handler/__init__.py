
from pisat.util.platform import is_raspberry_pi

from pisat.handler.handler_base import HandlerBase
from pisat.handler.digital_io_handler_base import DigitalIOHandlerBase
from pisat.handler.digital_input_handler_base import DigitalInputHandlerBase
from pisat.handler.digital_output_handler_base import DigitalOutputHandlerBase
from pisat.handler.pwm_handler_base import PWMHandlerBase
from pisat.handler.i2c_handler_base import I2CHandlerBase
from pisat.handler.spi_handler_base import SPIHandlerBase
from pisat.handler.serial_handler_base import SerialHandlerBase

from pisat.handler.handler_base import DataBrokenError


if is_raspberry_pi():
    from pisat.handler.pigpio_digital_input_handler import PigpioDigitalInputHandler
    from pisat.handler.pigpio_digital_output_handler import PigpioDigitalOutputHandler
    from pisat.handler.pigpio_pwm_handler import PigpioPWMHandler
    from pisat.handler.pigpio_i2c_handler import PigpioI2CHandler
    from pisat.handler.pigpio_spi_handler import PigpioSPIHandler
    from pisat.handler.pigpio_serial_handler import PigpioSerialHandler

    from pisat.handler.rpigpio_digital_input_handler import RpiGpioDigitalInputHandler
    from pisat.handler.rpigpio_digital_output_handler import RpiGpioDigitalOutputHandler
    from pisat.handler.rpigpio_pwm_handler import RpiGpioPWMHandler

from pisat.handler.pyserial_serial_handler import PyserialSerialHandler
