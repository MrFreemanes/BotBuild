from PySide6.QtWidgets import QLabel, QVBoxLayout

from gui.widgets.actions.base_action_widget import BaseActionWidget


class IfActionWidget(BaseActionWidget):
    def set_up(self):
        self._add_label()

    def _add_label(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Действие:\n'))
        layout.addWidget(QLabel('True:\n'))
        layout.addWidget(QLabel('False:\n'))
        self.layout.addLayout(layout)

