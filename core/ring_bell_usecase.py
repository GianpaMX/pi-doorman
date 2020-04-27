class RingBellUsecase:
    def __init__(self, door_gateway):
        self.door_gateway = door_gateway

    def execute(self):
        self.door_gateway.ring_bell()
