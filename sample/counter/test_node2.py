from pisat.core.nav import Node


class TestNode2(Node):

    def enter(self):
        self.counter = self.manager.ger_component("counter")

    def judge(self, data) -> bool:
        if self.counter.count > 5:
            print("Good")
            self.counter.reset()

        self.counter.increment()

        if self.counter.count > 2:
            return True
        else:
            return False