from World import Narrative
from World.Types.Log import Message

from Grammar.tree import Node
from Grammar.actions import Terminals as T
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
        self.semantics_indices = {}
        self.semantics_parsed_for_branches = []
        self.current_node = local_quest
        self.completed_indices = []

        export_grammar_plot(local_quest)

        self.semantics_indices[0] = []
        self.get_narratives(root=local_quest, pre_semantics=[])

    def get_narratives(self, root: Node, pre_semantics: list):
        """
        Run narration functions for Non-terminal nodes that weren't parsed already
        :param root:
        :param pre_semantics:
        :return:
        """
        if root.index in self.semantics_parsed_for_branches:
            return

        if root.branches:
            # Parse only Non-terminals
            children_pre_semantics = Narrative.find(root)(*pre_semantics)

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
        Message.debug("level: %i, current-node: %s" % (self.current_node.index, self.current_node.action))
        if full:
            Message.debug("semantics: %s" % self.semantics_indices)
        else:
            Message.debug("semantics: %s" % self.get_current_semantics())

    def find_next_active_level(self, node: Node=None):

        if node is None:
            node = self.current_node

        if node.index not in self.completed_indices and node.action != T.null:

            if node.branches:
                # go down the tree, player should first complete parent's branches
                for branch in node.branches:
                    if branch.index not in self.completed_indices:
                        # if completed skip
                        if branch.index not in self.semantics_parsed_for_branches:
                            # don't parse branches which already parsed
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
        # only non-terminal actions
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
