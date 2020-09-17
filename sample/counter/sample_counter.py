
from pisat.core.manager import ComponentManager
from pisat.core.nav import Context
from pisat.core.cansat import CanSat

from .counter import Counter
from .test_node1 import TestNode1
from .test_node2 import TestNode2


def main():
    counter = Counter(name="counter")
    manager = ComponentManager(counter)
    
    context = Context({
        TestNode1: {True: TestNode2, False: TestNode1},
        TestNode2: {True: None, False: TestNode2}
    })
    
    cansat = CanSat(context, manager)
    cansat.run()
    
if __name__ == "__main__":
    main()
