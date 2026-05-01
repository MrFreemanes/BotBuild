import logging
from logging import config

from PySide6.QtCore import QObject, Signal

from config.action_config import ActionType
from config.widget_config import DirectionType
from gui.models.edge_model import EdgeModel
from gui.models.node_model import NodeModel
from gui.models.port_model import PortModel
from logs.logger_cfg import cfg


class GraphModel(QObject):
    """
    Класс-модель отвечающий за хранение данных о связях/нодах для их сохранения/восстановления.
    """
    node_added = Signal(object)
    node_update_pos = Signal(object)
    node_update_params = Signal(object)
    node_delete = Signal(object)
    edge_added = Signal(object)
    edge_update_pos = Signal(object)
    edge_delete = Signal(object)

    def __init__(self):
        super().__init__()

        logging.config.dictConfig(cfg)
        self.logger = logging.getLogger('log_model')

        self.nodes: dict[str, NodeModel] = {}
        self.edges: dict[str, EdgeModel] = {}

    def add_edge(self, port_1: PortModel, port_2: PortModel) -> None:
        """
        Отвечает за создание связи, ее сохранение, отправку сигнала о создании в edge_added.
        :param port_1: PortModel для соединения с другим.
        :param port_2: PortModel
        """
        if port_1.direction == port_2.direction:
            return
        if port_1.node_id == port_2.node_id:
            return
        if port_1.edge_id is not None or port_2.edge_id is not None:
            return
        from_port = port_1 if port_1.direction == DirectionType.OUTPUT else port_2
        to_port = port_2 if port_2.direction == DirectionType.INPUT else port_1

        edge = EdgeModel(from_port, to_port)
        self.edges[edge.id] = edge
        self.logger.info('Add edge, from_port_name: %s, to_port_name: %s', from_port.name, to_port.name)

        self.edge_added.emit(edge)

    def delete_edge(self, edge_id: str) -> None:
        """
        Отвечает за удаление связи и отправку сигнала об этом в edge_delete.
        :param edge_id: id связи.
        """
        edge = self.edges[edge_id]
        del self.edges[edge_id]
        edge.from_port.free()
        edge.to_port.free()
        self.logger.info('Delete edge, from_port_name: %s, to_port_name: %s',
                         edge.from_port.name, edge.to_port.name)

        self.edge_delete.emit(edge)

    def add_node(self, action_type: ActionType, pos: tuple) -> None:
        """
        Отвечает за создание ноды, ее сохранение, отправку сигнала о создании в node_added.
        :param action_type: Тип действия.
        :param pos: Координаты на view.
        """
        node = NodeModel(action_type, pos)
        self.nodes[node.id] = node
        self.logger.info('Add node, action_type: %s', action_type)

        self.node_added.emit(node)

    def set_node_pos(self, node_id: str, pos: tuple) -> None:
        """
        Отвечает за обновление позиции ноды и отправку сигнала об изменении в
        node_update_pos и edge_update_pos для передвижения связей.
        :param node_id: id ноды.
        :param pos: Координаты на view.
        """
        node = self.nodes[node_id]
        node.set_pos(pos)

        self.node_update_pos.emit(node)
        self.edge_update_pos.emit(node)

    def set_node_params(self, node_id: str, key: str, value: str | int) -> None:
        """
        Отвечает за обновление параметров ноды и отправку сигнала для синхронизации данных в node_update_params.
        :param node_id:
        :param key:
        :param value:
        """
        node = self.nodes[node_id]
        params = node.get_params()
        params[key] = value
        node.set_params(params)
        self.logger.info('Set param node, k/v: {%s: %s}', key, value)

        self.node_update_params.emit(node)

    def delete_node(self, node_id: str) -> None:
        """
        Отвечает за удаление ноды и отправку сигнала об этом в node_delete.
        :param node_id:
        """
        node = self.nodes[node_id]
        for edge_id, edge in list(self.edges.items()):
            if edge.is_there_connection(node_id):
                self.delete_edge(edge.id)
        del self.nodes[node_id]
        self.logger.info('Delete node, id: %s', node_id)

        self.node_delete.emit(node)

    def to_dict(self) -> dict:
        self.logger.info('Model to dict')
        nodes_data = []
        edges_data = []
        for node in self.nodes.values():
            nodes_data.append(node.to_dict())
        for edge in self.edges.values():
            edges_data.append(edge.to_dict())

        data = {'nodes': nodes_data, 'edges': edges_data}
        return data

    def load_from_dict(self, data: dict) -> None:
        """
        Создает модели ноды, отправляет сигнал о создании в node_added.
        Создает модели связи, отправляет сигнал о создании в edge_added.
        :param data: словарь загруженный из файла bot.json/
        """
        self.logger.info('Model load from dict')
        self.nodes.clear()
        self.edges.clear()
        for node_data in data['nodes']:
            node = NodeModel(
                action_type=ActionType(node_data['action_type']),
                pos=node_data['pos'],
                node_id=node_data['id'],
            )
            node.set_params(node_data['params'])

            self.nodes[node.id] = node
            self.node_added.emit(node)

        for edge_data in data['edges']:
            from_node = self.nodes[edge_data['from_node_id']]
            to_node = self.nodes[edge_data['to_node_id']]
            edge = EdgeModel(
                from_port=from_node.outputs[edge_data['from_port_name']],
                to_port=to_node.inputs[edge_data['to_port_name']],
                edge_id=edge_data['id']
            )

            self.edges[edge.id] = edge
            self.edge_added.emit(edge)
