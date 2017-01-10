from Elements import Load, Relay, DigitalSensor, AnalogSensor

import time
import warnings


class Component:
    """Component base class -- read state only.  Extend this class for new components"""

    _component_class = None

    def __init__(self, element, name):

        if self.__class__._component_class is None:
            pass
        elif isinstance(element, self.__class__._component_class) is False:
            raise RuntimeError('The element is incompatible with this Component subclass')
        self._element = element
        self._name = name

    @property
    def element(self):
        return self._element

    @property
    def name(self):
        return self._name

    # must extend this function for custom services
    @property
    def state(self):
        return self.element.state

    # must extend this function for custom services
    # does nothing
    @state.setter
    def state(self, target_state):
        warnings.warn("Component class does not have its own state-setting method!  It must be defined in child class!")

    # if exception is thrown, element is disconnected
    @property
    def active(self):
        temp = None
        try:
            temp = self.element
            print(str(self.element.name) + 'has responded... probably connected')
            return True
        except Exception:
            print('Exception thrown... ' + str(self.element.name) + ' probably not connected!')
            return False
        finally:
            del temp


class Pump(Component):

    _component_class = Relay
    _states = {
        'ON': 'ON',
        'OFF': 'OFF'
    }
    _states_lookup = {v: k for k, v in _states.items()}

    @property
    def state(self):
        status = super().state
        return self._states_lookup[status]

    @state.setter
    def state(self, target_state):
        self.element.state = self.__class__._states[target_state]


class Light(Component):

    _component_class = Relay
    _states = {
        'ON': 'ON',
        'OFF': 'OFF'
    }
    _states_lookup = {v: k for k, v in _states.items()}

    @property
    def state(self):
        status = super().state
        return self._states_lookup[status]

    @state.setter
    def state(self, target_state):
        self.element.state = self.__class__._states[target_state]


class Valve(Component):

    _component_class = Relay
    _states = {
        'OPEN': 'ON',
        'CLOSED': 'OFF'
    }
    _states_lookup = {v: k for k, v in _states.items()}

    _VALVE_PAUSE = 5

    @property
    def state(self):
        status = super().state
        return self._states_lookup[status]

    @state.setter
    def state(self, target_state):
        # if already in that state, do not pause.  state.setter is always called.
        if target_state == self.state:
            self.element.state = self.__class__._states[target_state]
        else:
            self.element.state = self.__class__._states[target_state]
            time.sleep(Valve._VALVE_PAUSE)


class WaterLevelSensor(Component):

    _component_class = DigitalSensor
    _states = {
        'FULL': 'HIGH',
        'EMPTY': 'LOW'
    }
    _states_lookup = {v: k for k, v in _states.items()}

    @property
    def state(self):
        status = super().state
        return self._states_lookup[status]
