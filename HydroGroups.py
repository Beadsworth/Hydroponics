from Components import Component, ArduinoComponent
from Groups import Group
from HydroComponents import Light, Valve, Pump, WaterLevelSensor

import time
import warnings


class Arduino(Group):
    """Arduino class, use for Arduino startup and higher functions."""
    # replace _states with possible set-states
    _valid_states = "CONNECTED", "DISCONNECTED", "RECONNECTED"

    # item_list can contain groups or components
    def __init__(self, item_list, name):

        # basic checks and initialization
        super().__init__(item_list, name)

        self._item_list = []

        def controller_search(check):
            # if component, return element.controller
            if isinstance(check, ArduinoComponent):
                self._item_list.append(check.element.controller)
            # if group, call controller search on every item in group
            elif isinstance(check, Group):
                for component in check.component_list:
                    controller_search(component)
            # unexpected behavior
            else:
                raise RuntimeError("Unexpected behavior.  Item was not Component or Group object.")

        # self._item_list should have all child components by this point.
        # check to make sure all controllers are the same.

        for item in item_list:
            controller_search(item)

        def all_same(check_list):
            return all(x == check_list[0] for x in check_list)

        if all_same(self._item_list) is False:
            raise RuntimeError("Arduino class must have all child items on same Arduino board!")

        self._controller = self._item_list[0]
        del self._item_list

    @property
    def state(self):

        if self._controller.active is True:
            return "CONNECTED"
        elif self._controller.active is False:
            return "DISCONNECTED"

    @state.setter
    @Group.check_state
    def state(self, target_state):

        if target_state == "CONNECTED":
            self._controller.connect()
        elif target_state == "DISCONNECTED":
            self._controller.disconnect()
        elif target_state == "RECONNECTED":
            self._controller.reconnect()


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


class FloodZone(Group):

    _valid_states = 'FILL', 'DRAIN', 'IDLE'

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

        if self._level_sensor.state == 'FULL':
            return 'FULL'

        # level sensor not full -- must be filling or draining or just empty
        else:
            # zone empty, control valve closed
            if self._control_valve.state == 'CLOSED':
                return 'EMPTY'

            # control valve open, either draining or filling
            else:
                # if drain open, pump off, and control valve open
                if (self._outlet_valve.state == 'OPEN') and (self._pump.state == 'OFF'):
                    return 'DRAINING'
                # outlet closed, inlet open, pump on
                elif (self._outlet_valve.state == 'CLOSED') and (self._inlet_valve.state == 'OPEN') \
                        and (self._pump.state == 'ON'):
                    return 'FILLING'
                else:
                    return 'UNEXPECTED_BEHAVIOR'

    @state.setter
    @Group.check_state
    def state(self, target_state):

        if target_state == 'FILL':
            self.fill()
        elif target_state == 'DRAIN':
            self.drain()
        elif target_state == 'IDLE':
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
