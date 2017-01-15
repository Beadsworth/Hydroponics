from Components import Component

import warnings


class Group:

    """Group base class -- read state only.  Extend this class for new Groups.  Multiple components/groups"""

    _states = None

    def __init__(self, component_list, name):

        self._component_list = []

        for component in component_list:
            # if component is not Component class or another Group
            if (isinstance(component, Component) is False) and (isinstance(component, Group) is False):
                raise RuntimeError('At least one member of the group was invalid.  Components and Groups Only!')

            self._component_list.append(component)

        self._name = name

    @property
    def component_list(self):
        return self._component_list

    @property
    def name(self):
        return self._name

    # must extend this function for custom services
    @property
    def state(self):
        # return dict of states
        status_list = []
        for component in self._component_list:
            status_list.append((str(component.name), str(component.state)))
        return dict(status_list)

    # must extend this function for custom services
    # checks if state is valid.
    @state.setter
    def state(self, target_state):

        if self.__class__._states is None:
            warnings.warn(
                "Group class does not have its own state-setting method!  It must be defined in child class!")

        elif target_state not in self.__class__._states:
            raise RuntimeError("Invalid state for " + str(self.__class__))


class Example(Group):
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
        Group.state.fset(self, target_state)
        # replace "pass" with inherited function
        pass


if __name__ == '__main__':
    pass
