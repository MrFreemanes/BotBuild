import time

from core.actions.base_action import Action
from core.actions.halpers.context import Context


class Wait(Action):
    def __init__(self, time_sleep: int | float):
        self.time_sleep = time_sleep

    def run(self, context: Context):
        time.sleep(self.time_sleep)


class WaitUntil(Action):
    def __init__(self, condition, timeout=None):
        self.condition = condition
        self.timeout = timeout

    def run(self, context: Context):
        start = time.time()

        while context.running:
            if self.condition.run(context):
                return

            if self.timeout and time.time() - start > self.timeout:
                return


class Loop(Action):
    def __init__(self, actions: list, count=None):
        self.actions = actions
        self.count = count

    def run(self, context: Context):
        interaction = 0

        while self.count is None or interaction < self.count:
            for action in self.actions:
                if not context.running:
                    return
                action.run(context)

            interaction += 1
