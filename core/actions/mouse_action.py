from config.action_config import ClickType
from core.actions.base_action import BaseAction
from core.actions.halpers.context import Context
from core.actions.halpers.mouse_click import click


class ClickAction(BaseAction):
    def __init__(self,
                 coordinates: tuple | None = None,
                 click_type: ClickType = ClickType.LEFT,
                 clicks: int = 1,
                 node_id: str = None):
        """
        :param coordinates: Координаты клика.
        :param click_type: Тип клика.
        :param clicks: Количество нажатий.
        """
        super().__init__(node_id)

        self.coordinates = coordinates
        self.click_type = ClickType(click_type)
        self.clicks = clicks

    def run(self, context: Context) -> None:
        """
        Нажатие по координатам, переданным пользователем, если они указаны.
        В противном случае нажатие осуществляется по координатам, которые были сохранены в context.
        Если и эти координаты отсутствуют, то context.running = False.
        """
        context.working_node(self.node_id)
        if self.coordinates is not None:
            click(*self.coordinates, clicks=self.clicks, button=self.click_type)
        else:
            if context.is_coordinates():
                click(*context.coordinates, clicks=self.clicks, button=self.click_type)
            else:
                context.running = False

