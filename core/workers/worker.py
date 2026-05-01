from config.config import Status
from core.actions.halpers.context import Context
from core.workers.base_worker import BaseWorker


class Worker(BaseWorker):
    @BaseWorker.register_task('run_bot')
    def run_bot(self) -> None:
        context = Context(self.working_action)
        for action in self.item.params:
            if not context.running:
                self.send_result((), status=Status.ERROR, text_error='Бот завершился раньше')
                break
            action.run(context)
        self.send_result((), status=Status.DONE)

    def working_action(self, node_id: str) -> None:
        self.send_result(node_id, status=Status.RUN)
