from Grammar.actions import Terminals
from Grammar.tree import Node

from World import Narrative
from World.Types.Person import Player

from copy import deepcopy


class World:
    from World.Instances import Custom as WorldElements

    player = None

    def parse_quest(self, quest: Node) -> None:
        """
        :param quest: Quest to be traversed
        :return: None, prints the results in console
        """

        def recursion(root: Node, pre_semantics: list, index: int, depth: int):
            # if index > 1:
            #     return index
            # elif index == 23:
            #     nothing = 0
            #     print(list(root.branches))

            if root.action == Terminals.null:
                return index

            print('-------  depth= %d, index is: %d ------------------------------------------------' % (depth, root.index))
            if hasattr(root, 'rule') and root.rule:
                print(root.action.name + '[%d]' % root.rule)
            else:
                print(root.action.name)

            children_pre_semantics = Narrative.find(root)(*pre_semantics)
            # print(node_semantic)

            traversed = index

            if root.branches and children_pre_semantics:
                for i, branch in enumerate(root.branches):
                    traversed = recursion(branch, children_pre_semantics[i], traversed + 1, depth + 1)

            return traversed

        local_quest = deepcopy(quest)
        # local_quest.clean_nulls()
        local_quest.set_indices()
        recursion(local_quest, [], 0, 0)

        # for elem in self.elements:
        #     if isinstance(elem, Player):
        #         print(">\nplayer's final location: " + str(elem.current_location))
        #         print("player's intel: " + str(elem.intel))
        #         print("player's belongings: " + str(elem.belongings))
        #         print("player's favours book: " + str(elem.favours_book))
