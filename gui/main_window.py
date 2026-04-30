from PySide6.QtWidgets import QGraphicsScene, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

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

        run_btn = QPushButton('Run')
        save_btn = QPushButton('Save')
        load_btn = QPushButton('load')
        sidebar = Sidebar()

        layout_btn = QVBoxLayout()
        layout_btn.addWidget(sidebar)
        layout_btn.addWidget(run_btn)
        layout_btn.addWidget(save_btn)
        layout_btn.addWidget(load_btn)

        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(layout_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        run_btn.clicked.connect(self._run)
        save_btn.clicked.connect(self.save)
        load_btn.clicked.connect(self.load)
        self.graph_compiler.validate_signal.connect(self._dialog_error)

    def connect_widget(self) -> None:
        """Подключение виджетов к функциям."""
        pass

    def _run(self) -> None:
        chain = self.graph_compiler.compile()
        if chain is not None:
            self.run_task('run_bot', chain)
        else:
            self.logger.warning('chain пуст')

    def _finally_run(self) -> None:
        pass

    def save(self):
        save_bot_json('Test.json', self.model.to_dict())

    def load(self):
        self.view.clear_scene()
        self.model.load_from_dict(load_bot_json('Test.json'))
