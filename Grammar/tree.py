from Grammar.actions import NonTerminals as NT, Terminals as T
from Grammar.rules import rules
import json


class Tree(object):
    branches = []
    action = None
    rule = None

    def serialize(self) -> dict:

        serialized_branches = []
        if self.branches:
            for branch in self.branches:
                if branch:
                    ser = branch.serialize()
                    serialized_branches.append(ser)

        return {
            "action_str": str(self.action),
            "rule": self.rule,
            "branches": serialized_branches,
            "action": self.action.value,
            "terminal": True if isinstance(self.action, T) else False
        }

    def pretty_string(self):
        rule_str = ""
        if self.rule:
            rule_str = "(" + str(self.rule) + ")"
        if not self.branches:
            return str(self.action) + rule_str
        return str(self.action) + rule_str + ":{" + ", ".join(map(Tree.pretty_string, self.branches)) + "}"

    def __dict__(self) -> dict:
        return self.serialize()

    def __str__(self):
        return json.dumps(self.serialize())

    def __repr__(self):
        return self.pretty_string()

    def __eq__(self, other):
        if isinstance(other, Tree):
            return self.action == other.action and self.rule == other.rule and self.branches == other.branches
        return False


class Node(Tree):
    def __init__(self, action: NT, rule: int=None, *branches):
        self.action = action
        self.rule = rule
        self.branches = None
        self.flatten = []
        self.depth = 0
        if rule:
            if action in rules:
                if rule in rules[action]:
                    if len(branches) == len(rules[action][rule]):
                        for (sub_tree, action_type) in zip(branches, rules[action][rule]):
                            if isinstance(sub_tree, Node):
                                if sub_tree.action == action_type:
                                    pass
                                else:
                                    raise Exception("type mismatch, expecting type '" + str(action_type)
                                                    + "', got '" + str(sub_tree.action) + "' instead.")
                            else:
                                raise Exception("branch is not of type '" + str(type(Node))
                                                + "', instead it is '" + str(type(sub_tree)) + "'")
                        self.branches = list(branches)
                        # update tree flat and depth vars
                        self.update()
                    else:
                        raise Exception("branches for Tree action are not valid, as the node is of action type '"
                                        + str(action) + "' and rule is '" + str(rule)
                                        + "'. According to rules it should have exactly '"
                                        + str(len(rules[action][rule])) + "', but you have entered '"
                                        + str(len(branches)) + "'.")

                else:
                    raise Exception("rule '" + str(rule) + "' is not in rules for selected action, '"
                                    + str(action) + "'. It should be one of " + str(rules[action].keys()))
            else:
                raise Exception("action '" + str(action) + "' is not in rules. It should be one of "
                                + str(rules.keys()))

    def flat(self) -> list:

        flatten_branches = []

        if self.branches:
            for branch in self.branches:
                if branch.action != T.null:

                    flatten_branches += branch.flat()

            if len(flatten_branches) > 1:
                self.flatten = [self.action] + flatten_branches
            else:
                self.flatten = flatten_branches

        else:
            self.flatten = [self.action]

        return self.flatten

    def calc_depth(self, current_level: int=0) -> int:
        if current_level > 900:
            return 900

        max_depth = 0
        if self.branches:
            for branch in self.branches:
                branch_depth = branch.calc_depth(current_level + 1) + 1
                if branch_depth > 900:
                    return branch_depth
                max_depth = max(branch_depth, max_depth)

        self.depth = max_depth
        return self.depth

    def update(self):
        self.flat()
        self.calc_depth()


class Leaf(Node):
    def __init__(self, action: T):
        # Node expects a NonTerminal action, but I'm giving a Terminal and that's fine!
        super(Leaf, self).__init__(action, None)
