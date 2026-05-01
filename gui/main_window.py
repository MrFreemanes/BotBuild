from PySide6.QtWidgets import QGraphicsScene, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from config.config import Result
from gui.base_window import BaseWindow
from utils.graph_compiler import GraphCompiler
from gui.models.graph_model import GraphModel
from gui.widgets.graph_view import GraphView
from gui.widgets.sidebar.sidebar_widget import Sidebar
from utils.file_io import load_bot_json, save_bot_json


class MainWindow(BaseWindow):
    def setup_ui(self) -> None:
        """Обозначение главных переменных."""
        self.setWindowTitle('BotBuild')

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-4000, -4000, 8000, 8000)
        self.model = GraphModel()
        self.view = GraphView(self.scene, self.model)
        self.graph_compiler = GraphCompiler(self.model)

        self.run_btn = QPushButton('Run')
        self.save_btn = QPushButton('Save')
        self.load_btn = QPushButton('load')
        sidebar = Sidebar()

        layout_btn = QVBoxLayout()
        layout_btn.addWidget(sidebar)
        layout_btn.addWidget(self.run_btn)
        layout_btn.addWidget(self.save_btn)
        layout_btn.addWidget(self.load_btn)

        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(layout_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def connect_widget(self) -> None:
        """Подключение виджетов к функциям."""
        self.run_btn.clicked.connect(self._run)
        self.save_btn.clicked.connect(self.save)
        self.load_btn.clicked.connect(self.load)
        self.graph_compiler.validate_signal.connect(self._dialog_error)

    def _run(self) -> None:
        chain = self.graph_compiler.compile()
        if chain is not None:
            self.run_task('run_bot',
                          chain,
                          progress_handler=self._set_working_node_id,
                          finally_handler=self._finally_run)
        else:
            self.logger.warning('chain пуст')

    def _set_working_node_id(self, result: Result) -> None:
        self.view.set_working_node(result.result)

    def _finally_run(self) -> None:
        self.view.set_working_node(None)

    def save(self) -> None:
        save_bot_json('Test.json', self.model.to_dict())

    def load(self) -> None:
        self.view.clear_scene()
        self.model.load_from_dict(load_bot_json('Test.json'))
