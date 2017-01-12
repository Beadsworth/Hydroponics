from Components import Component, Light, Valve, Pump, WaterLevelSensor

import warnings
import time


class Group:

    """Group base class -- read state only.  Extend this class for new Groups"""

    _states = None

    def __init__(self, component_list, name):

        self._component_list = []

        for component in component_list:
            if isinstance(component, Component) is False:
                raise RuntimeError('At least one member of the group was not a Component.  Components Only!')
            self._component_list.append(component)

        self._name = name

    @property
    def component_list(self):
        return self._component_list

    @property
    def name(self):
        return self._name

    # must extend this function for custom services
    @property
    def state(self):
        # return dict of states
        status_list = []
        for component in self._component_list:
            status_list.append((str(component.name), str(component.state)))
        return dict(status_list)

    # must extend this function for custom services
    # checks if state is valid.
    @state.setter
    def state(self, target_state):

        if self.__class__._states is None:
            warnings.warn(
                "Group class does not have its own state-setting method!  It must be defined in child class!")

        elif target_state not in self.__class__._states:
            raise RuntimeError("Invalid state for " + str(self.__class__))


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

        elif (status[self._level_sensor.name] == 'FULL') and \
                (status[self._control_valve.name] == 'CLOSED'):  # zone empty, control valve closed
            return 'EMPTY'

        else :  # control valve open, actively filling or draining
            if (status[self._outlet_valve.name] == 'OPEN') and (status[self._pump.name] == 'OFF'):  # drain open, pump off
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
