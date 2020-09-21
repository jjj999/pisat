
from time import sleep, time

from pisat.handler import PyserialSerialHandler
from pisat.comm.transceiver import Im920
from pisat.comm.transceiver import SocketTransceiver


handler1 = PyserialSerialHandler("/dev/ttyUSB0", baudrate=19200)
handler2 = PyserialSerialHandler("/dev/ttyUSB1", baudrate=19200)

im920_1 = Im920(handler1, name="im920_1")
im920_2 = Im920(handler2, name="im920_2")

address_1 = ("1CD2", "0", "0")
address_2 = ("37B6", "0", "0")

socket_transceiver_1 = SocketTransceiver(im920_1)
socket_transceiver_2 = SocketTransceiver(im920_2)

socket_1 = socket_transceiver_1.create_socket(address_1)
socket_2 = socket_transceiver_2.create_socket(address_2)

socket_transceiver_1.observe()
socket_transceiver_2.observe()

socket_1.send(im920_1.encode("Hello World " * 10))

init = time()
while True:
    if time() - init > 10:
        break
    data = socket_2.recv(16)
    if not len(data):
        continue
    
    print(im920_2.decode(data))

    
print("break")
socket_transceiver_1.stop_observe()
socket_transceiver_2.stop_observe()
