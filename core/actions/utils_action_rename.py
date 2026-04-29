import time

from core.actions.base_action import Action
from core.actions.halpers.context import Context


class WaitAction(Action):
    def __init__(self, waiting_time: int | float):
        self.waiting_time = waiting_time

    def run(self, context: Context):
        time.sleep(self.waiting_time)


class WaitUntilAction(Action):
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


class LoopAction(Action):
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
