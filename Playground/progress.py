from Data import quests
from Grammar.tree import Node


class Progress:

    quest: Node = None
    semantics_index = []

    def __init__(self, quest: Node):
        self.quest = quest

    def parse_node(self, index: int):

        def traverse_quest(root: Node, traversed: int):

            if traversed >= index:
                return traversed, root

            if root.branches:
                for branch in root.branches:
                    traversed, node = traverse_quest(branch, traversed+1)
                    if traversed >= index:
                        return traversed, node

            return traversed, root

        return traverse_quest(root=self.quest, traversed=0)[1]


pro = Progress(quest=quests.cure.clean_nulls())
node = pro.parse_node(14)
print(node.action, node.rule)

# quest = quests.cure.clean_nulls()
# print(quest.branches[0].branches[0].branches[0].pretty_string())
