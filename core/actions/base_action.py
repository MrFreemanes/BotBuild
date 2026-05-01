from abc import ABC, abstractmethod

from core.actions.halpers.context import Context


class BaseAction(ABC):
    def __init__(self, node_id: str):
        self.node_id = node_id

    @abstractmethod
    def run(self, context: Context):
        pass
