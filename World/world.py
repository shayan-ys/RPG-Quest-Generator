from World import Narrative
from World.elements import Element
from World.properties import Name
from World.tags import ActionTags
from World.types import Player

from Grammar.actions import Terminals, NonTerminals
from Grammar.tree import Node


class World:
    from World.Instances import Custom as WorldElements
    elements = WorldElements.elements

    player = Element(Player, name='player_1')
    player.type.intel = WorldElements.player_pre_intel
    actions_map = {}

    def __init__(self):
        # populating 'actions_map' property
        # for element in self.elements:
        #     if not isinstance(element, Element):
        #         continue
        #     for tag in element.type.tags:
        #         if isinstance(tag, ActionTags):
        #             act = tag.action
        #             if act in self.actions_map:
        #                 self.actions_map[act].append(element)
        #             else:
        #                 self.actions_map[act] = [element]
        pass

    def parse_quest(self, quest: Node) -> None:
        """
        Traverse the given 'quest' actions to, assign elements to each action
        and update the World's status and Player's memory
        :param quest: Quest to be traversed
        :return: None, prints the results in console
        """

        def recursion(root: Node, index: int, depth: int):
            if index > 1:
                return index

            print('-------  depth= %d, index is: %d ------------------------------------------------' % (depth, index))
            print(root)

            results = Narrative.find(root, depth)(self.elements)
            print(results)

            traversed = index

            if root.branches:
                for branch in root.branches:
                    traversed = recursion(branch, traversed + 1, depth + 1)

            return traversed

        recursion(quest, 0, 0)
        # for index, action in enumerate(quest.flatten):
        #     print("%d:" % (index + 1))
        #     print(action)
        #     if isinstance(action, Terminals):
        #         elem = self.find(action=action)    # type: Element
        #         print(elem.name)
        #         self.player.remember(action=action, receivers=[elem])
        #
        #     print('---')

        # print('memory: (from oldest to newest)')
        # for memo in reversed(self.player.memory):
        #     print(memo)

    def find(self, action: Terminals) -> Element:
        """
        Find suitable element for the given 'action' based on the current status of the World and Player's memory
        :param action: The action you're trying to find the right element for
        :return: Suitable element object
        """
        elem = None
        if action in self.actions_map and len(self.actions_map[action]):

            available_elements = list(self.actions_map[action])
            while elem is None and len(available_elements) > 1:

                elect_elem = available_elements.pop()
                for memo in self.player.short_memory():
                    # check if elected element is in short memory of the player, try another available element
                    # memo is element of memory list, so it's an Interaction

                    if action == memo.action:
                        for receiver_elem in memo.receivers:
                            if elect_elem != receiver_elem:
                                elem = elect_elem

            if len(available_elements) == 1:
                elem = available_elements.pop()

        return elem

    def str__actions_map(self) -> str:
        """
        Pretty string of 'actions_map' property
        :return: Pretty string
        """
        if self.actions_map:
            return_str = '{'
            for action, elems in self.actions_map.items():
                return_str += '\n\t%-11s: %s' % (str(action.name), str(elems))
            return_str += '\n}'
            return return_str
        else:
            return '{}'

    def __str__(self):
        return str(self.actions_map)

    def __repr__(self):
        return self.__str__()
