from Components.Component import ArduinoComponent
from Groups.Group import Group


class Arduino(Group):
    """Arduino class, use for Arduino startup and higher functions."""
    # replace _states with possible set-states
    _valid_states = "CONNECTED", "DISCONNECTED", "RECONNECTED"

    # item_list can contain groups or components
    def __init__(self, item_list, name):

        # basic checks and initialization
        super().__init__(item_list, name)

        self._item_list = []

        def controller_search(check):
            # if component, return element.controller
            if isinstance(check, ArduinoComponent):
                self._item_list.append(check.element.controller)
            # if group, call controller search on every item in group
            elif isinstance(check, Group):
                for component in check.component_list:
                    controller_search(component)
            # unexpected behavior
            else:
                raise RuntimeError("Unexpected behavior.  Item was not Component or Group object.")

        # self._item_list should have all child components by this point.
        # check to make sure all controllers are the same.

        for item in item_list:
            controller_search(item)

        def all_same(check_list):
            return all(x == check_list[0] for x in check_list)

        if all_same(self._item_list) is False:
            raise RuntimeError("Arduino class must have all child items on same Arduino board!")

        self._controller = self._item_list[0]
        del self._item_list

    @property
    def state(self):

        if self._controller.active is True:
            return "CONNECTED"
        elif self._controller.active is False:
            return "DISCONNECTED"

    @state.setter
    @Group.check_state
    def state(self, target_state):

        if target_state == "CONNECTED":
            self._controller.connect()
        elif target_state == "DISCONNECTED":
            self._controller.disconnect()
        elif target_state == "RECONNECTED":
            self._controller.reconnect()
