
import time
import random
import unittest

from pisat.core.logger import SensorController
from pisat.core.nav import Node, Context
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import NumberGenerator


NAME_NUMBERGENERATOR = "numgen"


class LinkedDataModel(LinkedDataModelBase):
    num = linked_loggable(NumberGenerator.DataModel.num, NAME_NUMBERGENERATOR)
    
    @cached_loggable
    def num_sqrt(self):
        return self.num ** 2


class TestNode1(Node):
    
    model = LinkedDataModel
    
    def judge(self, data: LinkedDataModel) -> bool:
        print(f"TestNode1 num_sqrt: {data.num_sqrt}")
        if data.num_sqrt < 0.5:
            return True
        else:
            return False
        
    
class TestNode2(Node):
    
    model = LinkedDataModel
    
    def judge(self, data: LinkedDataModel) -> bool:
        print(f"TestNode2 num_sqrt: {data.num_sqrt}")
        if data.num_sqrt > 0.5:
            return True
        else:
            return False
        
        
class TestNodeContext(unittest.TestCase):
    
    def setUp(self) -> None:
        self.context = Context({TestNode1: {True: TestNode2, False: TestNode1},
                                TestNode2: {True: None, False: TestNode2}}, 
                                start=TestNode1)
        numgen = NumberGenerator(random.random, name=NAME_NUMBERGENERATOR)
        self.sencon = SensorController(LinkedDataModel, name="sencon")
        self.sencon.append(numgen)
        
    def test_flow(self):
        node = self.context.start(None, None)
        while True:
            data = self.sencon.read()
            result = node.judge(data)
            
            next = self.context.next(result)
            if next is None:
                break
            
            if next != node.__class__:
                print(f"{node.__class__.__name__} detected: {result}")
                node = next(None, None)
                
        
if __name__ == "__main__":
    unittest.main()
