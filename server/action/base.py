import time

from . import TaskAction


class TaskActionReverse(TaskAction):
    name = 'reverse'

    def process(self) -> None:
        time.sleep(2)
        self.task.done(self.task.data[::-1])


class TaskActionSwap(TaskAction):
    name = 'swap'

    def process(self) -> None:
        time.sleep(5)
        result = ''
        size = len(self.task.data) // 2
        for i in range(0, size):
            result += self.task.data[2 * i + 1]
            result += self.task.data[2 * i]
        result += self.task.data[2 * size:]
        self.task.done(result)


class TaskActionRepeat(TaskAction):
    name = 'repeat'

    def process(self) -> None:
        time.sleep(7)
        result = ''
        for i in range(0, len(self.task.data)):
            result += self.task.data[i] * (i + 1)
        self.task.done(result)
