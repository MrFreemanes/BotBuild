from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QGraphicsEllipseItem

from gui.models.port_model import PortModel


class PortWidget(QGraphicsEllipseItem):
    def __init__(self, port: PortModel, x: int | float, y: int | float, patent):
        super().__init__(x, y, 10, 10, patent)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

        self.port = port
        self.edge_id = port.edge_id

    def get_center(self) -> QPointF:
        return self.scenePos() + self.boundingRect().center()

    def mousePressEvent(self, event, /):
        view = self.scene().views()[0]
        view.interaction_handler.port_mouse_press(event, self)
