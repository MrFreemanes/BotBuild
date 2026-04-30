from PySide6.QtWidgets import QLabel, QHBoxLayout, QSpinBox

from gui.widgets.actions.base_action_widget import BaseActionWidget


class WaitActionWidget(BaseActionWidget):
    def set_up(self) -> None:
        self._add_spin_box_waiting_time()

    def _add_spin_box_waiting_time(self) -> None:
        self.spin_box = QSpinBox(value=self._params['waiting_time'], minimum=1)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Время ожидания:'))
        layout.addWidget(self.spin_box)
        self.layout.addLayout(layout)

        self.spin_box.valueChanged.connect(self._changed_spin_box_waiting_time)

    def _changed_spin_box_waiting_time(self, waiting_time) -> None:
        self.model.set_node_params(self.node.id, 'waiting_time', waiting_time)
