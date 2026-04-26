from PySide6.QtCore import QObject

from config.action_config import ActionType
from config.widget_config import DirectionType


class PortModel(QObject):
    def __init__(self, node_id: str, action_type: ActionType, name: str, direction: DirectionType):
        super().__init__()

        self.node_id = node_id
        self.action_type = action_type
        self.name = name
        self.direction = direction
        self.edge_id = None

    def free(self):
        self.edge_id = None

    def busy(self, edge_id):
        self.edge_id = edge_id
