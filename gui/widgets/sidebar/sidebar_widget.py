from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from config.action_config import ActionType


class Sidebar(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setHeaderHidden(True)
        self.setDragEnabled(True)

        self.build_tree()

    def build_tree(self):
        actions = QTreeWidgetItem(['Actions'])
        self.addTopLevelItem(actions)

        click = QTreeWidgetItem(['Click'])
        click.setData(0, Qt.UserRole, ActionType.CLICK)
        actions.addChild(click)

        wait = QTreeWidgetItem(['Wait'])
        wait.setData(0, Qt.UserRole, ActionType.WAIT)
        actions.addChild(wait)

        if_action = QTreeWidgetItem(['If'])
        if_action.setData(0, Qt.UserRole, ActionType.IF)
        actions.addChild(if_action)

        if_actions = QTreeWidgetItem(['If actions'])
        self.addTopLevelItem(if_actions)

        if_search = QTreeWidgetItem(['If search'])
        if_search.setData(0, Qt.UserRole, ActionType.SEARCH_FOR_IF)
        if_actions.addChild(if_search)

        self.expandAll()

    def startDrag(self, supportedActions, /):
        item = self.currentItem()

        if not item:
            return

        action_type = item.data(0, Qt.UserRole)

        if action_type is None:
            return

        drag = QDrag(self)
        mime = QMimeData()

        mime.setText(action_type.value)
        drag.setMimeData(mime)

        drag.exec()
