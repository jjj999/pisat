

from pisat.util.nmea import NMEAParser


parser = NMEAParser("parser")

f = open("res/satellites_raw.txt", "rb")

try:
    while True:
        input()
        raw = f.readline()
        data = parser.parse(raw)
        
        if data is None:
            print(f"Format: None")
        else:
            print(f"Format: {data.FORMAT}")
            print(data.extract())
            
        print(f"Sentence: {raw}", end="\n\n")
except KeyboardInterrupt:
    f.close()
