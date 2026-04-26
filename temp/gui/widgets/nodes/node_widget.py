from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsProxyWidget

from config.widget_registry import WIDGET_REGISTRY
from gui.models.graph_model import GraphModel
from gui.models.node_model import NodeModel
from gui.widgets.actions.base_action_widget import BaseActionWidget
from gui.widgets.potrs.port_widget import PortWidget


class NodeWidget(QGraphicsRectItem):
    def __init__(self, model: GraphModel, node: NodeModel):
        super().__init__()

        self.model = model
        self.node = node
        self.setPos(*self.node.get_pos())
        self.setBrush(QBrush(QColor(50, 100, 200)))
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)

        # Виджет
        self.widget = self.create_widget()
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)

        # Размер Node
        w, h = self.widget.get_geometry()
        self.setRect(0, 0, w + 4, h + 4)

        # Позиция виджета
        rect = self.rect()
        p_x = (rect.width() - w) / 2
        p_y = (rect.height() - h) / 2
        self.proxy.setPos(p_x, p_y)

        # Порты
        self.input_ports_widget, self.output_ports_widget = self.create_ports()

        self.drag_pos = None

    def create_widget(self) -> BaseActionWidget:
        return WIDGET_REGISTRY[self.node.action_type](
            self.model,
            self.node
        )

    def create_ports(self) -> tuple[dict[str, PortWidget], dict[str, PortWidget]]:
        in_ports = {}
        out_ports = {}
        rect = self.rect()
        w, h = rect.width(), rect.height()
        for i, in_port in enumerate(self.node.inputs.items()):
            in_ports[in_port[0]] = (PortWidget(
                port=in_port[1],
                x=-10,
                y=(h * ((i + 1) / (len(self.node.inputs) + 1)) - 5),
                patent=self
            ))
        for i, out_port in enumerate(self.node.outputs.items()):
            out_ports[out_port[0]] = (PortWidget(
                port=out_port[1],
                x=w,
                y=(h * ((i + 1) / (len(self.node.outputs) + 1)) - 5),
                patent=self
            ))
        return in_ports, out_ports

    def mousePressEvent(self, event, /):
        self.drag_pos = (event.pos().x(), event.pos().y())
        event.accept()

    def mouseMoveEvent(self, event, /):
        if not self.drag_pos:
            return

        x = self.pos().x() - (self.drag_pos[0] - event.pos().x())
        y = self.pos().y() - (self.drag_pos[1] - event.pos().y())
        self.model.set_node_pos(self.node.id, (x, y))
