from pyfirmata import ArduinoMega, util, PWM, Arduino
import time

default_high_str = 'HIGH'
default_low_str = 'LOW'
relay_off_str = 'RELAY_OFF'
relay_on_str = 'RELAY_ON'
relay_disable_str = 'RELAY_DISABLE'
relay_enable_str = 'RELAY_ENABLE'
load_off_str = 'LOAD_OFF'
load_on_str = 'LOAD_ON'
valve_close_str = 'VALVE_CLOSE'
valve_open_str = 'VALVE_OPEN'
light_off_str = 'LIGHT_OFF'
light_low_str = 'LIGHT_LOW'
light_high_str = 'LIGHT_HIGH'

VALVE_PAUSE = 5

LOW = 0
HIGH = 1
RELAY_OPEN = HIGH
RELAY_CLOSED = LOW

LOAD_STATES = {default_low_str: LOW, default_high_str: HIGH}
RELAY_BOARD_STATES = {relay_disable_str: LOW, relay_enable_str: HIGH}
RELAY_STATES = {relay_on_str: RELAY_CLOSED, relay_off_str: RELAY_OPEN}
VALVE_STATES = {valve_open_str: RELAY_CLOSED, valve_close_str: RELAY_OPEN}
LIGHT_STATES = {light_off_str: 2, light_low_str: 1, light_high_str: 0}


class Controller:
    """Board that controls components.  Each board needs its own session.  First initialize controller, then components,
    then connect."""
    def __init__(self, board_addr):
        self.board_addr = board_addr
        self.board = None
        self.it = None
        self.components = []
        self.active = False

        # self.connect()

    def connect(self):
        if self.active:
            print('Already connected!')
            return
        print('Connecting to controller board...')
        # TODO change back to ArduinoMega
        self.board = Arduino(self.board_addr)
        self.it = util.Iterator(self.board)
        self.it.start()
        self.active = True

        for component in [comp for comp in self.components if isinstance(comp, Component)]:
            # prepare all pin_objs after board connects
            component.prepare()
            # all loads set to RELAY_OPEN before relay board enabled
            if isinstance(component, Relay):
                component.off()

        # turn high relay sub-board, enabling relay control
        time.sleep(0.5)
        self.enable_all_relays()

        #for sensor in self.sensors:
         #   self.board.analog[sensor.pin].enable_reporting

        print('Connection successful!')

    def disconnect(self):
        self.check_connection()
        print('Disconnecting controller board...')
        # for sensor in self.sensors:
        #  self.board.analog[sensor.pin].disable_reporting

        # disable all relay sub-boards
        self.close_all_valves()
        self.disable_all_relays()

        # set all load pins to LOW
        for component in self.components:
            # all loads set to RELAY_OPEN
            if isinstance(component, Load):
                component.low()

            # set all pin_obj to None
            component.pin_obj = None

        self.it = None
        self.active = False
        self.board.exit()
        self.board = None
        print('Disconnected!')

    def reconnect(self):
        self.check_connection()
        print('Resetting connection...')
        self.disconnect()
        self.connect()

    def check_connection(self):
        if self.active is False:
            raise RuntimeError('Controller not connected!')

    def component_name_check(self, name_str):
        if name_str in [component.name for component in self.components]:
            raise RuntimeError('Multiple Components have the same name: \"' + name_str + '\"')

    def enable_all_relays(self):
        self.check_connection()
        for component in self.components:
            if isinstance(component, RelayBoard):
                component.enable()

    def disable_all_relays(self):
        self.check_connection()
        for component in self.components:
            if isinstance(component, RelayBoard):
                component.disable()

    def close_all_valves(self):
        """set all Valves to closed position"""
        self.check_connection()
        for component in self.components:
            if isinstance(component, Valve):
                component.close()

    def open_all_valves(self):
        """set all Valves to closed position"""
        self.check_connection()
        for component in self.components:
            if isinstance(component, Valve):
                component.open()

    def emergency_off(self):
        """turn low loads, on all valves"""
        self.check_connection()
        for component in self.components:
            # skip valves
            if isinstance(component, Valve):
                continue
            # if component attached to relay, but is not a valve
            elif isinstance(component, Relay):
                component.off()
            # for loads that are not valves, relays, or relayboards, set low
            elif isinstance(component, Load) and not isinstance(component, RelayBoard):
                component.low()

        self.close_all_valves()
        self.disable_all_relays()


class Component:
    """Superclass, mostly to prevent adding/removing components while Controller is active."""
    def __init__(self, controller, pin, name):

        controller.component_name_check(name)
        self.controller = controller
        self.pin = pin
        self.name = name

        # board must be inactive to initialize and add a load
        if self.controller.active is True:
            raise RuntimeError('Controller already active!  Cannot add more components while board is active.  '
                               'Disconnect before adding components.')

        self.pin_obj = None
        self.controller.components.append(self)

    def prepare(self):
        """Initialize pin_obj after board is active"""
        self.controller.check_connection()
        self.pin_obj = self.controller.board.get_pin('d:' + str(self.pin) + ':o')
        self.pin_obj.write(LOW)


