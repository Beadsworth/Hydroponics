from Components.Light import Light
from Groups.Group import Group


class SuperLight(Group):

    _valid_states = 'OFF', 'LOW', 'HIGH'

    def __init__(self, light_a, light_b, name):

        if (isinstance(light_a, Light) is False) or (isinstance(light_b, Light) is False):
            raise TypeError("SuperLight must be composed of Lights.")
        self._light_a = light_a
        self._light_b = light_b
        # dummy variable for switching
        self._switch = 0
        super().__init__([light_a, light_b], name)

    @property
    def state(self):
        state_a = self._light_a.state
        state_b = self._light_b.state

        count = sum((state_a == 'ON', state_b == 'ON'))

        if count == 2:
            return 'HIGH'
        elif count == 1:
            return 'LOW'
        elif count == 0:
            return 'OFF'

    @state.setter
    @Group.check_state
    def state(self, target_state):

        if target_state == 'HIGH':
            self._light_a.state = 'ON'
            self._light_b.state = 'ON'
        elif target_state == 'LOW':
            if self._switch == 0:
                self._light_b.state = 'OFF'
                self._light_a.state = 'ON'
            else:
                self._light_a.state = 'OFF'
                self._light_b.state = 'ON'

            self._switch = int((self._switch + 1) % 2)
        elif target_state == 'OFF':
            self._light_a.state = 'OFF'
            self._light_b.state = 'OFF'
