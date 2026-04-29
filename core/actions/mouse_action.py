from config.action_config import ClickType
from core.actions.base_action import Action
from core.actions.halpers.context import Context
from core.actions.halpers.mouse_click import click


class ClickAction(Action):
    def __init__(self,
                 coordinates: tuple | None = (123, 123),
                 click_type: ClickType = ClickType.LEFT,
                 clicks: int = 1):
        self.coordinates = coordinates
        self.click_type = ClickType(click_type)
        self.clicks = clicks

    def run(self, context: Context):
        if self.coordinates is not None:
            click(*self.coordinates, clicks=self.clicks, button=self.click_type)
        else:
            if context.coordinates is not None:
                click(*context.coordinates, clicks=self.clicks, button=self.click_type)
            else:
                context.running = False

# MoveTo(time_to_move=0), PressMoveTo(time_to_move=0), MoveToClick(time_to_move=0)
