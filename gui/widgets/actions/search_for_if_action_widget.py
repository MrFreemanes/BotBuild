from PySide6.QtWidgets import QLabel, QVBoxLayout

from gui.widgets.actions.base_action_widget import BaseActionWidget


class SearchForIfActionWidget(BaseActionWidget):
    def set_up(self) -> None:
        self._add_label()

    def _add_label(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Шаблон: '))
        self.layout.addLayout(layout)

