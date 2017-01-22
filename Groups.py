from Components import Component


class Group:

    """Group base class -- read state only.  Extend this class for new Groups.  Multiple components/groups"""

    _valid_states = 'Hi', 'Ho'

    def __init__(self, component_list, name):

        self._component_list = []

        for component in component_list:
            # if component is not Component class or another Group
            if (isinstance(component, Component) is False) and (isinstance(component, Group) is False):
                raise RuntimeError('At least one member of the group was invalid.  Components and Groups Only!')

            self._component_list.append(component)

        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def component_list(self):
        return self._component_list

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


if __name__ == '__main__':
    pass
