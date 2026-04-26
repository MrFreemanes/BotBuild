import uuid
import logging
from logging import config

from PySide6.QtCore import QObject

from gui.models.port_model import PortModel
from logs.logger_cfg import cfg
from config.widget_config import DirectionType
from config.node_registry import NODE_REGISTRY
from config.action_config import ActionType


class NodeModel(QObject):
    def __init__(self, action_type: ActionType, pos: tuple, node_id: str = None):
        super().__init__()

        logging.config.dictConfig(cfg)
        self.logger = logging.getLogger('log_model')

        self.action_type = action_type
        self.id = node_id or str(uuid.uuid4())
        self._pos = pos
        self._params = NODE_REGISTRY[self.action_type]['base_params'].copy()

        self.inputs = {name: PortModel(self.id, self.action_type, name, DirectionType.INPUT) for name in
                       NODE_REGISTRY[self.action_type]['ports']['inputs']}
        self.outputs = {name: PortModel(self.id, self.action_type, name, DirectionType.OUTPUT) for name in
                        NODE_REGISTRY[self.action_type]['ports']['outputs']}

        self.logger.debug('NodeModel created, id: %s, action_type: %s, pos: %s, params %s',
                          self.id, self.action_type, self._pos, self._params)

    def set_pos(self, pos: tuple):
        self._pos = pos

    def get_pos(self) -> tuple:
        return self._pos

    def set_params(self, params: dict):
        self._params.update(params)
        self.logger.info('New params in node, id: %s, params: %s', self.id, self._params)

    def get_params(self) -> dict:
        return self._params.copy()

    def to_dict(self) -> dict:
        return {
            'action_type': self.action_type.value,
            'id': self.id,
            'pos': self._pos,
            'params': self._params
        }
