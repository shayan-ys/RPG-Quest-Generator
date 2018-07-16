from Grammar.tree import Node

from World import Narrative
from World.elements import Player


class World:
    from World.Instances import Custom as WorldElements
    elements = WorldElements.elements

    player = Player(name='player_1', intel=WorldElements.player_pre_intel)

    def parse_quest(self, quest: Node) -> None:
        """
        :param quest: Quest to be traversed
        :return: None, prints the results in console
        """

        def recursion(root: Node, pre_semantics: list, index: int, depth: int):
            # if index > 5:
            #     return index
            # elif index == 4:
            #     nothing = 0

            # print('-------  depth= %d, index is: %d ------------------------------------------------' % (depth, index))
            # if hasattr(root, 'rule') and root.rule:
            #     print(root.action.name + '[%d]' % root.rule)
            # else:
            #     print(root.action.name)

            node_semantic, children_pre_semantics = Narrative.find(root, depth)(self.elements, *pre_semantics)
            # print(node_semantic)

            traversed = index

            if root.branches and node_semantic:
                for i, branch in enumerate(root.branches):
                    traversed = recursion(branch, children_pre_semantics[i], traversed + 1, depth + 1)

            return traversed

        recursion(quest, [], 0, 0)

    # def find(self, action: Terminals) -> Element:
    #     """
    #     Find suitable element for the given 'action' based on the current status of the World and Player's memory
    #     :param action: The action you're trying to find the right element for
    #     :return: Suitable element object
    #     """
    #     elem = None
    #     if action in self.actions_map and len(self.actions_map[action]):
    #
    #         available_elements = list(self.actions_map[action])
    #         while elem is None and len(available_elements) > 1:
    #
    #             elect_elem = available_elements.pop()
    #             for memo in self.player.short_memory():
    #                 # check if elected element is in short memory of the player, try another available element
    #                 # memo is element of memory list, so it's an Interaction
    #
    #                 if action == memo.action:
    #                     for receiver_elem in memo.receivers:
    #                         if elect_elem != receiver_elem:
    #                             elem = elect_elem
    #
    #         if len(available_elements) == 1:
    #             elem = available_elements.pop()
    #
    #     return elem
    #
    # def str__actions_map(self) -> str:
    #     """
    #     Pretty string of 'actions_map' property
    #     :return: Pretty string
    #     """
    #     if self.actions_map:
    #         return_str = '{'
    #         for action, elems in self.actions_map.items():
    #             return_str += '\n\t%-11s: %s' % (str(action.name), str(elems))
    #         return_str += '\n}'
    #         return return_str
    #     else:
    #         return '{}'
    #
    # def __str__(self):
    #     return str(self.actions_map)
    #
    # def __repr__(self):
    #     return self.__str__()
