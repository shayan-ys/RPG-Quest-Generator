from World import Narrative

from Grammar.tree import Node
from Grammar.actions import NonTerminals as NT, Terminals as T
from Grammar.plot import export_grammar_plot

from copy import copy


class Progress:

    quest: Node = None
    semantics_indices = {}
    semantics_parsed_for_branches = []
    current_node: Node = None
    completed_indices = []

    def __init__(self, quest: Node):
        local_quest = copy(quest)
        # local_quest.clean_nulls()
        local_quest.set_indices()
        self.quest = local_quest
        self.current_node = local_quest

        export_grammar_plot(local_quest)

        self.semantics_indices[0] = []
        self.get_narratives(root=local_quest, pre_semantics=[])

    def find_node(self, index: int=None) -> Node:
        if index is None:
            index = self.current_node.index
        elif index == self.current_node.index:
            return self.current_node

        def traverse_quest(root: Node):

            if root.index >= index:
                return root

            if root.branches:
                for branch in root.branches:
                    node = traverse_quest(branch)
                    if node.index >= index:
                        return node

            return root

        return traverse_quest(root=self.quest)

    def get_narratives(self, root: Node, pre_semantics: list):
        if root.index in self.semantics_parsed_for_branches:
            return

        if root.branches:
            children_pre_semantics = Narrative.find(root)(*pre_semantics)
            # if not children_pre_semantics:
            #     print(Narrative.find(root).__name__)
            #     print(pre_semantics)

            for i, branch in enumerate(root.branches):
                if branch.action == T.null:
                    continue
                self.semantics_indices[branch.index] = children_pre_semantics[i]

        self.semantics_parsed_for_branches.append(root.index)

    def get_current_semantics(self):
        if self.current_node and self.current_node.index in self.semantics_indices:
            return self.semantics_indices[self.current_node.index]
        return []

    def print_progress(self, full: bool=False):
        # print("level:", self.current_node.index, ", current-node:", self.current_node.action, self.current_node.rule,
        #       ", branches:", [(branch.action, branch.rule) for branch in self.current_node.branches])
        # print("semantics:", self.semantics_indices)
        print("level:", self.current_node.index, ", current-node:", self.current_node.action)
        if full:
            print("semantics:", self.semantics_indices)
        else:
            print("semantics:", self.get_current_semantics())

    def find_next_active_level(self, node: Node=None):

        if node is None:
            node = self.current_node

        # is_action_done_method = results.find(node)
        # if not is_action_done_method(*self.semantics_indices[node.index]):
        if node.index not in self.completed_indices and node.action != T.null:

            if node.action != NT.sub_quest:
                # todo: sub_quest is being skipped which is wrong!!! problem is addressed on Oct 24 should think about

                if node.branches:
                    # go down the tree, player should first complete parent's branches
                    for branch in node.branches:
                        if branch.index not in self.completed_indices:
                            self.update_active_level(branch)
                            if not self.find_next_active_level(branch):
                                return False
                else:
                    # terminal waiting to be completed
                    return False

        self.completed_indices.append(node.index)
        return True

    def update_active_level(self, new_node: Node):
        # using previous node
        self.get_narratives(self.current_node, pre_semantics=self.get_current_semantics())

        # update active level
        self.current_node = new_node

    def check_action_proceed(self, action: T, args: list) -> bool:
        if action == self.current_node.action and args == self.get_current_semantics():
            self.completed_indices.append(self.current_node.index)
            self.find_next_active_level(self.quest)
            return True
        self.find_next_active_level()
        return False