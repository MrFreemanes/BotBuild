from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from config.action_config import ActionType


class Sidebar(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        self.setMinimumWidth(170)

        self.build_tree()

    def build_tree(self) -> None:
        actions = QTreeWidgetItem(['Actions'])
        self.addTopLevelItem(actions)

        # Normal action
        click = QTreeWidgetItem(['Click'])
        click.setData(0, Qt.UserRole, ActionType.CLICK)
        actions.addChild(click)

        wait = QTreeWidgetItem(['Wait'])
        wait.setData(0, Qt.UserRole, ActionType.WAIT)
        actions.addChild(wait)

        if_action = QTreeWidgetItem(['If'])
        if_action.setData(0, Qt.UserRole, ActionType.IF)
        actions.addChild(if_action)

        wait_until_action = QTreeWidgetItem(['Wait until'])
        wait_until_action.setData(0, Qt.UserRole, ActionType.WAIT_UNTIL)
        actions.addChild(wait_until_action)

        # If actions
        if_actions = QTreeWidgetItem(['If actions'])
        self.addTopLevelItem(if_actions)

        if_search = QTreeWidgetItem(['If search'])
        if_search.setData(0, Qt.UserRole, ActionType.SEARCH_FOR_IF)
        if_actions.addChild(if_search)

        # Wait until actions
        wait_until_actions = QTreeWidgetItem(['Wait until actions'])
        self.addTopLevelItem(wait_until_actions)

        wait_until_search = QTreeWidgetItem(['Wait until search'])
        wait_until_search.setData(0, Qt.UserRole, ActionType.SEARCH_FOR_WAIT_UNTIL)
        wait_until_actions.addChild(wait_until_search)

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
