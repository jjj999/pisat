#! python3

"""

pisat.logger.sensors.handler_base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.
"""

from pisat.base.component import Component


class DataBrokenError(Exception):
    """Raised if data is broken."""
    pass

class HandlerBase(Component):
    pass
