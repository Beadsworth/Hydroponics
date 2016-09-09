from enum import Enum

from HydroIO import RELAY_ON, RELAY_OFF, VALVE_CLOSED, VALVE_OPEN, setPin, getPin


class LightMode(Enum):
    OFF, LOW, HIGH = range(3)


class Pump:
    def __init__(self, pin):
        self.pin = pin
        # self.states = RELAY_OFF

    def set_mode(self, setting):
        if setting not in [RELAY_OFF, RELAY_ON]:
            raise ValueError('Invalid mode setting for pump!')
        setPin(self.pin, setting)


class Valve:
    def __init__(self, pin):
        self.pin = pin
        self.state = VALVE_CLOSED

    def set_mode(self, setting):
        if setting not in [VALVE_CLOSED, VALVE_OPEN]:
            raise ValueError('Invalid mode setting for valve!')
        setPin(self.pin, setting)


class Light:
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pin_switch = self.pin_a
        # self.state = RELAY_OFF

    def set_mode(self, setting):
        if setting == LightMode.HIGH:
            setPin(self.pin_a, RELAY_ON)
            setPin(self.pin_b, RELAY_ON)
        elif setting == LightMode.LOW:
            setPin(self.pin_switch, RELAY_ON)
            if self.pin_switch is self.pin_a:
                self.pin_switch = self.pin_b
            else:
                self.pin_switch = self.pin_a
        elif setting == LightMode.OFF:
            setPin(self.pin_a, RELAY_OFF)
            setPin(self.pin_b, RELAY_OFF)
        else:
            raise ValueError('Invalid mode setting for light!')

    def is_high(self):
        results = [getPin(self.pin_a), getPin(self.pin_b)] # [(true, 1), (false,2)]
        status = map(lambda x: x[0], results)
        values = map(lambda x: x[1], results)
        if False in status:
            raise ValueError

        for value in values:
            if value != RELAY_ON:
                return False

        return True

class Zone:

    def __init__(self, name, control_valve, inlet_valve, outlet_valve, pump):
        self.name = name
        self.control_valve = control_valve
        self.outlet_valve = outlet_valve
        self.inlet_valve = inlet_valve
        self.pump = pump

    def flood(self):
        self.outlet_valve.set_mode(VALVE_CLOSED)
        self.control_valve.set_mode(VALVE_OPEN)
        self.inlet_valve.set_mode(VALVE_OPEN)
        self.pump.set_mode(RELAY_ON)

    def maintain(self):

        self.pump.set_mode(RELAY_OFF)
        self.outlet_valve.set_mode(VALVE_CLOSED)
        self.inlet_valve.set_mode(VALVE_CLOSED)
        self.control_valve.set_mode(VALVE_CLOSED)

    def drain(self):
        self.pump.set_mode(RELAY_OFF)
        self.inlet_valve.set_mode(VALVE_CLOSED)
        self.control_valve.set_mode(VALVE_OPEN)
        self.outlet_valve.set_mode(VALVE_OPEN)

