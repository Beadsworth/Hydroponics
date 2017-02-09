from pyfirmata import ArduinoMega, util, Arduino, INPUT, ANALOG
import time

LOW = 0
HIGH = 1
RELAY_OPEN = HIGH
RELAY_CLOSED = LOW


class Controller:
    """Board that controls elements.  Each board needs its own session.  First initialize controller, then elements,
    then connect."""
    def __init__(self, board_addr, board_type='uno'):
        self._board_addr = board_addr
        self._board = None
        self._it = None
        self._elements = []
        self._active = False
        self._board_type = board_type

    @property
    def board(self):
        return self._board

    @property
    def elements(self):
        return self._elements

    @property
    def active(self):
        return self._active

    def connect(self):
        if self._active:
            print('Already connected!')
            return
        print('Connecting to controller board...')

        if self._board_type == 'mega':
            self._board = ArduinoMega(self._board_addr)
        else:
            self._board = Arduino(self._board_addr)

        self._it = util.Iterator(self._board)
        self._it.start()
        self._active = True

        for element in [elem for elem in self._elements if isinstance(elem, ArduinoElement)]:
            # prepare all pin_objs after board connects
            element.prepare()
            # all loads set to 'OFF' before relay board enabled
            if isinstance(element, Relay):
                element.state = 'OFF'

        # turn on relay sub-board, enabling relay control
        time.sleep(0.5)
        self.enable_all_relays()

        # for sensor in self.sensors:
        # self.board.analog[sensor.pin].enable_reporting

        print('Connection successful!')

    def disconnect(self):
        self.check_connection()
        print('Disconnecting controller board...')
        # for sensor in self.sensors:
        #  self.board.analog[sensor.pin].disable_reporting

        # disable all relay sub-boards
        self.disable_all_relays()

        # set all load pins to LOW
        for element in self._elements:
            # all loads set to RELAY_OPEN
            if isinstance(element, Load):
                element.state = 'LOW'

            # set all pin_obj to None
            element._pin_obj = None

        self._it = None
        self._active = False
        self._board.exit()
        self._board = None
        print('Disconnected!')

    def reconnect(self):
        self.check_connection()
        print('Resetting connection...')
        self.disconnect()
        self.connect()

    def check_connection(self):
        if self._active is False:
            raise RuntimeError('Controller not connected!')

    def enable_all_relays(self):
        self.check_connection()
        for element in self._elements:
            if isinstance(element, RelayBoard):
                element.state = 'ENABLE'

    def disable_all_relays(self):
        self.check_connection()
        for element in self._elements:
            if isinstance(element, RelayBoard):
                element.state = 'DISABLE'


class ArduinoElement:
    """Superclass, mostly to prevent adding/removing elements while Controller is active."""
    def __init__(self, controller, pin, name):

        if name in [element.name for element in controller.elements]:
            raise RuntimeError('There is already an element with name: \"' + name + '\"')

        self._controller = controller
        self._pin = pin
        self._name = name

        # board must be inactive to initialize and add a load
        if self._controller.active:
            raise RuntimeError('Controller already active!  Cannot add more elements while board is active.  '
                               'Disconnect before adding elements.')

        self._pin_obj = None
        self._controller.elements.append(self)

    @property
    def controller(self):
        return self._controller

    @property
    def name(self):
        return self._name

    def prepare(self):
        """Initialize pin_obj after board is active"""
        self._controller.check_connection()
        self._pin_obj = self._controller.board.get_pin('d:' + str(self._pin) + ':o')
        self._pin_obj.write(LOW)


class Load(ArduinoElement):
    """Digital output pin.  On or Off."""
    # define states_lookup after states to block inheritance and key collision
    _states = {
        'LOW': LOW,
        'HIGH': HIGH
    }
    _states_lookup = {v: k for k, v in _states.items()}

    @property
    def state(self):
        self._controller.check_connection()
        status = self._pin_obj.read()
        return self._states_lookup[status]

    @state.setter
    def state(self, target_state):
        self._controller.check_connection()
        if target_state not in self.__class__._states:
            raise ValueError('Invalid state setting for Load!')
        self._pin_obj.write(self.__class__._states[target_state])


class RelayBoard(Load):
    # define states_lookup after states to block inheritance and key collision
    _states = {
        'DISABLE': LOW,
        'ENABLE': HIGH
    }
    _states_lookup = {v: k for k, v in _states.items()}
    _states.update(Load._states)


class Relay(Load):
    # define states_lookup after states to block inheritance and key collision
    _states = {
        'ON': RELAY_CLOSED,
        'OFF': RELAY_OPEN
    }
    _states_lookup = {v: k for k, v in _states.items()}
    _states.update(Load._states)


class DigitalSensor(ArduinoElement):
    """Read only Digital Sensor ArduinoElement."""

    def prepare(self):
        """Modify pin object to be a digital input"""
        ArduinoElement.prepare(self)
        # call to parent prepare() takes care of connection checks
        self._pin_obj.mode = INPUT

    @property
    def state(self):
        self._controller.check_connection()
        status = self._pin_obj.read()
        if status is True:
            return 'HIGH'
        else:
            return 'LOW'


class AnalogSensor(ArduinoElement):
    """Read only Analog Sensor ArduinoElement."""
    # TODO check if this class works
    def prepare(self):
        """Modify pin object to be a digital input"""
        ArduinoElement.prepare(self)
        # call to parent prepare() takes care of connection checks
        self._pin_obj.mode = ANALOG

    @property
    def state(self):
        self._controller.check_connection()
        status = self._pin_obj.read()
        return status

if __name__ == '__main__':
    pass
