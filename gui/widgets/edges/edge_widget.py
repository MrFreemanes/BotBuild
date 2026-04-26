from PySide6.QtCore import Qt
from PySide6.QtGui import QPainterPath, QPen
from PySide6.QtWidgets import QGraphicsPathItem

from gui.models.edge_model import EdgeModel
from gui.widgets.potrs.port_widget import PortWidget


class EdgeWidget(QGraphicsPathItem):
    def __init__(self, edge: EdgeModel, from_port: PortWidget, to_port: PortWidget):
        super().__init__()
        self.setPen(QPen(Qt.blue))

        self.edge = edge
        self.from_port = from_port
        self.to_port = to_port

        self.from_port.edge_id = self.edge.id
        self.to_port.edge_id = self.edge.id

        self.update_path()

    def update_path(self):
        p1 = self.from_port.get_center()
        p2 = self.to_port.get_center()

        path = QPainterPath()
        path.moveTo(p1)
        dx = (p2.x() - p1.x()) / 2

        path.cubicTo(
            p1.x() + dx, p1.y(),
            p2.x() - dx, p2.y(),
            p2.x(), p2.y()
        )

        self.setPath(path)

    def __del__(self):
        self.from_port.edge_id = None
        self.to_port.edge_id = None