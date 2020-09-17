from pisat.core.nav import Node


class TestNode1(Node):

    def enter(self):
        self.counter = self.manager.get_component("counter")

    def judge(self, data) -> bool:
        self.counter.increment()

        if self.counter.count > 5:
            return True
        else:
            return False