class Load(Component):
    """Digital output pin.  On or Off."""
    # define states_lookup after states to block inheritance and key collision
    states = LOAD_STATES
    states_lookup = {v: k for k, v in states.items()}

    def set_state(self, target_state):
        self.controller.check_connection()
        if target_state not in self.__class__.states:
            raise ValueError('Invalid state setting for Load!')

        self.pin_obj.write(self.__class__.states[target_state])
        return None

    def get_state(self):
        self.controller.check_connection()
        # find status of pin (0 or 1) and return state-str
        status = self.pin_obj.read()
        # TODO fix this
        return self.states_lookup[status]

    def high(self):
        self.set_state(default_high_str)

    def low(self):
        self.set_state(default_low_str)


class RelayBoard(Load):
    # define states_lookup after states to block inheritance and key collision
    states = RELAY_BOARD_STATES
    states_lookup = {v: k for k, v in states.items()}
    states.update(Load.states)

    def enable(self):
        self.set_state(relay_enable_str)

    def disable(self):
        self.set_state(relay_disable_str)


class Relay(Load):
    # define states_lookup after states to block inheritance and key collision
    states = RELAY_STATES
    states_lookup = {v: k for k, v in states.items()}
    states.update(Load.states)

    def on(self):
        self.set_state(relay_on_str)

    def off(self):
        self.set_state(relay_off_str)


class Valve(Relay):
    # define states_lookup after states to block inheritance and key collision
    states = VALVE_STATES
    states_lookup = {v: k for k, v in states.items()}
    states.update(Relay.states)

    def set_state(self, target_state):
        # if valve already in this state, do nothing
        if target_state == self.get_state():
            return
        else:
            Load.set_state(self, target_state)
            self.controller.board.pass_time(VALVE_PAUSE)

    def open(self):
        self.set_state(valve_open_str)

    def close(self):
        self.set_state(valve_close_str)


class Light:

    states = LIGHT_STATES

    def __init__(self, controller, pin_a, pin_b, name):

        if pin_a == pin_b:
            raise RuntimeError('The same pin was listed twice for this Light.')

        controller.component_name_check(name)

        self.controller = controller
        self.name = name
        self.sublight_a = Relay(controller, pin_a, name + ':A')
        self.sublight_b = Relay(controller, pin_b, name + ':B')
        # dummy variably used for switching a and b -- used in low()
        self.sublight_switch = None

        # TODO assess whether Light object should be included in components list
        # self.controller.components.append(self)

    def set_state(self, target_state):

        self.controller.check_connection()
        if target_state not in Light.states:
            raise ValueError('Invalid state setting for Light!')

        if target_state == light_off_str:

            self.sublight_a.off()
            self.sublight_b.off()

        elif target_state == light_low_str:

            # switch objects between a and b, turn on a, turn off b ALWAYS
            self.sublight_switch = self.sublight_a
            self.sublight_a = self.sublight_b
            self.sublight_b = self.sublight_switch
            self.sublight_switch = None

            self.sublight_a.on()
            self.sublight_b.off()

        elif target_state == light_high_str:

            self.sublight_a.on()
            self.sublight_b.on()

        else:
            raise RuntimeError('Unexpected state error for Light!')

        return None

    def get_state(self):

        state_a = self.sublight_a.get_state()
        state_b = self.sublight_b.get_state()
        combo = (state_a, state_b)

        if relay_off_str in combo:
            # if at least one low...

            if relay_on_str not in combo:
                # neither one is high -> OFF
                return light_off_str
            else:
                # at least one is high -> LOW
                return light_low_str

        else:
            # neither one is low -> HIGH
            return light_high_str

    def high(self):
        self.set_state(light_high_str)

    def low(self):
        self.set_state(light_low_str)

    def off(self):
        self.set_state(light_off_str)


class Zone:

    def __init__(self, name, control_valve, inlet_valve, outlet_valve, pump):
        self.name = name
        self.control_valve = control_valve
        self.outlet_valve = outlet_valve
        self.inlet_valve = inlet_valve
        self.pump = pump

    def fill(self):
        self.outlet_valve.close()
        self.control_valve.open()
        self.inlet_valve.open()
        self.pump.on()

    def maintain(self):

        self.pump.off()
        self.inlet_valve.close()
        self.outlet_valve.close()
        self.control_valve.close()

    def drain(self):
        self.pump.off()
        self.inlet_valve.close()
        self.control_valve.open()
        self.outlet_valve.open()

    def flood(self, dur_in_minutes):
        self.fill()
        # time.sleep(fill_time)
        self.maintain()
        # time.sleep(dur_in_minutes - (fill_time + drain_time))
        self.drain()
        # time.sleep(drain_time)
        self.maintain()


if __name__ == '__main__':
    pass

