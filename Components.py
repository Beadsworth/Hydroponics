class Component:
    """Component base class -- read state only.  Extend this class for new components"""

    _valid_states = None

    # TODO consider removing element from base class
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def valid_states(self):
        return self._valid_states

    # checks if state is valid.
    @staticmethod
    def check_state(function):
        def wrapper(inst, target_state):
            if target_state not in inst.valid_states:
                raise RuntimeError("Invalid state for " + str(inst.__class__))
            return function(inst, target_state)
        return wrapper


class ArduinoComponent(Component):
    """Component base class -- read state only.  Extend this class for new components"""

    _element_class = None
    _valid_states = None

    # TODO consider removing element from base class
    def __init__(self, element, name):

        super().__init__(name)

        if self.__class__._element_class is None:
            pass
        elif isinstance(element, self.__class__._element_class) is False:
            raise RuntimeError('The element is incompatible with this Component subclass')

        self._element = element

    @property
    def element(self):
        return self._element


if __name__ == '__main__':
    pass
