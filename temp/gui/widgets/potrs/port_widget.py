from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsEllipseItem

from gui.models.port_model import PortModel


class PortWidget(QGraphicsEllipseItem):
    def __init__(self, port: PortModel, x: int | float, y: int | float, patent):
        super().__init__(x, y, 10, 10, patent)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

        self.port = port
        self.edge_widget = None

    def get_center(self):
        return self.scenePos() + self.boundingRect().center()

    def mousePressEvent(self, event, /):
        view = self.scene().views()[0]

        if not self.port.is_free and self.edge_widget is not None:
            view.remove_connection(self.edge_widget)
        view.start_connection(self)
