from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsProxyWidget

from config.widget_registry import WIDGET_REGISTRY
from gui.models.graph_model import GraphModel
from gui.models.node_model import NodeModel
from gui.widgets.actions.base_action_widget import BaseActionWidget
from gui.widgets.potrs.port_widget import PortWidget


class NodeWidget(QGraphicsRectItem):
    """
    Класс визуального отображения ноды.
    """

    def __init__(self, model: GraphModel, node: NodeModel, interaction_handler):
        super().__init__()

        self.model = model
        self.node = node
        self.interaction_handler = interaction_handler
        self.setPos(*self.node.get_pos())
        self.setBrush(Qt.blue)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)

        # Виджет
        self.widget = self.create_widget()
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)

        self.update_size()
        # Порты
        self.input_ports_widget, self.output_ports_widget = self.create_ports()

    def create_widget(self) -> BaseActionWidget:
        """
        :return: BaseActionWidget - виджет в зависимости от переданного типа действия.
        """
        return WIDGET_REGISTRY[self.node.action_type](
            self.model,
            self.node,
            node_widget=self
        )

    def create_ports(self) -> tuple[dict[str, PortWidget], dict[str, PortWidget]]:
        """
        Создает 2 словаря портов {имя_порта: порт, ...}. Устанавливает их равномерно по правой и левой стороне ноды.
        :return: ({имя_порт_входа: порт, ...}, {имя_порт_выхода: порт, ...})
        """
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

    def update_size(self):
        """
        Берет размер виджета на ноде и меняет размер в соответствии с ним.
        """
        # Размер Node
        w, h = self.widget.get_geometry()
        self.setRect(0, 0, w + 4, h + 4)

        rect = self.rect()
        p_x = (rect.width() - w) / 2
        p_y = (rect.height() - h) / 2
        self.proxy.setPos(p_x, p_y)

    def mousePressEvent(self, event, /):
        self.interaction_handler.node_mouse_press(event, self)
        event.accept()

    def mouseMoveEvent(self, event, /):
        self.interaction_handler.node_mouse_move(event, self)

    def work(self):
        self.setBrush(QBrush(QColor(0,107,60)))
        for in_port in self.input_ports_widget.values():
            in_port.work()
        for out_port in self.output_ports_widget.values():
            out_port.work()

    def rest(self):
        self.setBrush(Qt.blue)
        for in_port in self.input_ports_widget.values():
            in_port.rest()
        for out_port in self.output_ports_widget.values():
            out_port.rest()
