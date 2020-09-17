
from typing import Dict, Any
from pprint import pprint

from pisat.core.nav import Node
from pisat.core.nav import Context
import pisat.sensor.const as const
from pisat.sensor.sensor import Bme280


bme280 = Bme280(debug=True)

class TestNode1(Node):
    
    def enter(self):
        self.bme280 = bme280
    
    def judge(self, data: Dict[str, Any]) -> bool:
        if data[const.DATA_PRESS] > 1000.:
            return True
        else:
            return False
        
    def control(self):
        print(self.bme280.read())
        
    def exit(self):
        pass
    
class TestNode2(Node):
    
    def enter(self):
        self.bme280 = bme280
    
    def judge(self, data: Dict[str, Any]) -> bool:
        if data[const.DATA_PRESS] > 1000.:
            return True
        else:
            return False
        
    def control(self):
        print(self.bme280.read())
        
    def exit(self):
        pass
    
    
context = Context({TestNode1: {True: TestNode2, False: TestNode1},
                   TestNode2: None}, 
                  start=TestNode1, 
                  end=TestNode2)
node1 = TestNode1()

pprint(context.next(node1.judge({const.DATA_PRESS: 800})))
pprint(context.next(False))
