#! python3
#
#
#
#
#

from pisat.comm.codecs import CodecIm920
from pisat.comm.devices import Im920

class CommIm920(Im920, CodecIm920):

    def __init__(self, serial_port:str, tags:tuple, 
                baudrate=19200, timeout_read=1.0, timeout_write=1.0, packet=64):

        Im920.__init__(self, serial_port, baudrate=baudrate, timeout_read=timeout_read, timeout_write=timeout_write)
        CodecIm920.__init__(self, tags=tags, packet=packet)

    def send_formatted(self, flag:str, tag_data:dict):
        self.send(self.encoder(flag, tag_data))

    def send_request(self, num_data):
        self.send(CodecIm920.REQUEST_FLAG + str(num_data))

    def receive_formatted(self):

        try:
            data_received = self.receive()
            flag, data_decoded = self.decoder(data_received[3])

            data_received[3] = flag

            if flag == CodecIm920.REQUEST_FLAG:
                data_received.append(data_decoded)
            
            else:
                data_received.append(self.formater(data_decoded))

            return data_received

        except IndexError:
            return []