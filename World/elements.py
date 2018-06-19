from World.properties import Name
from World.types import Type


class Element:
    type = None  # type: Type
    properties = []
    string = ""

    def __init__(self, elem_type: Type, properties: list):
        self.type = elem_type
        self.properties += properties
        for prop in self.properties:
            if isinstance(prop, Name):
                self.string = str(prop)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()
