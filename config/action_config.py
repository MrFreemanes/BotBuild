from enum import Enum


class ActionType(Enum):
    """
    Типы действий. Используются в ui и core.
    """
    CLICK = "Click"
    WAIT = "Wait"
    IF = "If"
    SEARCH_FOR_IF = "Search for if"
    WAIT_UNTIL = "Wait Until"
    SEARCH_FOR_WAIT_UNTIL = "Search for wait until"


class ClickType(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    MIDDLE = "Middle"


# Действия к которым подключается первый порт If
ACTIONS_SUITABLE_FOR_IF = [
    ActionType.SEARCH_FOR_IF
]
# Действия к которым подключается первый порт Wait until
ACTIONS_SUITABLE_FOR_WAIT_UNTIL = [
    ActionType.SEARCH_FOR_WAIT_UNTIL
]
