from time import time
from typing import ClassVar
from enum import auto, Enum

from .case import camel_to_snake


class ActionType(Enum):
    CUSTOM = auto()
    QUIT = auto()


class Action:
    type: ClassVar[ActionType]

    def __init__(self) -> None:
        self.time = time()

    def __init_subclass__(cls, type: ActionType) -> None:
        super().__init_subclass__()
        cls.type = type

    @property
    def name(self) -> str:
        if not hasattr(self, "_name"):
            _name = camel_to_snake(self.__class__.__name__)
            if _name.endswith("_event"):
                _name = _name[:-6]
            self._name = _name
        return self._name


class QuitAction(Action, type=ActionType.QUIT):
    pass
