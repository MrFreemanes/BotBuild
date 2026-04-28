from core.actions.base_action import Action
from core.actions.halpers.context import Context


class If(Action):
    def __init__(self, condition, action_true: list, action_false: list | None = None):
        self.condition = condition
        self.action_true = action_true
        self.action_false = action_false

    def run(self, context: Context) -> None:
        if self.condition.run(context):
            for a in self.action_true:
                if not context.running:
                    break
                a.run(context)
        else:
            if self.action_false is None:
                context.running = False
                return

            for a in self.action_false:
                if not context.running:
                    break
                a.run(context)
