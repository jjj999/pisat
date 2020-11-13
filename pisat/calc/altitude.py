
import math


PRESS_ATOMOSPHERE = 1013.25         # hpa
TEMP_ABS_CELSIUS0 = 273.15           # K


def press2alti(press: float, temp: float) -> float:
    dep_p = math.pow(PRESS_ATOMOSPHERE / press, 1. / 5.257) - 1
    dep_t = temp + TEMP_ABS_CELSIUS0
    return dep_p * dep_t / 0.0065
    