from abc import ABC, abstractmethod

from core.actions.halpers.context import Context


class Action(ABC):
    @abstractmethod
    def run(self, context: Context):
        pass
