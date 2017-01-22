from ArduinoElements import DigitalSensor
from Components.Component import ArduinoComponent


class WaterLevelSensor(ArduinoComponent):

    _element_class = DigitalSensor
    _valid_states = 'FULL', 'EMPTY'

    @property
    def state(self):

        if self.element.state == 'HIGH':
            return 'FULL'
        elif self.element.state == 'LOW':
            return 'EMPTY'
