from gpiozero import LED
from time import sleep


class DoorGateway:
    def __init__(self, gpiopin, duration):
        self.gpiopin = gpiopin
        self.duration = duration

    def open(self):
        led = LED(self.gpiopin)
        led.on()
        sleep(self.duration)
        led.off()
