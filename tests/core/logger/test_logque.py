from memory_profiler import profile
import csv
import time

from collections import deque
from pisat.core.logger import LogQueue


path_data = "../../../data/test.csv"
data = deque()

def get_data():
    with open(path_data, "rt") as f:
        dnames = list(f.readline()[:-2].split(","))
        f.readline()
        
        while True:
            line = f.readline()
            if not line:
                break
            
            data.append([float(d) for d in line.split(",")])
            
    data2 = deque()
    for _ in range(100):
        data2.extend(data)
        
    data3 = deque()
    for line in data2:
        data3.appendleft({dname: val for dname, val in zip(dnames, line)})
        
    return data3, dnames
        
@profile
def main1():
    
    data, dnames = get_data()
    data3 = deque()
    
    while True:
        try:
            d = data.popleft()
            data3.append(d)
        except IndexError:
            break
        
    with open("hoge.csv", "wt") as f:
        write = csv.DictWriter(f, data3[1].keys())
        while len(data3) > 0:
            write.writerow(data3.popleft())

@profile        
def main2():
    
    data, dnames = get_data()
    
    with LogQueue(100, dnames=dnames) as que:
        while True:
            try:
                que.append(data.popleft())
            except IndexError:
                break

            
init = time.time()
main2()
time2 = time.time() - init

print("time of main2: {} sec".format(time2))