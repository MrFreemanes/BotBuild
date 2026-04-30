from PySide6.QtCore import Signal, QObject

from config.action_config import ActionType
from config.action_registry import ACTION_REGISTRY
from core.actions.base_action import Action
from gui.models.edge_model import EdgeModel
from gui.models.graph_model import GraphModel
from gui.models.node_model import NodeModel


class GraphCompiler(QObject):
    validate_signal = Signal(object)

    def __init__(self, model: GraphModel):
        super().__init__()
        self.model = model

        self.visited = []
        self.nodes: dict[str, NodeModel] | None = None
        self.edges: dict[str, EdgeModel] | None = None

    def compile(self):
        self.nodes = self.model.nodes.copy()
        self.edges = self.model.edges.copy()

        if not self._validate():
            return None

        chain = self._build(self._get_start_node())

        self.visited.clear()
        self.nodes = None
        self.edges = None

        return chain

    def _build(self, node: NodeModel | None) -> list[Action]:
        if node is None or node.id in self.visited:
            return []
        self.visited.append(node.id)

        if len(node.outputs) == 1:
            return [ACTION_REGISTRY[node.action_type](**node.get_params())] + self._build(self._get_next_node(node))
        elif len(node.outputs) == 0:
            return [ACTION_REGISTRY[node.action_type](**node.get_params())]
        else:
            outputs = {port_name: self._build(self._get_next_node(node, port_name)) for port_name in
                       node.outputs.keys()}
            return [ACTION_REGISTRY[node.action_type](**node.get_params(), **outputs)]

    def _validate(self) -> bool:
        if len(self.nodes) == 0:
            self.validate_signal.emit('На графе нет нод')
            return False

        connected_nodes = set()

        for edge in self.edges.values():
            connected_nodes.add(edge.from_node_id)
            connected_nodes.add(edge.to_node_id)

        for node_id, node in self.nodes.items():
            if node.inputs and node_id not in connected_nodes:
                self.validate_signal.emit(f'Нода {node.action_type.value} не подключена.')
                return False
            if len(node.outputs) > 1:
                if not self._validate_halper(node):
                    return False

        return True

    def _validate_halper(self, node: NodeModel) -> bool:
        match node.action_type:
            case ActionType.IF:
                if node.outputs['action'].edge_id is None or node.outputs['actions_true'].edge_id is None:
                    self.validate_signal.emit(f'Есть не подключенные порты у {ActionType.IF.value}')
                    return False
                return True
            case ActionType.WAIT_UNTIL:
                if node.outputs['action'].edge_id is None or node.outputs['actions_true'].edge_id is None:
                    self.validate_signal.emit(f'Есть не подключенные порты у {ActionType.WAIT_UNTIL.value}')
                    return False
                return True
            case _:
                self.validate_signal.emit(f'Неизвестная нода {node.action_type.value}')
                return False

    def _get_start_node(self) -> NodeModel | None:
        incoming = {node_id: 0 for node_id in self.nodes}

        for edge in self.edges.values():
            incoming[edge.to_node_id] += 1

        for node_id, count in incoming.items():
            if count == 0:
                return self.model.nodes[node_id]

        return None

    def _get_next_node(self, node: NodeModel, port_name: str = None) -> NodeModel | None:
        port = node.outputs['output' if port_name is None else port_name]
        edge = self.edges.get(port.edge_id, None)
        if edge:
            return self.model.nodes[edge.to_node_id]
        return None


"""
создаю словарь если в ноде больне 1 вызода со списками по названию 
начинаю итерироваться -> беру ключ проверяю есть ли подключение в этом порту если есть в список добавляю ноду 
"""
