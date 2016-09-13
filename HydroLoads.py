from HydroIO import set_pin, get_pin


pump_off_str = 'PUMP_OFF'
pump_on_str = 'PUMP_ON'
valve_closed_str = 'VALVE_CLOSED'
valve_open_str = 'VALVE_OPEN'
sublight_off_str = 'SUBLIGHT_OFF'
sublight_on_str = 'SUBLIGHT_ON'
light_off_str = 'LIGHT_OFF'
light_low_str = 'LIGHT_LOW'
light_high_str = 'LIGHT_HIGH'


pump_modes = {pump_off_str: 0, pump_on_str: 1}
valve_modes = {valve_closed_str: 0, valve_open_str: 1}
sublight_modes = {sublight_off_str: 0, sublight_on_str: 1}
light_modes = {light_off_str: 0, light_low_str: 1, light_high_str: 2}


def check_if_successful(status):

    if status[0] is False:
        raise RuntimeError('Arduino communication failed!')


class Load:

    def __init__(self, pin, mode_dict):

        self.pin = pin
        self.mode_dict = mode_dict

    def set_mode(self, target_mode):

        if target_mode not in self.mode_dict:
            raise ValueError('Invalid mode setting for Load!')

        status = set_pin(self.pin, self.mode_dict[target_mode])
        check_if_successful(status)
        return None

    def get_mode(self):

        status = get_pin(self.pin)
        check_if_successful(status)
        return status[1]    # returns 0 or 1


class Pump(Load):

    def __init__(self, pin):
        Load.__init__(self, pin, pump_modes)

    def set_mode(self, target_mode):
        Load.set_mode(self, target_mode)

    def get_mode(self):

        current_mode = Load.get_mode(self)
        if current_mode is self.mode_dict[pump_off_str]:
            return pump_off_str
        elif current_mode is self.mode_dict[pump_on_str]:
            return pump_on_str
        else:
            raise RuntimeError('Pump get_mode failed!')

    def off(self):
        self.set_mode(pump_off_str)

    def on(self):
        self.set_mode(pump_on_str)


class Valve(Load):

    def __init__(self, pin):
        Load.__init__(self, pin, valve_modes)

    def set_mode(self, target_mode):
        Load.set_mode(self, target_mode)

    def get_mode(self):

        current_mode = Load.get_mode(self)
        if current_mode is self.mode_dict[valve_closed_str]:
            return valve_closed_str
        elif current_mode is self.mode_dict[valve_open_str]:
            return valve_open_str
        else:
            raise RuntimeError('Valve get_mode failed!')

    def close(self):
        self.set_mode(valve_closed_str)

    def open(self):
        self.set_mode(valve_open_str)


class Sublight(Load):

    def __init__(self, pin):
        Load.__init__(self, pin, sublight_modes)

    def set_mode(self, target_mode):
        Load.set_mode(self, target_mode)

    def get_mode(self):

        current_mode = Load.get_mode(self)
        if current_mode is self.mode_dict[sublight_off_str]:
            return sublight_off_str
        elif current_mode is self.mode_dict[sublight_on_str]:
            return sublight_on_str
        else:
            raise RuntimeError('SubLight get_mode failed!')

    def off(self):
        self.set_mode(sublight_off_str)

    def on(self):
        self.set_mode(sublight_on_str)


class Light:

    def __init__(self, sublight_a, sublight_b):
        self.sublight_a = sublight_a
        self.sublight_b = sublight_b
        self.sublight_switch = self.sublight_a
        self.mode_dict = light_modes

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
