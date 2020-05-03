class RingBellUsecase:
    def __init__(self, door_gateway, notifications_gateway, token):
        self.door_gateway = door_gateway
        self.notifications_gateway = notifications_gateway
        self.token = token

    def execute(self):
        self.door_gateway.ring_bell()
        self.notifications_gateway.send(self.token)
