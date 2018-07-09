from World.interactions import Interaction
from World.properties import Name
from World.statics import ElementParams
from World.types import Type

from Grammar.actions import Terminals


class Element:
    type = Type()     # type: Type
    properties = []   # list of Non-Changeable properties (unlike status)
    stats = {}        # @autofill dict key: status.name, value: status object is changeable throughout the game
    memory = []       # list of Interactions
    name = ""         # element's name

    def __init__(self, elem_type, name: str, properties: list=None):
        # set 'type'
        self.type = elem_type()

        # set (or add 'properties' to pre-defined ones in the world instantiation)
        # self.properties += properties

        # reset 'memory'
        self.memory = []

        self.name = name

        # reset and fill stats dict: (status.name) -> status object
        # self.stats = {}
        # for status_class in self.type.status_classes:
        #     status_obj = status_class()
        #     self.stats[status_obj.name] = status_obj
        #
        # # set 'name' property automatically
        # for prop in self.properties:
        #     if isinstance(prop, Name):
        #         self.name = str(prop)

    def remember(self, action: Terminals, receivers: list) -> None:
        """
        Create and store an interaction into the memory's list
        :param action: Action to be remembered
        :param receivers: Elements the 'action' is being done on them
        :return: Nothing, method just stores in the memory
        """
        interact = Interaction(action=action, doers=[self], receivers=receivers)
        self.memory.insert(0, interact)

    def short_memory(self) -> list:
        """
        Retrieve short version of memory (most recent ones) using 'short_term_memory_length' variable
        :return: list
        """
        if len(self.memory) > ElementParams.short_term_memory_length:
            return self.memory[:ElementParams.short_term_memory_length]
        else:
            return self.memory

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name and self.properties == other.properties

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
