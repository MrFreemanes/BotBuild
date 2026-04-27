from PySide6.QtGui import QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem

from gui.widgets.potrs.port_widget import PortWidget


class EdgeTemporaryWidget(QGraphicsPathItem):
    def __init__(self, drag_port: PortWidget):
        super().__init__()

        self.drag_port = drag_port
        self.temp_pos = None

    def set_temp_pos(self, pos) -> None:
        self.temp_pos = pos
        self.update_path()

    def update_path(self) -> None:
        p1 = self.drag_port.get_center()
        p2 = self.temp_pos

        path = QPainterPath()
        path.moveTo(p1)

        dx = (p2.x() - p1.x()) / 2

        path.cubicTo(
            p1.x() + dx, p1.y(),
            p2.x() - dx, p2.y(),
            p2.x(), p2.y()
        )

        self.setPath(path)
