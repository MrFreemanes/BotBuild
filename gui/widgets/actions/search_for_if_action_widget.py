import os

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QFileDialog

from gui.widgets.actions.base_action_widget import BaseActionWidget


class SearchForIfActionWidget(BaseActionWidget):
    def set_up(self) -> None:
        self._add_label()

    def _add_label(self) -> None:
        layout = QVBoxLayout()
        template_path = self._params['template_path']
        self.path_btn = QPushButton()
        self.path_btn.clicked.connect(self._open_file_dialog)
        layout.addWidget(QLabel('Шаблон: '))
        layout.addWidget(self.path_btn)
        self.layout.addLayout(layout)
        if template_path is not None and os.path.exists(template_path):
            self.path_btn.setText(template_path.split('/')[-1])
        else:
            QTimer.singleShot(0, self._open_file_dialog)

    def _open_file_dialog(self):
        view = self.graphicsProxyWidget().scene().views()[0]
        template_path, _ = QFileDialog.getOpenFileName(
            view,
            "Выберите шаблон",
            "",
            "Images (*.png *.jpg)"
        )
        if template_path:
            self.model.set_node_params(self.node.id, 'template_path', str(template_path))
            self.path_btn.setText(template_path.split('/')[-1])
            QTimer.singleShot(0, self.node_widget.update_size)
        else:
            self.model.delete_node(self.node.id)
