from Groups import Group
from HydroComponents import Light, Valve, Pump, WaterLevelSensor

import time
import warnings


class Arduino(Group):
    """Arduino class, use for Arduino startup and higher functions."""
    # replace _states with possible set-states
    _states = None

    def __init__(self, name):
        # replace "pass" with inherited function
        pass
        # leave super() alone at end of __init__()
        super().__init__([], name)

    @property
    def state(self):
        # replace None with property
        return None

    @state.setter
    def state(self, target_state):
        # leave fset() along at beginning of @state.setter
        Group.state.fset(self, target_state)
        # replace "pass" with inherited function
        pass


class SuperLight(Group):

    _states = 'OFF', 'LOW', 'HIGH'

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
        else:
            return 'ERROR'

    @state.setter
    def state(self, target_state):

        Group.state.fset(self, target_state)

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
        else:  # 'OFF'
            self._light_a.state = 'OFF'
            self._light_b.state = 'OFF'


class FloodZone(Group):

    _states = 'FILL', 'DRAIN', 'IDLE'

    def __init__(self, control_valve, inlet_valve, outlet_valve, pump, level_sensor, name):

        assert isinstance(control_valve, Valve)
        assert isinstance(inlet_valve, Valve)
        assert isinstance(outlet_valve, Valve)
        assert isinstance(pump, Pump)
        assert isinstance(level_sensor, WaterLevelSensor)

        self._name = name
        self._control_valve = control_valve
        self._inlet_valve = inlet_valve
        self._outlet_valve = outlet_valve
        self._pump = pump
        self._level_sensor = level_sensor

        super().__init__([control_valve, inlet_valve, outlet_valve, pump, level_sensor], name)

    @property
    def state(self):

        status = super().state

        if status[self._level_sensor.name] == 'FULL':
            return 'FULL'

        elif (status[self._level_sensor.name] == 'EMPTY') and \
                (status[self._control_valve.name] == 'CLOSED'):  # zone empty, control valve closed
            return 'EMPTY'

        else:  # control valve open, actively filling or draining
            # if drain open and pump off
            if (status[self._outlet_valve.name] == 'OPEN') and (status[self._pump.name] == 'OFF'):
                return 'DRAINING'
            elif (status[self._outlet_valve.name] == 'CLOSED') and (status[self._pump.name] == 'ON') \
                    and (status[self._inlet_valve.name] == 'OPEN'):  # outlet closed, inlet open, pump on
                return 'FILLING'

    @state.setter
    def state(self, target_state):

        Group.state.fset(self, target_state)

        if target_state == 'FILL':
            self.fill()
        elif target_state == 'DRAIN':
            self.drain()
        else:  # 'IDLE'
            self.idle()

    def fill(self):
        # check if already full
        if self._level_sensor.state == 'FULL':
            # remeasure 5 times, if fail once more, stop and give warning
            temp = []
            for i in range(5):
                temp.append(self._level_sensor.state)
                time.sleep(0.2)
            # if at least one occurrence of 'FULL'
            if 'FULL' in temp:
                warnings.warn("Water level sensor detects zone is full!  Aborting 'FILL' operation.")
                return

        self._outlet_valve.state = 'CLOSED'
        self._control_valve.state = 'OPEN'
        self._inlet_valve.state = 'OPEN'
        self._pump.state = 'ON'

    def idle(self):

        self._pump.state = 'OFF'
        self._inlet_valve.state = 'CLOSED'
        self._outlet_valve.state = 'CLOSED'
        self._control_valve.state = 'CLOSED'

    def drain(self):
        self._pump.state = 'OFF'
        self._inlet_valve.state = 'CLOSED'
        self._control_valve.state = 'OPEN'
        self._outlet_valve.state = 'OPEN'


if __name__ == '__main__':
    pass
