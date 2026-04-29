from config.config import Status
from core.actions.halpers.context import Context
from core.workers.base_worker import BaseWorker


class Worker(BaseWorker):
    @BaseWorker.register_task('run_bot')
    def run_bot(self) -> None:
        context = Context()
        print(self.item.params)
        for params in self.item.params:
            if not context.running:
                self.send_result((), status=Status.ERROR, text_error='Бот завершился раньше')
                break
            params.run(context)
        self.send_result((), status=Status.DONE)