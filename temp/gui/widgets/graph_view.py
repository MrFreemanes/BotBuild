from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene

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
        self.node_widgets: dict[str, NodeWidget] = {}
        self.edge_widgets: dict[str, EdgeWidget] = {}

        self.drag_port = None
        self.temp_edge = None

        self.model.node_added.connect(self.node_widget_add)
        self.model.node_update_pos.connect(self.node_widget_update_pos)
        self.model.node_update_params.connect(self.node_widget_update_params)
        self.model.node_delete.connect(self.node_widget_delete)

        self.model.edge_added.connect(self.edge_widget_add)
        self.model.edge_update_pos.connect(self.edge_widget_update_pos)
        self.model.edge_delete.connect(self.edge_widget_delete)

    @Slot(NodeModel)
    def node_widget_add(self, node: NodeModel):
        node_widget = NodeWidget(self.model, node)
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
            if port.edge_widget is not None:
                port.edge_widget.update_path()
        for port in node_widget.input_ports_widget.values():
            if port.edge_widget is not None:
                port.edge_widget.update_path()

    @Slot(EdgeModel)
    def edge_widget_delete(self, edge: EdgeModel):
        edge_widget = self.edge_widgets[edge.id]
        del self.edge_widgets[edge.id]
        self.scene.removeItem(edge_widget)

    def start_connection(self, port_widget):
        self.drag_port = port_widget

        self.temp_edge = EdgeTemporaryWidget(port_widget)
        self.scene.addItem(self.temp_edge)

    def remove_connection(self, edge_widget: EdgeWidget):
        self.model.delete_edge(edge_widget.edge.id)

    def mouseMoveEvent(self, event, /):
        if self.temp_edge:
            scene_pos = self.mapToScene(event.pos())
            self.temp_edge.set_temp_pos(scene_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event, /):
        if self.temp_edge:
            scene_pos = self.mapToScene(event.pos())
            items = self.scene.items(scene_pos)
            target_port = None
            for item in items:
                if isinstance(item, PortWidget):
                    target_port = item
                    break
            if target_port:
                self.model.add_edge(self.drag_port.port, target_port.port)
            self.scene.removeItem(self.temp_edge)
            self.temp_edge = None
            self.drag_port = None
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
