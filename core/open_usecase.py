class OpenUsecase:
    def __init__(self, pins, door_gateway):
        self.pins = pins
        self.door_gateway = door_gateway

    def execute(self, pin):
        if pin in self.pins: self.door_gateway.open()
