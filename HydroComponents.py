from Components import Component
from ArduinoElements import Relay, DigitalSensor

import time


class Pump(Component):

    _element_class = Relay
    _states = 'ON', 'OFF'

    @property
    def state(self):
        status = super().state

        if status == 'ON':
            return 'ON'
        elif status == 'OFF':
            return 'OFF'
        else:
            return 'ERROR'

    @state.setter
    def state(self, target_state):
        # check if valid state
        Component.state.fset(self, target_state)

        if target_state == 'ON':
            self.element.state = 'ON'
        elif target_state == 'OFF':
            self.element.state = 'OFF'
        else:
            pass


class Light(Component):

    _element_class = Relay
    _states = 'ON', 'OFF'

    @property
    def state(self):
        status = super().state

        if status == 'ON':
            return 'ON'
        elif status == 'OFF':
            return 'OFF'
        else:
            return 'ERROR'

    @state.setter
    def state(self, target_state):
        # check if valid state
        Component.state.fset(self, target_state)

        if target_state == 'ON':
            self.element.state = 'ON'
        elif target_state == 'OFF':
            self.element.state = 'OFF'
        else:
            pass


class Valve(Component):

    _element_class = Relay
    _states = 'OPEN', 'CLOSED'
    _VALVE_PAUSE = 5

    @property
    def state(self):
        status = super().state

        if status == 'ON':
            return 'OPEN'
        elif status == 'OFF':
            return 'CLOSED'
        else:
            return 'ERROR'

    @state.setter
    def state(self, target_state):
        # check if valid state
        Component.state.fset(self, target_state)

        if self.state == target_state:
            return

        if target_state == 'OPEN':
            self.element.state = 'ON'
        elif target_state == 'CLOSED':
            self.element.state = 'OFF'
        else:
            pass

        time.sleep(Valve._VALVE_PAUSE)


class WaterLevelSensor(Component):

    _element_class = DigitalSensor
    _states = 'FULL', 'EMPTY'

    @property
    def state(self):
        status = super().state

        if status == 'HIGH':
            return 'FULL'
        elif status == 'LOW':
            return 'EMPTY'
        else:
            return 'ERROR'


if __name__ == '__main__':
    pass
