from core.actions.base_action import Action
from core.actions.halpers.context import Context


class IfAction(Action):
    def __init__(self, action: list, actions_true: list, actions_false: list):
        self.action = action[0]
        self.actions_true = actions_true
        self.actions_false = actions_false

    def run(self, context: Context) -> None:
        if self.action.run(context):
            for a in self.actions_true:
                if not context.running:
                    break
                a.run(context)
        else:
            if self.actions_false:
                context.running = False
                return

            for a in self.actions_false:
                if not context.running:
                    break
                a.run(context)
