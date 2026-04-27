from config.action_config import ActionType, ACTIONS_SUITABLE_FOR_IF
from config.node_registry import NODE_REGISTRY
from config.widget_config import DirectionType
from gui.models.graph_model import GraphModel


class ConnectionController:
    """
    Класс создающий и удаляющий связи (EdgeWidget).
    Проверяет валидность соединения и отправляет в GraphModel порты для соединения.
    Если порт уже участвует в соединении, то отправляет в GraphModel edge_id для удаления связи.
    """

    def __init__(self, model: GraphModel, view):
        self.model = model
        self.view = view
        self.drag_port_widget = None
        self.temp_edge = None

    def start_connect(self, drag_port_widget) -> None:
        """
        Проверяет подключен ли порт. Вызывает метод создания временной связи.
        :param drag_port_widget: Порт-виджет от которого начали тянуть.
        """
        if drag_port_widget.edge_id is not None:
            self.model.delete_edge(drag_port_widget.edge_id)

        self.drag_port_widget = drag_port_widget
        self.temp_edge = self.view.temp_edge_create(self.drag_port_widget)

    def update_connect(self, scene_pos) -> None:
        """
        Вызывает метод обновления позиции временной линии если она есть.
        :param scene_pos: Координаты курсора в view.
        """
        if self.temp_edge:
            self.temp_edge.set_temp_pos(scene_pos)

    def finish_connect(self, drop_port_widget) -> None:
        """
        Если есть порт от которого тянули и их связь возможна -
        то отправляет в GraphModel порты для создания связи.
        :param drop_port_widget: Порт-виджет под курсором.
        """
        if not self.drag_port_widget:
            return

        if self.is_valid(self.drag_port_widget.port, drop_port_widget.port):
            self.model.add_edge(self.drag_port_widget.port, drop_port_widget.port)

        self.cleanup()

    def cleanup(self) -> None:
        """
        Отчищает данные о временной связи.
        """
        self.view.temp_edge_delete(self.temp_edge)
        self.temp_edge = None
        self.drag_port_widget = None

    def is_valid(self, p1, p2) -> bool:
        """
        Метод проверяющий возможность соединения 2-х портов.
        :param p1: PortModel
        :param p2: PortModel
        :return: bool - можно ли соединить.
        """
        from_port = p1 if p1.direction == DirectionType.OUTPUT else p2
        to_port = p2 if p2.direction == DirectionType.INPUT else p1

        if to_port.action_type in ACTIONS_SUITABLE_FOR_IF:
            if from_port.name != NODE_REGISTRY[ActionType.IF]['ports'][DirectionType.OUTPUT][0]:
                return False

        if from_port.name == NODE_REGISTRY[ActionType.IF]['ports'][DirectionType.OUTPUT][0]:
            if to_port.action_type not in ACTIONS_SUITABLE_FOR_IF:
                return False

        return True
