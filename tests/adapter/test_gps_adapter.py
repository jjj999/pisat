
from math import radians

import pisat.config.dname as dname
from pisat.adapter.gps_adapter import GpsAdapter
from pisat.config.dname import GPS_LATITUDE, GPS_LATITUDE_NS


data = {dname.GPS_LONGITUDE: 179,
        dname.GPS_LONGITUDE_EW: "E",
        dname.GPS_LATITUDE: 35,
        dname.GPS_LATITUDE_NS: "N"}

adapter = GpsAdapter((radians(-179), radians(35)))
print(adapter.calc(data))