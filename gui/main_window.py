from PySide6.QtWidgets import QGraphicsScene, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from config.action_config import ActionType
from gui.base_window import BaseWindow
from gui.models.graph_model import GraphModel
from gui.widgets.graph_view import GraphView
from gui.widgets.sidebar.sidebar_widget import Sidebar
from utils.file_io import load_bot_json, save_bot_json


class MainWindow(BaseWindow):
    def setup_ui(self) -> None:
        """Обозначение главных переменных."""
        self.setWindowTitle('BotBuild')

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        self.model = GraphModel()
        self.view = GraphView(self.scene, self.model)

        save_btn = QPushButton('Save')
        load_btn = QPushButton('load')
        sidebar = Sidebar()

        layout_btn = QVBoxLayout()
        layout_btn.addWidget(sidebar)
        layout_btn.addWidget(save_btn)
        layout_btn.addWidget(load_btn)

        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(layout_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        save_btn.clicked.connect(self.save)
        load_btn.clicked.connect(self.load)
        self.init_nodes()

    def init_nodes(self):
        self.model.add_node(ActionType.CLICK, (100, 100))
        self.model.add_node(ActionType.CLICK, (120, 120))
        self.model.add_node(ActionType.CLICK, (130, 130))
        self.model.add_node(ActionType.WAIT, (150, 150))
        self.model.add_node(ActionType.IF, (110, 110))
        self.model.add_node(ActionType.SEARCH_FOR_IF, (110, 110))

    def connect_widget(self) -> None:
        """Подключение виджетов к функциям."""
        pass

    def _run(self) -> None:
        pass

    def _finally_run(self) -> None:
        pass

    def save(self):
        save_bot_json('Test.json', self.model.to_dict())

    def load(self):
        self.view.clear_scene()
        self.model.load_from_dict(load_bot_json('Test.json'))
