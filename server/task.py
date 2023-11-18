import logging
import uuid
from typing import Optional
from queue import SimpleQueue


class Task:
    """Task class which contain task details:
       - id: uuid of task
       - task_type
       - data: initial data of task
       - status: current task status
       - result: result of taks processing
    """

    # FIXME enum???
    INIT = 'init'
    QUEUE = 'queue'
    RUNNING = 'running'
    DONE = 'done'
    ERROR = 'error'

    def __init__(self, task_type: str, data: str):
        # Без проверки на уникальность id в TaskProcessor
        self.id = str(uuid.uuid4())
        self.task_type = task_type
        self.data = data
        self.status = self.INIT
        self.result = None

    def __str__(self):
        return f"Task({self.id}: '{self.task_type}' : '{self.data}')"

    def done(self, result: str) -> None:
        self.status = self.DONE
        self.result = result
        logging.debug("Done %s", self)

    def error(self, error_str: str) -> None:
        self.status = self.ERROR
        self.result = error_str
        logging.debug("Error %s", self)

    def process(self) -> None:
        from action import repository
        repository.process(self)


class TaskProcessor:
    """Class to process tasks from queue."""

    def __init__(self):
        self.__tasks = {}
        self.__queue = SimpleQueue()

    def add(self, task_type: str, data: str) -> Task:
        task = Task(task_type, data)
        task.status = task.QUEUE
        logging.debug("Put in queue %s", task)
        self.__queue.put(task)
        self.__tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Optional[Task]:
        return self.__tasks.get(task_id)

    def run(self) -> None:
        while True:
            task = self.__queue.get()
            task.status = task.RUNNING
            logging.debug("Processing %s", task)
            task.process()


processor = TaskProcessor()
