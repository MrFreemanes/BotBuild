class Context:
    def __init__(self, callback_running):
        """
        coordinates - координаты переданные действием.
        template - шаблон (пока не используется).
        running - флаг об остановке.
        callback_running - функция/метод для обозначения работающего действия в данный момент.
        """
        self.coordinates = None
        self.template = None
        self.running = True
        self.callback_running = callback_running

    def is_coordinates(self) -> bool:
        return self.coordinates is not None

    def working_node(self, node_id: str):
        if isinstance(node_id, str):
            self.callback_running(node_id)
