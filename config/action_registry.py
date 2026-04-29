from config.action_config import ActionType
from core.actions import *

ACTION_REGISTRY = {
    ActionType.CLICK: ClickAction,
    ActionType.WAIT: WaitAction,
    ActionType.IF: IfAction,
    ActionType.SEARCH_FOR_IF: ImageSearchAction
}
