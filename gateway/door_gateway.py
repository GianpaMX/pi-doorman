from gpiozero import LED
from time import sleep


class DoorGateway:
    def __init__(self, gpiopin, duration):
        self.duration = duration
        self.led = LED(gpiopin)
        self.led.on()

    def open(self):
        self.led.off()
        sleep(self.duration)
        self.led.on()
