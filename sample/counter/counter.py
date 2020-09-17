from typing import Optional

from pisat.base import Component


class Counter(Component):

    def __init__(self, name:Optional[str] = None):
        # Component のコンストラクタを呼び出す
        # Component には name プロパティが定義されている
        super().__init__(name=name)

        self._count: int = 0

    @property
    def count(self):
        return self._count

    def increment(self):
        self._count += 1

    def reset(self):
        self._count = 0