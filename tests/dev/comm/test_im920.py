
from threading import Thread
from time import sleep

from pisat.handler import PyserialSerialHandler
from pisat.comm.transceiver import Im920


handler1 = PyserialSerialHandler("/dev/ttyUSB0", baudrate=19200)
handler2 = PyserialSerialHandler("/dev/ttyUSB1", baudrate=19200)

im920_1 = Im920(handler1, name="im920_1")
im920_2 = Im920(handler2, name="im920_2")


def main_1():
    for _ in range(10):
        im920_1.send_raw(None, im920_1.encode("hello"))
        sleep(0.2)

def main_2():
    for _ in range(10):
        raw = im920_2.recv_raw()
        sleep(0.2)
        if not len(raw):
            continue
        print(raw[1])
        
thread_1 = Thread(target=main_1)
thread_2 = Thread(target=main_2)

thread_1.start()
thread_2.start()
