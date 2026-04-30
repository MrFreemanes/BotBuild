from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QVBoxLayout

from gui.widgets.actions.base_action_widget import BaseActionWidget


class WaitUntilActionWidget(BaseActionWidget):
    def set_up(self) -> None:
        self._add_label()
        self._add_spin_box_timeout()

    def _add_label(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Действие:\n', alignment=(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)))
        layout.addWidget(QLabel('True:\n', alignment=(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)))
        layout.addWidget(QLabel('Timeout:', alignment=(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)))
        self.layout.addLayout(layout)

    def _add_spin_box_timeout(self):
        timeout = self._params['timeout'] or 0
        self.spin_box = QSpinBox(value=timeout, minimum=0)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Таймаут:'))
        layout.addWidget(self.spin_box)
        self.layout.addLayout(layout)

        self.spin_box.valueChanged.connect(self._changed_spin_box_timeout)

    def _changed_spin_box_timeout(self, timeout) -> None:
        self.model.set_node_params(self.node.id, 'timeout', timeout)
