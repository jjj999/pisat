#! python3

"""

pisat.config.dname
~~~~~~~~~~~~~~~~~~
The module in which data names for the pisat system are defined. 
The data names defined in the module are used for the pisat system, 
especially DataLogger and SensorController. Thus, this module 
is for a guarantee of consistency of data names. The data names are 
same as those are used in sensors and adapters.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.sensor
pisat.adapter
pisat.core.logger.SensorController
"""

# ACCELERATION
ACCELERATION_X                      = "ACCELERATION_X"
ACCELERATION_Y                      = "ACCELERATION_Y"
ACCELERATION_Z                      = "ACCELERATION_Z"

# VELOCITY
VELOCITY_X                          = "VELOCITY_X"
VELOCITY_Y                          = "VELOCITY_Y"
VELOCITY_Z                          = "VELOCITY_Z"

# GYRO
GYRO_ROLL                           = "GYRO_ROLL"
GYRO_PITCH                          = "GYRO_PITCH"
GYRO_YAW                            = "GYRO_YAW"
GYRO_X                              = "GYRO_X"
GYRO_Y                              = "GYRO_Y"
GYRO_Z                              = "GYRO_Z"

# GEOMAGNETISM
GEOMAGNETISM_ROLL                   = "GEOMAGNETISM_ROLL"
GEOMAGNETISM_PITCH                  = "GEOMAGNETISM_PITCH"
GEOMAGNETISM_YAW                    = "GEOMAGNETISM_YAW"
GEOMAGNETISM_X                      = "GEOMAGNETISM_X"
GEOMAGNETISM_Y                      = "GEOMAGNETISM_Y"
GEOMAGNETISM_Z                      = "GEOMAGNETISM_Z"

# POSITION
ALTITUDE_SEALEVEL                   = "ALTITUDE_SEALEVEL"
ALTITUDE_GEOID                      = "ALTITUDE_GEOID"
DISTANCE                            = "DISTANCE"
RELATIVE_COORDINATE_X               = "RELATIVE_COORDINATE_X"
RELATIVE_COORDINATE_Y               = "RELATIVE_COORDINATE_Y"
RELATIVE_COORDINATE_Z               = "RELATIVE_COORDINATE_Z"
ANGLE_RADIAN_FROM_NORTH_POLE        = "ANGLE_RADIAN_FROM_NORTH_POLE"
ANGLE_RADIAN_FROM_SOUTH_POLE        = "ANGLE_RADIAN_FROM_SOUTH_POLE"

# MACROSCOPIC STATE VALUE
PRESSURE                            = "PRESSURE"
TEMPERATURE                         = "TEMP"
HUMMIDITY                           = "HUMIDITY"
ILLUMINANCE                         = "ILLUMINANCE"

# GPS DATA
GPS_TIME_UTC                        = "GPS_TIME_UTC"
GPS_DATE_UTC                        = "GPS_DATE_UTC"
GPS_STATUS                          = "GPS_STATUS"
GPS_LONGITUDE                       = "GPS_LONGITUDE"
GPS_LONGITUDE_RADIAN                = "GPS_LONGITUDE_RADIAN"
GPS_LONGITUDE_DEGREE                = "GPS_LONGITUDE_DEGREE"
GPS_LONGITUDE_MINUITE               = "GPS_LONGITUDE_MINUITE"
GPS_LONGITUDE_EW                    = "GPS_LONGITUDE_EW"
GPS_LATITUDE                        = "GPS_LATITUDE"
GPS_LATITUDE_RADIAN                 = "GPS_LATITUDE_RADIAN"
GPS_LATITUDE_DEGREE                 = "GPS_LATITUDE_DEGREE"
GPS_LATITUDE_MINUITE                = "GPS_LATITUDE_MINUITE"
GPS_LATITUDE_NS                     = "GPS_LATITUDE_NS"
GPS_BODY_VELOCITY_KNOT              = "GPS_BODY_VELOCITY_KNOT"
GPS_BODY_VELOCITY_KM                = "GPS_BODY_VELOCITY_KM"
GPS_BODY_TRUE_ANGLE_VELOCITY        = "GPS_BODY_TRUE_ANGLE_VELOCITY"
GPS_BODY_MAGNETIC_ANGLE_VELOCITY    = "GPS_BODY_MAGNETIC_ANGLE_VELOCITY"
GPS_DIFF_ANGLE_TWONORTH             = "GPS_DIFF_ANGLE_TWONORTH"
GPS_ANGLE_TWONORTH_EW               = "GPS_ANGLE_TWONORTH_EW"
GPS_MODE                            = "GPS_MODE"
GPS_CHECK_SUM                       = "GPS_CHECK_SUM"
GPS_ALTITUDE_SEALEVEL               = "GPS_ALTITUDE_SEALEVEL"
GPS_ALTITUDE_SEALEVEL_UNIT          = "GPS_ALTITUDE_SEALEVEL_UNIT"
GPS_ALTITUDE_GEOID                  = "GPS_ALTITUDE_GEOID"
GPS_ALTITUDE_GEOID_UNIT             = "GPS_ALTITUDE_GEOID_UNIT"
GPS_TIME_FROM_LATEST_DGPS           = "GPS_TIME_FROM_LATEST_DGPS"
GPS_ID_DIFF_POINT                   = "GPS_ID_DIFF_POINT"
GPS_TYPE_DETECT                     = "GPS_TYPE_DETECT"
GPS_NUM_SATELLITES                  = "GPS_NUM_SATELLITE"
GPS_NUMBER_SATELLITE                = "GPS_NUMBER_SATELLITE"
GPS_QUALITY_POSITION                = "QUALITY_POSITION"
GPS_RATE_DECLINE_QUALITY_POSITION   = "GPS_RATE_DECLINE_QUALITY_POSITION"
GPS_RATE_DECLINE_QUALITY_HORIZONTAL = "GPS_RATE_DECLINE_QUALITY_HORIZONTAL"
GPS_RATE_DECLINE_QUALITY_VERTICAL   = "GPS_RATE_DECLINE_QUALITY_VERTICAL"
GPS_NUM_SENTENCES_GSV               = "GPS_NUMS_SENTENCES_GSV"
GPS_NUM_THIS_SENTENCE_GSV           = "GPS_NUM_THIS_SENTENCE_GSV"
GPS_NUMBER_THIS_SATELLITE           = "GPS_NUMBER_THIS_SATELLITE"
GPS_NUM_SATELLITES_IN_VIEW          = "GPS_NUM_SATELLITES_IN_VIEW"
GPS_ANGLE_ELEVATION_SATTELITE       = "GPS_ANGLE_ELEVATION_SATTELITE"
GPS_ANGLE_AZIMUTH_SATTELITE         = "GPS_ANGLE_AZIMUTH_SATTELITE"
GPS_RATIO_CARRIER_NOISE             = "GPS_RATIO_CARRIER_NOISE"
