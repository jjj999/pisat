#! python3

"""

pisat.config.type
~~~~~~~~~~~~~~~~~
The module in which types for the pisat system are defined. 

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.sensor
pisat.adapter
pisat.core.logger.SensorController
"""

from typing import Tuple, Union


# Logable means this type of object can be logged by DataLogger.
# A subject to be logged and saved into a log file must be
# Logable type.
Logable = Union[int, float, str]

# This type is for addresses of TransceiverBase and its subclasses.
TypeAddress = Tuple[Union[int, str]]
