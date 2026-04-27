from enum import Enum


class ActionType(Enum):
    """
    Типы действий. Используются в ui и core.
    """
    CLICK = "Click"
    WAIT = "Wait"
    IF = "If"
    LOOP = "Loop"
    SEARCH_FOR_IF = "Search for if"
    SEARCH = "Search"


class ClickType(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    MIDDLE = "Middle"


ACTIONS_SUITABLE_FOR_IF = [ActionType.SEARCH_FOR_IF]  # Действия к которым подключается первый порт if/
