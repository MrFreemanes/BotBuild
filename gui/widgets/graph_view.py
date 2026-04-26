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


class GraphView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, model: GraphModel):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

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
    def node_widget_add(self, node: NodeModel):
        node_widget = NodeWidget(self.model, node, self.interaction_handler)
        self.node_widgets[node.id] = node_widget
        self.scene.addItem(node_widget)

    @Slot(NodeModel)
    def node_widget_update_pos(self, node: NodeModel):
        node_widget = self.node_widgets[node.id]
        node_widget.setPos(*node.get_pos())

    @Slot(NodeModel)
    def node_widget_update_params(self, node: NodeModel):
        node_widget = self.node_widgets[node.id]
        node_widget.widget.set_params(node.get_params())

    @Slot(NodeModel)
    def node_widget_delete(self, node: NodeModel):
        node_widget = self.node_widgets[node.id]
        self.scene.removeItem(node_widget)
        del self.node_widgets[node.id]

    @Slot(EdgeModel)
    def edge_widget_add(self, edge: EdgeModel):
        widget_1 = self.node_widgets[edge.from_node_id]
        widget_2 = self.node_widgets[edge.to_node_id]
        port_1 = widget_1.output_ports_widget[edge.from_port_name]
        port_2 = widget_2.input_ports_widget[edge.to_port_name]
        edge_widget = EdgeWidget(edge, port_1, port_2)
        self.edge_widgets[edge.id] = edge_widget
        self.scene.addItem(edge_widget)

    @Slot(NodeModel)
    def edge_widget_update_pos(self, node: NodeModel):
        node_widget = self.node_widgets[node.id]
        for port in node_widget.output_ports_widget.values():
            if port.edge_id is not None:
                self.edge_widgets[port.edge_id].update_path()
        for port in node_widget.input_ports_widget.values():
            if port.edge_id is not None:
                self.edge_widgets[port.edge_id].update_path()

    @Slot(EdgeModel)
    def edge_widget_delete(self, edge: EdgeModel):
        edge_widget = self.edge_widgets[edge.id]
        edge_widget.to_port.edge_id = None
        edge_widget.from_port.edge_id = None
        del self.edge_widgets[edge.id]
        self.scene.removeItem(edge_widget)

    def temp_edge_create(self, port_widget: PortWidget):
        temp_edge = EdgeTemporaryWidget(port_widget)
        self.scene.addItem(temp_edge)
        return temp_edge

    def temp_edge_delete(self, temp_edge: EdgeTemporaryWidget):
        self.scene.removeItem(temp_edge)

    def mouseMoveEvent(self, event, /):
        self.interaction_handler.view_mouse_move(event, self)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event, /):
        self.interaction_handler.view_mouse_release(event, self)
        super().mouseReleaseEvent(event)

    def clear_scene(self):
        self.node_widgets.clear()
        self.edge_widgets.clear()
        self.scene.clear()

    def wheelEvent(self, event):
        zoom_in = 1.2
        zoom_out = 1 / zoom_in

        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)
