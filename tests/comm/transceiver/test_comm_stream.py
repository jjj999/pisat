
from pisat.comm.transceiver.comm_stream import CommBytesStream


stream = CommBytesStream()
for _ in range(10):
    stream.add(b"hello" * 5)

for _ in range(20):
    print(stream.pop(50))

print(len(stream))