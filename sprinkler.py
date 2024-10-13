#!/bin/env python
from gpiozero import DistanceSensor, Buzzer

class Sprinkler:

    def __init__(self, trigger: int, echo: int, relay: int):
        self.relay = Buzzer(relay)
        self.ultrasonic = DistanceSensor(echo=echo, trigger=trigger)

    def read_sensor(self) -> float:
        return self.ultrasonic.distance

    def run_pump(self, duration):
        self.relay.beep(on_time=duration, off_time=1, n=1, background=False)

    def read_volume(self):
        distance = self.read_sensor()
        maximum_distance = 0.2
        fill_percentage = 1 - distance / maximum_distance
        return fill_percentage * 100

if __name__ == '__main__':
    sprinkler = Sprinkler(4, 27, 17)
    print(f'Current fill: {sprinkler.read_volume():0.1f}%')
