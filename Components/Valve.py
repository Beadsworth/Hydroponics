from ArduinoElements import Relay
from Components.Component import Component, ArduinoComponent

import time


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
