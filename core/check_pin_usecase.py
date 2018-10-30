class CheckPinUsecase:
    def __init__(self, pins):
        self.pins = pins

    def execute(self, pin):
        return pin in self.pins
