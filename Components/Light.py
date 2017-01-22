from ArduinoElements import Relay
from Components.Component import Component, ArduinoComponent


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
