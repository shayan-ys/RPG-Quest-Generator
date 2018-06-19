from World.elements import Element
from World.tags import ActionTags
from World.types import Type

from Grammar.actions import Terminals


class World:
    from World.Instances import Everquest
    elements = Everquest.elements

    # def parse_quest(self, quest: Node):
    #     for action in quest.flatten:
    #         print(action)
    #         if isinstance(action, Terminals):
    #             elem = self.elements.find(action=action)
    #             print(elem.properties[0].name)
    #
    #         print('---')

    actions_map = {}

    def __init__(self):
        for element in self.elements:
            if not isinstance(element, Element):
                continue
            for tag in element.type.tags:
                if isinstance(tag, ActionTags):
                    act = tag.action
                    if act in self.actions_map:
                        self.actions_map[act].append(element)
                    else:
                        self.actions_map[act] = [element]

    def find(self, action: Terminals) -> Type:
        if action in self.actions_map and len(self.actions_map[action]):
            elem = self.actions_map[action].pop(0)
            self.actions_map[action].append(elem)
            return elem
        return None

    def print__actions_map(self) -> str:
        if self.actions_map:
            return_str = '{'
            for action, elems in self.actions_map.items():
                return_str += '\n\t%-11s: %s' % (str(action.name), str(elems))
            return_str += '\n}'
            return return_str
        else:
            return '{}'

    def __str__(self):
        return self.print__actions_map()
