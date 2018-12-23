from Grammar.actions import NonTerminals as NT, Terminals as T
from Grammar.rules import rules
from copy import deepcopy
import json


class Tree(object):
    branches = []
    action = None
    rule = None

    def serialize(self, simple=False) -> dict:

        serialized_branches = []
        if self.branches:
            for branch in self.branches:
                if branch:
                    ser = branch.serialize(simple=simple)
                    serialized_branches.append(ser)

        serialized = {
            "action_str": str(self.action),
            "rule": self.rule,
            "branches": serialized_branches
        }

        if not simple:
            serialized['action'] = self.action.value
            serialized['terminal'] = True if isinstance(self.action, T) else False

        return serialized

    def pretty_string(self):
        rule_str = ""
        if self.rule:
            rule_str = "(" + str(self.rule) + ")"
        if not self.branches:
            return str(self.action) + rule_str
        return str(self.action) + rule_str + ":{" + ", ".join(map(Tree.pretty_string, self.branches)) + "}"

    def dumps(self, simple=False) -> str:
        return json.dumps(self.serialize(simple=simple))

    def update(self, new_vars: dict):
        self.action = new_vars['action']
        self.rule = new_vars['rule']
        self.branches = new_vars['branches']

    def __dict__(self) -> dict:
        return {
            "action": self.action,
            "rule": self.rule,
            "branches": self.branches
        }

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.update(self.__dict__())
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__().items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __str__(self):
        return self.pretty_string()

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
        self.branches = []
        self.flatten = []
        self.depth = 0
        self.index = 0
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
                        self.update_metrics()
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

    def clean_nulls(self, index: int=0) -> (int, 'Node'):

        self.index = index
        all_branches_null = True
        if self.branches:
            cleaned_branches = []
            for branch in self.branches:
                index, cleaned = branch.clean_nulls(index+1)
                if cleaned.action != T.null:
                    all_branches_null = False
                cleaned_branches.append(cleaned)

            if all_branches_null:
                self.action = T.null
                self.branches = []
                self.rule = None

            # elif len(cleaned_branches) == 1 and self.action != NT.quest:
            #     self.action = cleaned_branches[0].action
            #     self.branches = cleaned_branches[0].branches
            #     self.rule = cleaned_branches[0].rule

            else:
                self.branches = cleaned_branches

        return index, self

    def set_indices(self, index: int=0) -> (int, 'Node'):

        self.index = index
        if self.branches:
            for branch in self.branches:
                index = branch.set_indices(index + 1)

        return index

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

    def update_metrics(self):
        self.flat()
        self.calc_depth()

    def genre(self) -> str:
        if self.action == NT.quest and self.branches:
            action = self.branches[0].action
            rule = self.branches[0].rule
            is_nt = True if self.branches[0].branches else False
        else:
            action = self.action
            rule = self.rule
            is_nt = True if self.branches else False

        if is_nt:
            return '%s(%i)' % (action.name, rule)
        return action.name


class Leaf(Node):
    def __init__(self, action: T):
        # Node expects a NonTerminal action, but I'm giving a Terminal and that's fine!
        super(Leaf, self).__init__(action, None)
