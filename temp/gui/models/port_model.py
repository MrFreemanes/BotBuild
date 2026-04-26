from PySide6.QtCore import QObject

from config.widget_config import DirectionType


class PortModel(QObject):
    def __init__(self, node_id: str, name: str, direction: DirectionType):
        super().__init__()

        self.node_id = node_id
        self.name = name
        self.direction = direction
        self.is_free = True

    def free(self):
        self.is_free = True

    def busy(self):
        self.is_free = False