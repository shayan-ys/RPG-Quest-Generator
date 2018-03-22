from enum import Enum, auto


class Terminals(Enum):
    explore = auto()
    give = auto()
    goto = auto()
    listen = auto()
    read = auto()


class NonTerminals(Enum):
    sub_quest = auto()
    goto = auto()
    learn = auto()
    get = auto()


T = Terminals
NT = NonTerminals

rules = {
    NT.goto: {
        1: [],
        2: [T.explore],
        3: [NT.learn, T.goto]
    },
    NT.learn: {
        1: [],
        2: [NT.goto, NT.sub_quest, T.listen],
        3: [NT.goto, NT.get, T.read],
        4: [NT.get, NT.sub_quest, T.give, T.listen]
    },
    NT.get: {
        1: []
    }
}


class Tree(object):
    branches = []
    action = None
    rule = None

    def __str__(self):
        rule_str = ""
        if self.rule:
            rule_str = "(" + str(self.rule) + ")"
        if not self.branches:
            return str(self.action) + rule_str
        return str(self.action) + rule_str + ":{" + ", ".join(map(str, self.branches)) + "}"

    def __repr__(self):
        return self.__str__()


class ActionTree(Tree):
    def __init__(self, action: NT, rule: int=None, *branches):
        self.action = action
        self.rule = rule
        self.branches = None
        if rule:
            if action in rules:
                if rule in rules[action]:
                    if len(branches) == len(rules[action][rule]):
                        for (sub_tree, action_type) in zip(branches, rules[action][rule]):
                            if isinstance(sub_tree, ActionTree):
                                if sub_tree.action == action_type:
                                    pass
                                else:
                                    raise Exception("type mismatch, expecting type '" + str(action_type)
                                                    + "', got '" + str(sub_tree.action) + "' instead.")
                            else:
                                raise Exception("branch is not of type '" + str(type(ActionTree))
                                                + "', instead it is '" + str(type(sub_tree)) + "'")
                        self.branches = branches
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


class ActionLeaf(ActionTree):
    def __init__(self, action: T):
        super(ActionLeaf, self).__init__(action, None)


tree = ActionTree(NT.goto, 2,
                  ActionLeaf(T.explore))

tree2 = ActionTree(NT.goto, 3,
                   ActionTree(NT.learn, 1),
                   ActionLeaf(T.goto))

tree3 = ActionTree(NT.goto, 3,
                   ActionTree(NT.learn, 3,
                              ActionTree(NT.goto, 2, ActionLeaf(T.explore)),
                              ActionTree(NT.get, 1),
                              ActionLeaf(T.read)),
                   ActionLeaf(T.goto))

print(tree3)
