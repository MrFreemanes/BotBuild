from enum import Enum


class ActionType(Enum):
    CLICK = "Click"
    WAIT = "Wait"
    IF = "If"
    LOOP = "Loop"


class ClickType(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    MIDDLE = "Middle"
