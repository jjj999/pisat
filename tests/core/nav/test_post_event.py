
import threading
import time

from pisat.core.nav import PostEvent


pevent = PostEvent()

def test():
    print("start thread")
    while not pevent.wait(2):
        print("waiting...")
    print(pevent.package)
    print("close thread")
    
thread = threading.Thread(target=test)
thread.start()
time.sleep(5)
print("event occured")
pevent.set("good")