from pyfirmata import Arduino, util, PWM
import time

default_HIGH_str = 'DEFAULT_HIGH'
default_LOW_str = 'DEFAULT_LOW'
relay_open_str = 'RELAY_OPEN'
relay_closed_str = 'RELAY_CLOSED'
pump_off_str = 'PUMP_OFF'
pump_on_str = 'PUMP_ON'
valve_closed_str = 'VALVE_CLOSED'
valve_open_str = 'VALVE_OPEN'
sublight_off_str = 'SUBLIGHT_OFF'
sublight_on_str = 'SUBLIGHT_ON'
light_off_str = 'LIGHT_OFF'
light_low_str = 'LIGHT_LOW'
light_high_str = 'LIGHT_HIGH'

# TODO change these -- they are backwards
RELAY_OPEN = 0
RELAY_CLOSED = 1

default_modes = {default_LOW_str: 0, default_HIGH_str: 1}
relay_modes = {relay_open_str: RELAY_OPEN, relay_closed_str: RELAY_CLOSED}
pump_modes = {pump_off_str: RELAY_OPEN, pump_on_str: RELAY_CLOSED}
valve_modes = {valve_closed_str: RELAY_OPEN, valve_open_str: RELAY_CLOSED}
sublight_modes = {sublight_off_str: RELAY_OPEN, sublight_on_str: RELAY_CLOSED}
light_modes = {light_off_str: 2, light_low_str: 1, light_high_str: 0}

default_modes_rev = {str(0): default_LOW_str, str(1): default_HIGH_str}
relay_modes_rev = {str(RELAY_OPEN): relay_open_str, str(RELAY_CLOSED): relay_closed_str}
pump_modes_rev = {str(RELAY_OPEN): pump_off_str, str(RELAY_CLOSED): pump_on_str}
valve_modes_rev = {str(RELAY_OPEN): valve_closed_str, str(RELAY_CLOSED): valve_open_str}
sublight_modes_rev = {str(RELAY_OPEN): sublight_off_str, str(RELAY_CLOSED): sublight_on_str}
light_modes_rev = {str(2): light_off_str, str(1): light_low_str, str(0): light_high_str}


class Controller:
    """Board that controls components.  Each board needs its own session.  First initialize controller, then components,
    then connect."""
    def __init__(self, board_addr):
        self.board_addr = board_addr
        self.board = None
        self.it = None
        self.relays = []
        self.loads = []
        self.sensors = []
        self.active = False

        # self.connect()

    def connect(self):
        if self.active:
            print('Already connected!')
            return
        print('Connecting to controller board...')
        self.board = Arduino(self.board_addr)
        self.it = util.Iterator(self.board)
        self.it.start()

        # turn off individual load relays before turning on relay sub-board
        for load in self.loads:
            self.board.digital[load.pin].write(1)
        # turn on relay sub-board, enabling relay control

        time.sleep(0.5)

        for relay in self.relays:
            self.board.digital[relay.pin].write(1)

        #for sensor in self.sensors:
         #   self.board.analog[sensor.pin].enable_reporting

        self.active = True
        print('Connection successful!')

    def disconnect(self):
        self.check_connection()
        print('Disconnecting controller board...')
        self.active = False
        #for sensor in self.sensors:
          #  self.board.analog[sensor.pin].disable_reporting
        # disable all relay sub-boards
        for relay in self.relays:
            self.board.digital[relay.pin].write(0)
        # set all load pins to LOW
        for load in self.loads:
            self.board.digital[load.pin].write(0)

        self.board.exit()
        self.board = None
        self.it = None
        print('Disconnected!')

    def reconnect(self):
        self.check_connection()
        print('Resetting connection...')
        self.disconnect()
        self.connect()

    def check_connection(self):
        if self.active is False:
            raise RuntimeError('Controller not connected!')

    def all_loads_off(self):
        self.check_connection()
        for load in self.loads:
            self.board.digital[load.pin].write(RELAY_OPEN)



# TODO change everything to pin#-type setting.  Let higher abstraction module handle load->number mapping
class Component:
    """Superclass, mostly to prevent adding/removing components while Controller is active."""
    def __init__(self, controller, pin):

        self.controller = controller
        self.pin = pin
        # board must be inactive to initialize and add a load
        if self.controller.active is True:
            raise RuntimeError('Controller already active!  Cannot add more components while board is active.  '
                               'Disconnect before adding components.')


