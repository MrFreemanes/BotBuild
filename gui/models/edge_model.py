import uuid

from PySide6.QtCore import QObject

from gui.models.port_model import PortModel


class EdgeModel(QObject):
    """
    Класс-модель соединяющий 2 порта. Имеет 2 модели порта, их имена и id нод с которыми они связаны.
    """

    def __init__(self, from_port: PortModel, to_port: PortModel, edge_id: str = None):
        super().__init__()

        self.id = edge_id or str(uuid.uuid4())

        self.from_port = from_port
        self.from_port_name = self.from_port.name
        self.from_node_id = self.from_port.node_id

        self.to_port = to_port
        self.to_port_name = self.to_port.name
        self.to_node_id = self.to_port.node_id

        self.from_port.busy(self.id)
        self.to_port.busy(self.id)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'from_node_id': self.from_node_id,
            'from_port_name': self.from_port_name,
            'to_node_id': self.to_node_id,
            'to_port_name': self.to_port_name
        }

    def is_there_connection(self, node_id) -> bool:
        return self.from_node_id == node_id or self.to_node_id == node_id

    def __del__(self):
        self.from_port.free()
        self.to_port.free()
