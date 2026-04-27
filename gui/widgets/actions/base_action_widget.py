import logging
from logging import config
from abc import abstractmethod

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from gui.models.graph_model import GraphModel
from gui.models.node_model import NodeModel
from gui.helpers.widget_overrides import attach_context_menu
from logs.logger_cfg import cfg


class BaseActionWidget(QWidget):
    """
    Базовый класс виджетов на нодах.
    """
    def __init__(self, model: GraphModel, node: NodeModel):
        super().__init__()

        logging.config.dictConfig(cfg)
        self.logger = logging.getLogger('log_widget')

        self.model = model
        self.node = node
        self._params = self.node.get_params()

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f'{self.node.action_type.value}\n', alignment=Qt.AlignCenter))
        self.setLayout(self.layout)

        self._attach_context_menu({'Удалить': lambda: self.model.delete_node(self.node.id)})
        self.set_up()

    @abstractmethod
    def set_up(self) -> None:
        pass

    def set_params(self, params: dict) -> None:
        self._params = params
        self.logger.info('New params in widget, id: %s, params: %s', self.node.id, self._params)

    def get_geometry(self) -> tuple:
        return self.sizeHint().width(), self.sizeHint().height()

    def _attach_context_menu(self, action: dict) -> None:
        attach_context_menu(self, action)
