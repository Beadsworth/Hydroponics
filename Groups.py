class Valve(Relay):
    # define states_lookup after states to block inheritance and key collision
    states = VALVE_STATES.copy()
    states_lookup = {v: k for k, v in states.items()}
    states.update(Relay.states)

    def set_state(self, target_state):
        # if valve already in this state, do nothing
        if target_state == self.get_state():
            return
        else:
            Load.set_state(self, target_state)
            # only pause if valve state is called
            if target_state in VALVE_STATES:
                self.controller.board.pass_time(VALVE_PAUSE)

    def open(self):
        self.set_state(valve_open_str)

    def close(self):
        self.set_state(valve_close_str)


class Light:

    states = LIGHT_STATES.copy()

    def __init__(self, controller, pin_a, pin_b, name):

        if pin_a == pin_b:
            raise RuntimeError('The same pin was listed twice for this Light.')

        controller.element_name_check(name)

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