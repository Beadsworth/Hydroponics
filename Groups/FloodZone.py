from Components.Pump import Pump
from Components.Valve import Valve
from Components.WaterLevelSensor import WaterLevelSensor
from Groups.Group import Group

from Trigger import OverflowTrigger

import time
import warnings


class FloodZone(Group):

    _valid_states = 'FILL', 'DRAIN', 'IDLE'

    def __init__(self, control_valve, inlet_valve, outlet_valve, pump, overflow_sensor, status_sensor, name):

        assert isinstance(control_valve, Valve)
        assert isinstance(inlet_valve, Valve)
        assert isinstance(outlet_valve, Valve)
        assert isinstance(pump, Pump)
        assert isinstance(overflow_sensor, WaterLevelSensor)

        self._name = name
        self._control_valve = control_valve
        self._inlet_valve = inlet_valve
        self._outlet_valve = outlet_valve
        self._pump = pump
        self._overflow_sensor = overflow_sensor
        self._status_sensor = status_sensor

        super().__init__([control_valve, inlet_valve, outlet_valve, pump, overflow_sensor, status_sensor], name)
        self.add_trigger(OverflowTrigger(self))

    @property
    def state(self):
        # TODO: fix for new sensor
        if self._overflow_sensor.state == 'FULL':
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
        if self._overflow_sensor.state == 'FULL':
            # remeasure 5 times, if fail once more, stop and give warning
            temp = []
            for i in range(5):
                temp.append(self._overflow_sensor.state)
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
