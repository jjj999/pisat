

from time import sleep

from pisat.sensor.handler import HandlerSerial
from pisat.sensor.sensor import Gyfsdmaxb


def readf_seq(gps, count):
    for _ in range(count):
        sleep(0.2)
        print("data:", gps.readf())

def read_seq(gps, count):
    for _ in range(count):
        print("data:", gps.read())


if __name__ == "__main__":
    handler = HandlerSerial()
    gps = Gyfsdmaxb(handler)

    readf_seq(gps, 100)

