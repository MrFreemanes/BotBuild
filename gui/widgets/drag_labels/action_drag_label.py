from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QLabel

from config.action_config import ActionType


class ActionDragLabel(QLabel):
    def __init__(self, text: str, action_type: ActionType):
        super().__init__(text)

        self.action_type = action_type

    def mouseMoveEvent(self, ev, /):
        if ev.buttons() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.action_type.value)

        drag.setMimeData(mime)
        drag.exec()
