
from collections import deque
from pisat.comm.transceiver.comm_stream import CommBytesStream
from threading import Thread
from time import sleep

from pisat.handler import PyserialSerialHandler
from pisat.comm.transceiver import Im920
from pisat.comm.transceiver import SocketTransceiver


def test_non_socket():
    
    handler1 = PyserialSerialHandler("/dev/ttyUSB0", baudrate=19200)
    handler2 = PyserialSerialHandler("/dev/ttyUSB1", baudrate=19200)

    im920_1 = Im920(handler1, name="im920_1")
    im920_2 = Im920(handler2, name="im920_2")
    im920_1.clear_buf()
    im920_2.clear_buf()
    
    def main_1():
        for _ in range(10):
            im920_1.send_raw(None, im920_1.encode("Hello World "))
            sleep(0.2)

    def main_2():
        que = deque()
        for _ in range(10):
            raw = im920_2.recv_raw()
            sleep(0.2)
            if not len(raw):
                continue
            que.append(raw[1])
        
        stream = CommBytesStream()
        for d in que:
            stream.add(d)
            
        while True:
            data = stream.pop(32)
            if len(data):
                print(im920_1.decode(data))
            else:
                break
            
    thread_1 = Thread(target=main_1)
    thread_2 = Thread(target=main_2)

    thread_1.start()
    thread_2.start()
    

def test_socket():
    handler1 = PyserialSerialHandler("/dev/ttyUSB0", baudrate=19200)
    handler2 = PyserialSerialHandler("/dev/ttyUSB1", baudrate=19200)

    im920_1 = Im920(handler1, name="im920_1")
    im920_2 = Im920(handler2, name="im920_2")
    im920_1.clear_buf()
    im920_2.clear_buf()
    
    address_1 = ("37B6", )
    address_2 = ("1CD2", )
    
    transceiver_1 = SocketTransceiver(im920_1)
    transceiver_2 = SocketTransceiver(im920_2)
    
    socket_1 = transceiver_1.create_socket(address_2)
    socket_2 = transceiver_2.create_socket(address_1)
    
    socket_1.send(im920_1.encode("Hello World " * 100))
    transceiver_1.flush(period=0.1, certain=True)
    
    count = 0
    while True:
        transceiver_2.load()
        data = socket_2.recv(256)
        if len(data):
            print("data: {} , len: {}".format(im920_1.decode(data), len(data)))
        else:
            count += 1
            if count > 5:
                break
            
            
def test_socket_nonblock():
    
    handler1 = PyserialSerialHandler("/dev/ttyUSB0", baudrate=19200)
    handler2 = PyserialSerialHandler("/dev/ttyUSB1", baudrate=19200)

    im920_1 = Im920(handler1, name="im920_1")
    im920_2 = Im920(handler2, name="im920_2")
    im920_1.clear_buf()
    im920_2.clear_buf()
    
    address_1 = ("37B6", )
    address_2 = ("1CD2", )
    
    transceiver_1 = SocketTransceiver(im920_1, period=0.1)
    transceiver_2 = SocketTransceiver(im920_2, period=0.1)
    
    socket_1 = transceiver_1.create_socket(address_2)
    socket_2 = transceiver_2.create_socket(address_1)
    
    for _ in range(10):
        socket_1.send(im920_1.encode("Hello World " * 10))
    socket_1.send(im920_1.encode("Hello World " * 10))
    
    count = 0
    while True:
        data = socket_2.recv(256)
        if len(data):
            print("data: {} , len: {}".format(im920_1.decode(data), len(data)))
        else:
            count += 1
            if count > 5:
                break
    
            
def test_socket_sender():
    handler = PyserialSerialHandler("/dev/ttyUSB0", baudrate=19200)

    im920 = Im920(handler, name="im920")
    im920.clear_buf()
    
    address = ("1CD2", )
    
    transceiver = SocketTransceiver(im920, period=0.1)
    socket = transceiver.create_socket(address)
    
    for _ in range(1):
        socket.send_later(im920.encode("Hello Taiki " * 10))
    socket.flush()
    
    
def test_socket_recver():
    
    handler = PyserialSerialHandler("/dev/ttyUSB0", baudrate=19200)

    im920 = Im920(handler, name="im920")
    im920.clear_buf()
    
    address = ("37B6", )
    
    transceiver = SocketTransceiver(im920, period=0.1)
    socket = transceiver.create_socket(address)
    sleep(10)
    
    count = 0
    while True:
        data = socket.recv(256)
        if len(data):
            print("data: {} , len: {}".format(im920.decode(data), len(data)))
        else:
            count += 1
            if count > 5:
                break
                    
    
if __name__ == "__main__":
    test_socket_sender()
