from core.actions.base_action import Action
from core.actions.halpers.context import Context


class IfAction(Action):
    def __init__(self, action: list, actions_true: list, actions_false: list):
        """
        :param action: [Action] возвращающий bool например ImageSearchAction.
        :param actions_true: [Action, ...].
        :param actions_false: [Action, ...].
        """
        self.action = action[0]
        self.actions_true = actions_true
        self.actions_false = actions_false

    def run(self, context: Context) -> None:
        """
        Вызывает self.action.run(context).
        Если True, то вызывает метод run() у объектов из списка actions_true. Иначе - actions_false если они есть.
        """
        if self.action.run(context):
            for a in self.actions_true:
                if not context.running:
                    break
                a.run(context)
        else:
            if not self.actions_false:
                context.running = False
                return

            for a in self.actions_false:
                if not context.running:
                    break
                a.run(context)
