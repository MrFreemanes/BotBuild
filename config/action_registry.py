from config.action_config import ActionType
from core.actions import *

ACTION_REGISTRY = {
    # Normal actions
    ActionType.CLICK: ClickAction,
    ActionType.WAIT: WaitAction,
    # If actions
    ActionType.IF: IfAction,
    ActionType.SEARCH_FOR_IF: ImageSearchAction,
    # Wait until actions
    ActionType.WAIT_UNTIL: WaitUntilAction,
    ActionType.SEARCH_FOR_WAIT_UNTIL: ImageSearchAction
}
