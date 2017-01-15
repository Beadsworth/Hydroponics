import warnings


class Component:
    """Component base class -- read state only.  Extend this class for new components"""

    _element_class = None
    _states = None

    def __init__(self, element, name):

        if self.__class__._element_class is None:
            pass
        elif isinstance(element, self.__class__._element_class) is False:
            raise RuntimeError('The element is incompatible with this Component subclass')
        self._name = name
        self._element = element

    @property
    def name(self):
        return self._name

    @property
    def element(self):
        return self._element

    # must extend this function for custom services
    @property
    def state(self):
        # return element state
        return self.element.state

    # must extend this function for custom services
    # checks if state is valid.
    @state.setter
    def state(self, target_state):

        if self.__class__._states is None:
            warnings.warn(
                "Component class does not have its own state-setting method!  It must be defined in child class!")

        elif target_state not in self.__class__._states:
            raise RuntimeError("Invalid state for " + str(self.__class__))


class Example(Component):
    """Example class, use as template for other Group child classes."""
    # replace _states with possible set-states
    _states = None

    def __init__(self, name):
        # replace "pass" with inherited function
        pass
        # leave super() alone at end of __init__()
        super().__init__([], name)

    @property
    def state(self):
        # replace None with property
        return None

    @state.setter
    def state(self, target_state):

        # leave fset() along at beginning of @state.setter
        Component.state.fset(self, target_state)
        # replace "pass" with inherited function
        pass


if __name__ == '__main__':
    pass
