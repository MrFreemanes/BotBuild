from abc import ABC, abstractmethod

from core.actions.halpers.context import Context


class BaseAction(ABC):
    @abstractmethod
    def run(self, context: Context):
        pass
