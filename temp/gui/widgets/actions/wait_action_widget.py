from PySide6.QtWidgets import QLabel, QComboBox, QHBoxLayout, QSpinBox

from gui.widgets.actions.base_action_widget import BaseActionWidget
from config.action_config import ClickType


class WaitActionWidget(BaseActionWidget):
    def set_up(self):
        self._add_spin_box_waiting_time()

    def _add_spin_box_waiting_time(self):
        self.spin_box = QSpinBox(value=self._params['waiting_time'], minimum=1)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Время ожидания:'))
        layout.addWidget(self.spin_box)
        self.layout.addLayout(layout)

        self.spin_box.valueChanged.connect(self._changed__spin_box_waiting_time)

    def _changed__spin_box_waiting_time(self, waiting_time):
        self.model.set_node_params(self.node.id, 'waiting_time', waiting_time)
