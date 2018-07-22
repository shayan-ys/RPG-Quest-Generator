from Grammar.tree import Node

from World import Narrative
from World.elements import Player


class World:
    from World.Instances import Everquest as WorldElements
    elements = WorldElements.elements

    player = Player(name='player_1', intel=WorldElements.player_pre_intel)

    def __init__(self):
        self.elements.append(self.player)

    def parse_quest(self, quest: Node) -> None:
        """
        :param quest: Quest to be traversed
        :return: None, prints the results in console
        """

        def recursion(root: Node, pre_semantics: list, index: int, depth: int):
            # if index > 54:
            #     return index
            # elif index == 4:
            #     nothing = 0

            print('-------  depth= %d, index is: %d ------------------------------------------------' % (depth, index))
            if hasattr(root, 'rule') and root.rule:
                print(root.action.name + '[%d]' % root.rule)
            else:
                print(root.action.name)

            node_semantic, children_pre_semantics = Narrative.find(root, depth)(self.elements, *pre_semantics)
            # print(node_semantic)

            traversed = index

            if root.branches and node_semantic:
                for i, branch in enumerate(root.branches):
                    traversed = recursion(branch, children_pre_semantics[i], traversed + 1, depth + 1)

            return traversed

        recursion(quest, [], 0, 0)

        for elem in self.elements:
            if isinstance(elem, Player):
                print(">\nplayer's final location: " + str(elem.current_location))
                print("player's intel: " + str(elem.intel))
                print("player's belongings: " + str(elem.belongings))