class Load(Component):
    """Digital output pin.  On or Off."""
    def __init__(self, controller, pin, mode_dict=default_modes, mode_dict_rev=default_modes_rev):
        Component.__init__(self, controller, pin)
        self.mode_dict = mode_dict
        self.mode_dict_rev = mode_dict_rev
        # if relay, add to relay list.  All others added to load list
        if mode_dict == relay_modes:
            self.controller.relays.append(self)
        else:
            self.controller.loads.append(self)

    def set_mode(self, target_mode):
        self.controller.check_connection()
        if target_mode not in self.mode_dict:
            raise ValueError('Invalid mode setting for Load!')

        self.controller.board.digital[self.pin].write(self.mode_dict[target_mode])
        return None

    def get_mode(self):
        self.controller.check_connection()
        # find status of pin (0 or 1) and return mode-str
        status = self.controller.board.digital[self.pin].read()
        return self.mode_dict_rev[str(status)]

    def high(self):
        self.set_mode(default_HIGH_str)

    def low(self):
        self.set_mode(default_LOW_str)


class Relay(Load):

    def __init__(self, controller, pin):
        Load.__init__(self, controller, pin, relay_modes, relay_modes_rev)

    def close(self):
        self.set_mode(relay_closed_str)

    def open(self):
        self.set_mode(relay_open_str)


class Pump(Load):

    def __init__(self, controller, pin):
        Load.__init__(self, controller, pin, pump_modes, pump_modes_rev)

    def off(self):
        self.set_mode(pump_off_str)

    def on(self):
        self.set_mode(pump_on_str)


class Valve(Load):

    def __init__(self, controller, pin):
        Load.__init__(self, controller, pin, valve_modes, valve_modes_rev)

    def set_mode(self, target_mode):
        Load.set_mode(self, target_mode)
        self.controller.board.pass_time(5)

    def close(self):
        self.set_mode(valve_closed_str)

    def open(self):
        self.set_mode(valve_open_str)


class Sublight(Load):

    def __init__(self, controller, pin):
        Load.__init__(self, controller, pin, sublight_modes, sublight_modes_rev)

    def off(self):
        self.set_mode(sublight_off_str)

    def on(self):
        self.set_mode(sublight_on_str)


class Light:

    def __init__(self, sublight_a, sublight_b):

        if (type(sublight_a) is not Sublight) or (type(sublight_b) is not Sublight):
            raise TypeError('Lights may only be composed of sublights.')

        if sublight_a == sublight_b:
            raise RuntimeError('The same sublight was listed twice for this Light.')

        self.sublight_a = sublight_a
        self.sublight_b = sublight_b
        self.sublight_switch = self.sublight_a
        self.mode_dict = light_modes
        self.mode_dict_rev = light_modes_rev

    def set_mode(self, target_mode):

        if target_mode not in self.mode_dict:
            raise ValueError('Invalid mode setting for Light!')

        if self.mode_dict[target_mode] is self.mode_dict[light_off_str]:

            self.sublight_a.off()
            self.sublight_b.off()

        elif self.mode_dict[target_mode] is self.mode_dict[light_low_str]:

            if self.sublight_switch is self.sublight_a:
                self.sublight_b.off()
                self.sublight_a.on()
                self.sublight_switch = self.sublight_b
            else:
                self.sublight_a.off()
                self.sublight_b.on()
                self.sublight_switch = self.sublight_a

        elif self.mode_dict[target_mode] is self.mode_dict[light_high_str]:

            self.sublight_a.on()
            self.sublight_b.on()

        else:
            raise RuntimeError('Unexpected mode error for Light!')

        return None

    def get_mode(self):

        mode_a = self.sublight_a.get_mode()
        mode_b = self.sublight_b.get_mode()
        combo = (mode_a, mode_b)

        if sublight_off_str in combo: # if at least one off

            if sublight_on_str not in combo: # neither one is on -> OFF
                return light_off_str
            else:  # at least one is on -> LOW
                return light_low_str

        else:  # neither one is off -> HIGH
            return light_high_str

    def high(self):
        self.set_mode(light_high_str)

    def low(self):
        self.set_mode(light_low_str)

    def off(self):
        self.set_mode(light_off_str)


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
        self.outlet_valve.close()
        self.inlet_valve.close()
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

    # setup
    addr = '/dev/ttyACM0'
    uno = Controller(addr)
    led_red = Sublight(uno, 2)
    led_yellow = Sublight(uno, 3)
    led_green = Sublight(uno, 4)
    led_blue = Sublight(uno, 5)
    led_white1 = Sublight(uno, 6)
    led_white2 = Sublight(uno, 7)

    led_list = [led_red, led_yellow, led_green, led_blue, led_white1, led_white2]

    # run

    try:
        uno.connect()
        time.sleep(2)

        for led in led_list:
            led.off()

        for i in range(20):
            for j in range(len(led_list)):
                led_list[(j+1)%len(led_list)].on()
                time.sleep(0.04)
                led_list[j].off()
                time.sleep(0.01)

    finally:

        uno.disconnect()
        print('Disconnected.')

    print('~~~ Finished! ~~~')
