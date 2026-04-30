from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout

from gui.widgets.actions.base_action_widget import BaseActionWidget


class IfActionWidget(BaseActionWidget):
    def set_up(self) -> None:
        self._add_label()

    def _add_label(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Action:\n', alignment=(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)))
        layout.addWidget(QLabel('True:\n', alignment=(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)))
        layout.addWidget(QLabel('False:\n\n', alignment=(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)))
        self.layout.addLayout(layout)
