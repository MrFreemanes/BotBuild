import time

from core.actions.base_action import BaseAction
from core.actions.halpers.context import Context


class WaitAction(BaseAction):
    def __init__(self, waiting_time: int | float, node_id: str = None):
        """
        :param waiting_time: Время остановки.
        """
        super().__init__(node_id)

        self.waiting_time = waiting_time

    def run(self, context: Context) -> None:
        context.working_node(self.node_id)
        time.sleep(self.waiting_time)


class WaitUntilAction(BaseAction):
    def __init__(self, action: list, actions_true: list, actions_false: list, timeout: int = 0, node_id: str = None):
        """
        :param action: [Action] возвращающий bool например ImageSearchAction.
        :param actions_true: [Action, ...].
        :param actions_false: [Action, ...]. Вызывается в случае таймаута.
        :param timeout: Время, через которое, если action не вернут True,
                        выполняется actions_false, если он не пуст.
                        Если timeout = 0, то не учитывается.
        """
        super().__init__(node_id)

        self.action = action[0]
        self.actions_true = actions_true
        self.actions_false = actions_false
        self.timeout = timeout

    def run(self, context: Context) -> None:
        """
        Выполняет action.run(context), пока тот не вернёт True или не истечёт время, переданное в timeout.
        Если время вышло, то вызывает метод run() у объектов из списка actions_false, если они есть.
        """
        start = time.time()
        context.working_node(self.node_id)
        while context.running:
            if self.action.run(context):
                for a in self.actions_true:
                    if not context.running:
                        break
                    a.run(context)
                break

            if self.timeout != 0 and time.time() - start > self.timeout:
                if not self.actions_false:
                    context.running = False
                    return

                for a in self.actions_false:
                    if not context.running:
                        break
                    a.run(context)
                break


class LoopAction(BaseAction):
    def __init__(self, actions: list, count=None, node_id: str = None):
        """
        :param actions: [Action, ...].
        :param count: Кол-во выполнений. Если None, то бесконечно.
        """
        super().__init__(node_id)

        self.actions = actions
        self.count = count

    def run(self, context: Context) -> None:
        """
        Вызов метода run() для действий из списка actions заданное количество раз, если это было указано.
        """
        interaction = 0
        context.working_node(self.node_id)
        while self.count is None or interaction < self.count:
            for action in self.actions:
                if not context.running:
                    return
                action.run(context)

            interaction += 1
