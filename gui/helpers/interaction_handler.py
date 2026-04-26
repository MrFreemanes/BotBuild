from gui.helpers.connection_controller import ConnectionController
from gui.models.graph_model import GraphModel
from gui.widgets.potrs.port_widget import PortWidget


class InteractionHandler:
    def __init__(self, model: GraphModel, connection_controller: ConnectionController):
        self.model = model
        self.connection_controller = connection_controller

        self.drag_pos = None

    def view_mouse_press(self, event, view_widget):
        pass

    def view_mouse_move(self, event, view_widget):
        scene_pos = view_widget.mapToScene(event.pos())
        self.connection_controller.update_connect(scene_pos)

    def view_mouse_release(self, event, view_widget):
        scene_pos = view_widget.mapToScene(event.pos())
        items = view_widget.scene.items(scene_pos)
        target_port = None
        for item in items:
            if isinstance(item, PortWidget):
                target_port = item
                break
        if target_port:
            self.connection_controller.finish_connect(target_port)
        self.connection_controller.cleanup()

    def node_mouse_press(self, event, node_widget):
        self.drag_pos = (event.pos().x(), event.pos().y())

    def node_mouse_move(self, event, node_widget):
        if not self.drag_pos:
            return

        x = node_widget.pos().x() - (self.drag_pos[0] - event.pos().x())
        y = node_widget.pos().y() - (self.drag_pos[1] - event.pos().y())
        self.model.set_node_pos(node_widget.node.id, (x, y))

    def node_mouse_release(self, event, node_widget):
        pass

    def port_mouse_press(self, event, port_widget):
        self.connection_controller.start_connect(port_widget)

    def port_mouse_move(self, event, port_widget):
        pass

    def port_mouse_release(self, event, port_widget):
        pass
