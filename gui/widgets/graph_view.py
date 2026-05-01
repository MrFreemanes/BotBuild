import logging
from logging import config

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene

from gui.helpers.connection_controller import ConnectionController
from gui.helpers.interaction_handler import InteractionHandler
from gui.models.edge_model import EdgeModel
from gui.models.graph_model import GraphModel
from gui.models.node_model import NodeModel
from gui.widgets.edges.edge_temporary_widget import EdgeTemporaryWidget
from gui.widgets.edges.edge_widget import EdgeWidget
from gui.widgets.nodes.node_widget import NodeWidget
from gui.widgets.potrs.port_widget import PortWidget
from logs.logger_cfg import cfg


class GraphView(QGraphicsView):
    """
    Класс GraphicsView отвечающий за отображение нод и связей из класса GraphModel.
    """

    def __init__(self, scene: QGraphicsScene, model: GraphModel):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setAcceptDrops(True)

        logging.config.dictConfig(cfg)
        self.logger = logging.getLogger('log_widget')

        self.scene = scene
        self.model = model
        self.connection_controller = ConnectionController(self.model, self)
        self.interaction_handler = InteractionHandler(self.model, self.connection_controller)
        self.node_widgets: dict[str, NodeWidget] = {}
        self.edge_widgets: dict[str, EdgeWidget] = {}

        self.model.node_added.connect(self.node_widget_add)
        self.model.node_update_pos.connect(self.node_widget_update_pos)
        self.model.node_update_params.connect(self.node_widget_update_params)
        self.model.node_delete.connect(self.node_widget_delete)

        self.model.edge_added.connect(self.edge_widget_add)
        self.model.edge_update_pos.connect(self.edge_widget_update_pos)
        self.model.edge_delete.connect(self.edge_widget_delete)

    @Slot(NodeModel)
    def node_widget_add(self, node: NodeModel) -> None:
        """
        Добавляет на граф виджет ноды.
        :param node: NodeModel из GraphModel.
        """
        node_widget = NodeWidget(self.model, node, self.interaction_handler)
        self.node_widgets[node.id] = node_widget
        self.scene.addItem(node_widget)

        self.logger.debug('View. Add node widget, action_type: %s', node.action_type)

    @Slot(NodeModel)
    def node_widget_update_pos(self, node: NodeModel) -> None:
        """
        Обновляет позицию виджета ноды на графе.
        :param node: NodeModel из GraphModel.
        """
        node_widget = self.node_widgets[node.id]
        node_widget.setPos(*node.get_pos())

    @Slot(NodeModel)
    def node_widget_update_params(self, node: NodeModel) -> None:
        """
        Обновляет параметры QWidget на виджете ноды.
        :param node: NodeModel из GraphModel.
        """
        node_widget = self.node_widgets[node.id]
        node_widget.widget.set_params(node.get_params())

        self.logger.debug('View. Update params node widget, action_type: %s', node.action_type)

    @Slot(NodeModel)
    def node_widget_delete(self, node: NodeModel) -> None:
        """
        Удаляет виджет ноды с графа.
        :param node: NodeModel из GraphModel.
        """
        node_widget = self.node_widgets[node.id]
        self.scene.removeItem(node_widget)
        del self.node_widgets[node.id]

        self.logger.debug('View. Delete node widget, action_type: s%', node.action_type)

    @Slot(EdgeModel)
    def edge_widget_add(self, edge: EdgeModel) -> None:
        """
        Соединяет 2 порта у виджетов ноды.
        :param edge: EdgeModel из GraphModel.
        """
        widget_1 = self.node_widgets[edge.from_node_id]
        widget_2 = self.node_widgets[edge.to_node_id]
        port_1 = widget_1.output_ports_widget[edge.from_port_name]
        port_2 = widget_2.input_ports_widget[edge.to_port_name]
        edge_widget = EdgeWidget(edge, port_1, port_2)
        self.edge_widgets[edge.id] = edge_widget
        self.scene.addItem(edge_widget)

        self.logger.debug('View. Add edge widget, from_port: s%, to_port: s%',
                          edge.from_port_name, edge.to_port_name)

    @Slot(NodeModel)
    def edge_widget_update_pos(self, node: NodeModel) -> None:
        """
        Обновляет путь связанный с виджетом ноды.
        :param node: NodeModel из GraphModel.
        """
        node_widget = self.node_widgets[node.id]
        for port in node_widget.output_ports_widget.values():
            if port.edge_id is not None:
                self.edge_widgets[port.edge_id].update_path()
        for port in node_widget.input_ports_widget.values():
            if port.edge_id is not None:
                self.edge_widgets[port.edge_id].update_path()

    @Slot(EdgeModel)
    def edge_widget_delete(self, edge: EdgeModel) -> None:
        """
        Удаляет путь.
        :param edge: EdgeModel из GraphModel.
        """
        edge_widget = self.edge_widgets[edge.id]
        edge_widget.to_port.edge_id = None
        edge_widget.from_port.edge_id = None
        del self.edge_widgets[edge.id]
        self.scene.removeItem(edge_widget)

        self.logger.debug('View. Delete edge widget, from_port: s%, to_port: s%',
                          edge.from_port_name, edge.to_port_name)

    def temp_edge_create(self, port_widget: PortWidget) -> EdgeTemporaryWidget:
        """
        Создает и добавляет на граф временный путь.
        :param port_widget: PortWidget под курсором при нажатии.
        :return: EdgeTemporaryWidget - класс на время передвижения мыши с зажатой лкм.
        """
        temp_edge = EdgeTemporaryWidget(port_widget)
        self.scene.addItem(temp_edge)
        return temp_edge

    def temp_edge_delete(self, temp_edge: EdgeTemporaryWidget) -> None:
        """
        Удаляет временный путь.
        :param temp_edge: EdgeTemporaryWidget - класс на время передвижения мыши с зажатой лкм.
        """
        self.scene.removeItem(temp_edge)

    def mouseMoveEvent(self, event, /):
        self.interaction_handler.view_mouse_move(event, self)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event, /):
        self.interaction_handler.view_mouse_release(event, self)
        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event, /):
        if event.mimeData().hasText():
            event.accept()

    def dragMoveEvent(self, event, /):
        event.accept()

    def dropEvent(self, event, /):
        self.interaction_handler.view_drop_event(event, self)

    def clear_scene(self) -> None:
        """
        Отчищает граф от нод и связей.
        """
        self.node_widgets.clear()
        self.edge_widgets.clear()
        self.scene.clear()

        self.logger.debug('View. Clear scene.')

    def wheelEvent(self, event) -> None:
        zoom_in = 1.2
        zoom_out = 1 / zoom_in

        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)
