from config.action_config import ActionType
from gui.widgets.actions import *

"""
WIDGET_REGISTRY - ActionWidget из gui.widgets.actions для создания виджетов на нодах.
"""
WIDGET_REGISTRY = {
    ActionType.CLICK: ClickActionWidget,
    ActionType.WAIT: WaitActionWidget,
    ActionType.IF: IfActionWidget,
    ActionType.SEARCH_FOR_IF: SearchForIfActionWidget
}
