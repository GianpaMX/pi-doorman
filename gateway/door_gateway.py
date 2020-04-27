import sched
import threading
from time import sleep
from time import time

from gpiozero import LED, Button


class DoorGateway:
    def __init__(self, latch_pin, latch_release_duration, bell_pin, door_button_pin):
        self.duration = latch_release_duration
        self.latch = LED(latch_pin)
        self.latch.on()

        self.when_door_button_pressed = None

        self.bell = LED(bell_pin)
        self.door_button = Button(door_button_pin)
        self.door_button.when_pressed = self.__when_door_button_pressed

        self.flags = 0x0
        self.scheduler = sched.scheduler(time, sleep)
        self.scheduler.enter(0.1, 1, self.__check_flag, (self.scheduler,))

        t = threading.Thread(target=self.scheduler.run)
        t.start()

    def __when_door_button_pressed(self):
        self.flags |= 0x1

    def __check_flag(self, new_scheduler):
        if self.flags & 0x1:
            self.flags = 0x2
        elif self.flags & 0x2:
            self.flags = 0x0
            if self.when_door_button_pressed is not None:
                self.when_door_button_pressed()

        self.scheduler.enter(0.1, 1, self.__check_flag, (new_scheduler,))

    def open(self):
        self.latch.off()
        sleep(self.duration)
        self.latch.on()

    def ring_bell(self):
        self.bell.on()
        sleep(2)
        self.bell.off()
