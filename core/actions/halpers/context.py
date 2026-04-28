class Context:
    def __init__(self):
        self.coordinates = None
        self.template = None
        self.running = True

    def is_coordinates(self) -> bool:
        return self.coordinates is not None
