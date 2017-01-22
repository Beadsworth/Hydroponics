from Components import Component, ArduinoComponent
from ArduinoElements import Relay, DigitalSensor

import time


class Pump(ArduinoComponent):

    _element_class = Relay
    _valid_states = 'ON', 'OFF'

    @property
    def state(self):

        if self.element.state == 'ON':
            return 'ON'
        elif self.element.state == 'OFF':
            return 'OFF'

    @state.setter
    @Component.check_state
    def state(self, target_state):

        if target_state == 'ON':
            self.element.state = 'ON'
        elif target_state == 'OFF':
            self.element.state = 'OFF'


class Light(ArduinoComponent):

    _element_class = Relay
    _valid_states = 'ON', 'OFF'

    @property
    def state(self):

        if self.element.state == 'ON':
            return 'ON'
        elif self.element.state == 'OFF':
            return 'OFF'

    @state.setter
    @Component.check_state
    def state(self, target_state):

        if target_state == 'ON':
            self.element.state = 'ON'
        elif target_state == 'OFF':
            self.element.state = 'OFF'


class Valve(ArduinoComponent):

    _element_class = Relay
    _valid_states = 'OPEN', 'CLOSED'
    _VALVE_PAUSE = 5

    @property
    def state(self):

        if self.element.state == 'ON':
            return 'OPEN'
        elif self.element.state == 'OFF':
            return 'CLOSED'

    @state.setter
    @Component.check_state
    def state(self, target_state):

        if self.state == target_state:
            return

        if target_state == 'OPEN':
            self.element.state = 'ON'
        elif target_state == 'CLOSED':
            self.element.state = 'OFF'

        time.sleep(Valve._VALVE_PAUSE)


class WaterLevelSensor(ArduinoComponent):

    _element_class = DigitalSensor
    _valid_states = 'FULL', 'EMPTY'

    @property
    def state(self):

        if self.element.state == 'HIGH':
            return 'FULL'
        elif self.element.state == 'LOW':
            return 'EMPTY'


import datetime


class Clock(Component):

    @property
    def state(self):
        """Return current clock time (datetime object), to the nearest second."""
        now = datetime.datetime.now().replace(microsecond=0)
        return now

if __name__ == '__main__':
    pass
