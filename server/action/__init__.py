import pkgutil
from abc import abstractmethod, ABC
import logging

from task import Task


class TaskAction(ABC):
    name = None

    def __init__(self, task: Task):
        self.task = task

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        repository.register(cls)

    @abstractmethod
    def process(self) -> None:
        """ Process operator command.
            Output: tuple (result (bool), response (str))
        """
        raise NotImplementedError("'process' method is not implemnted yet")


class TaskActionRepository:

    def __init__(self):
        self.__actions = {}

    def register(self, cls: type[TaskAction]) -> None:
        """Register task actions."""
        if cls.name:
            if cls.name in self.__actions:
                logging.warning("Action '%s' already registered", cls.name)
            else:
                logging.info("Register action '%s'", cls.name)
                self.__actions[cls.name] = cls

    def process(self, task: Task) -> None:
        """ Process task action."""
        if task.task_type in self.__actions:
            try:
                self.__actions[task.task_type](task).process()
            except Exception as e:
                logging.warning("Error processing task '%s'", task,
                                exc_info=True)
                task.error(str(e))
        else:
            logging.warning("Unknown task type '%s'", task.task_type)
            task.error(f"Unknown task type '{task.task_type}'")


# Должен быть реальным синглетоном
repository = TaskActionRepository()


__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__,
                                                      prefix=__name__ + '.'):
    __import__(modname)
