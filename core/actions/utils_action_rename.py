import time

from core.actions.base_action import Action
from core.actions.halpers.context import Context


class WaitAction(Action):
    def __init__(self, waiting_time: int | float):
        self.waiting_time = waiting_time

    def run(self, context: Context):
        time.sleep(self.waiting_time)


class WaitUntilAction(Action):
    def __init__(self, action: list, actions_true: list, actions_false: list, timeout=0):
        self.action = action[0]
        self.actions_true = actions_true
        self.actions_false = actions_false
        self.timeout = timeout

    def run(self, context: Context):
        start = time.time()

        while context.running:
            if self.action.run(context):
                for a in self.actions_true:
                    if not context.running:
                        break
                    a.run(context)
                break

            if self.timeout != 0 and time.time() - start > self.timeout:
                if self.actions_false:
                    context.running = False
                    return

                for a in self.actions_false:
                    if not context.running:
                        break
                    a.run(context)
                break


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
