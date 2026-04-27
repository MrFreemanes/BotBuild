from PySide6.QtCore import Qt

from config.action_config import ActionType
from gui.helpers.connection_controller import ConnectionController
from gui.models.graph_model import GraphModel
from gui.widgets.potrs.port_widget import PortWidget


class InteractionHandler:
    """
    Класс перехватывающий события мыши в view.
    """

    def __init__(self, model: GraphModel, connection_controller: ConnectionController):
        self.model = model
        self.connection_controller = connection_controller

        self.drag_pos = None

    def view_mouse_press(self, event, view_widget):
        pass

    def view_mouse_move(self, event, view_widget):
        """
        Вызывает методы при движении мыши.
        :param event: event из переопределенного метода.
        :param view_widget: QGraphicsView.
        """
        if event.buttons() == Qt.MouseButton.LeftButton:
            scene_pos = view_widget.mapToScene(event.pos())
            self.connection_controller.update_connect(scene_pos)

    def view_mouse_release(self, event, view_widget):
        """
        Проверяет есть ли PortWidget под курсором при отпускании кнопки мыши.
        :param event: event из переопределенного метода.
        :param view_widget: QGraphicsView.
        """
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

    def view_drop_event(self, event, view_widget):
        """
        Вызывает создание виджета при событии "drop" если в курсоре был объект из Sidebar.
        :param event: event из переопределенного метода.
        :param view_widget: QGraphicsView.
        """
        action_type = ActionType(event.mimeData().text())
        scene_pos = view_widget.mapToScene(event.pos())
        self.model.add_node(action_type, (scene_pos.x(), scene_pos.y()))

    def node_mouse_press(self, event, node_widget):
        """
        Определяет первоначальную позицию взятой ноды.
        :param event: event из переопределенного метода.
        :param node_widget: NodeWidget.
        """
        self.drag_pos = (event.pos().x(), event.pos().y())

    def node_mouse_move(self, event, node_widget):
        """
        Вычисляет перемещение и отправляет координаты в GraphModel для установления новой позиции ноды.
        :param event: event из переопределенного метода.
        :param node_widget: NodeWidget.
        """
        if not self.drag_pos:
            return

        x = node_widget.pos().x() - (self.drag_pos[0] - event.pos().x())
        y = node_widget.pos().y() - (self.drag_pos[1] - event.pos().y())
        self.model.set_node_pos(node_widget.node.id, (x, y))

    def node_mouse_release(self, event, node_widget):
        pass

    def port_mouse_press(self, event, port_widget):
        """
        При нажатии на порт вызывает метод начала соединения класса: ConnectionController.
        :param event: event из переопределенного метода.
        :param port_widget: PortWidget.
        """
        self.connection_controller.start_connect(port_widget)

    def port_mouse_move(self, event, port_widget):
        pass

    def port_mouse_release(self, event, port_widget):
        pass
