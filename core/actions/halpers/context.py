class Context:
    def __init__(self):
        """
        coordinates - координаты переданные действием.
        template - шаблон (пока не используется).
        running - флаг об остановке.
        """
        self.coordinates = None
        self.template = None
        self.running = True

    def is_coordinates(self) -> bool:
        return self.coordinates is not None
