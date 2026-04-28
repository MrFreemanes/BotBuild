from config.action_config import ClickType
from core.actions.base_action import Action
from core.actions.halpers.context import Context
from core.actions.halpers.mouse_click import click


class Click(Action):
    def __init__(self,
                 coordinates: tuple | None = None,
                 button: ClickType = ClickType.LEFT,
                 clicks: int = 1):
        self.coordinates = coordinates
        self.button = button
        self.clicks = clicks

    def run(self, context: Context):
        if self.coordinates is not None:
            click(*self.coordinates, clicks=self.clicks, button=self.button)
        else:
            click(*context.coordinates, clicks=self.clicks, button=self.button)

# MoveTo(time_to_move=0), PressMoveTo(time_to_move=0), MoveToClick(time_to_move=0)
