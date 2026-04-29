from PySide6.QtWidgets import QLabel, QComboBox, QHBoxLayout

from gui.widgets.actions.base_action_widget import BaseActionWidget
from config.action_config import ClickType


class ClickActionWidget(BaseActionWidget):
    def set_up(self) -> None:
        self._add_combo_box_click_type()

    def _add_combo_box_click_type(self) -> None:
        self.combo_box = QComboBox()
        self.combo_box.addItem(ClickType.LEFT.value)
        self.combo_box.addItem(ClickType.RIGHT.value)
        self.combo_box.addItem(ClickType.MIDDLE.value)
        self.combo_box.setCurrentText(self._params['click_type'])

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Тип клика:'))
        layout.addWidget(self.combo_box)
        self.layout.addLayout(layout)

        self.combo_box.currentTextChanged.connect(self._changed_combo_box_click_type)

    def _changed_combo_box_click_type(self, click_type) -> None:
        self.model.set_node_params(self.node.id, 'click_type', click_type)
