from enum import Enum, auto


class Terminals(Enum):
    null = auto()
    capture = auto()
    damage = auto()
    defend = auto()
    escort = auto()
    exchange = auto()
    experiment = auto()
    explore = auto()
    gather = auto()
    give = auto()
    goto = auto()
    kill = auto()
    listen = auto()
    read = auto()
    repair = auto()
    report = auto()
    spy = auto()
    stealth = auto()
    take = auto()
    use = auto()


class NonTerminals(Enum):
    quest = auto()
    knowledge = auto()
    comfort = auto()
    reputation = auto()
    serenity = auto()
    protection = auto()
    conquest = auto()
    wealth = auto()
    ability = auto()
    equipment = auto()

    sub_quest = auto()
    goto = auto()
    learn = auto()
    get = auto()
    steal = auto()
    spy = auto()
    capture = auto()
    kill = auto()


T = Terminals
NT = NonTerminals

rules = {
    NT.quest: {
        1: [NT.knowledge],
        2: [NT.comfort],
        3: [NT.reputation],
        4: [NT.serenity],
        5: [NT.protection],
        6: [NT.conquest],
        7: [NT.wealth],
        8: [NT.ability],
        9: [NT.equipment]
    },
    NT.knowledge: {
        1: [NT.get, NT.goto, T.give],
        2: [NT.spy],
        3: [NT.goto, T.listen, NT.goto, T.report],
        4: [NT.get, NT.goto, T.use, NT.goto, T.give]
    },
    NT.comfort: {
        1: [NT.get, NT.goto, T.give],
        2: [NT.goto, T.damage, NT.goto, T.report]
    },
    NT.reputation: {
        1: [NT.get, NT.goto, T.give],
        2: [NT.goto, NT.kill, NT.goto, T.report],
        3: [NT.goto, NT.goto, T.report]
    },
    NT.serenity: {
        1: [NT.goto, T.damage],
        2: [NT.get, NT.goto, T.use, NT.goto, T.give],
        3: [NT.get, NT.goto, T.use, T.capture, NT.goto, T.give],
        4: [NT.goto, T.listen, NT.goto, T.report],
        5: [NT.goto, T.take, NT.goto, T.give],
        6: [NT.get, NT.goto, T.give],
        7: [NT.goto, T.damage, T.escort, NT.goto, T.report]
    },
    NT.protection: {
        1: [NT.goto, T.damage, NT.goto, T.report],
        2: [NT.get, NT.goto, T.use],
        3: [NT.goto, T.repair],
        4: [NT.get, NT.goto, T.use],
        5: [NT.goto, T.damage]
    },
    NT.conquest: {
        1: [NT.goto, T.damage],
        2: [NT.goto, NT.steal, NT.goto, T.give]
    },
    NT.wealth: {
        1: [NT.goto, NT.get],
        2: [NT.goto, NT.steal],
        3: [T.repair]
    },
    NT.ability: {
        1: [T.repair, T.use],
        2: [NT.get, T.use],
        3: [T.use],
        4: [T.damage],
        5: [T.use],
        6: [NT.get, T.use],
        7: [NT.get, T.experiment]
    },
    NT.equipment: {
        1: [T.repair],
        2: [NT.get, NT.goto, T.give],
        3: [NT.steal],
        4: [NT.goto, T.exchange]
    },

    NT.sub_quest: {
        1: [NT.goto],
        2: [NT.goto, NT.quest, T.goto]
    },
    NT.goto: {
        1: [T.null],
        2: [T.explore],
        3: [NT.learn, T.goto]
    },
    NT.learn: {
        1: [T.null],
        2: [NT.goto, NT.sub_quest, T.listen],
        3: [NT.goto, NT.get, T.read],
        4: [NT.get, NT.sub_quest, T.give, T.listen]
    },
    NT.get: {
        1: [T.null],
        2: [NT.steal],
        3: [NT.goto, T.gather],
        4: [NT.goto, NT.get, NT.sub_quest, NT.goto, T.exchange]
    },
    NT.steal: {
        1: [NT.goto, T.stealth, T.take],
        2: [NT.goto, NT.kill, T.take]
    },
    NT.spy: {
        1: [NT.goto, T.spy, NT.goto, T.report]
    },
    NT.capture: {
        1: [NT.get, NT.goto, T.capture]
    },
    NT.kill: {
        1: [NT.goto, T.kill]
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
        self.flatten = []
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
                        self.branches = list(branches)
                        # create/update flatten branches
                        self.flat()
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

    def flat(self, update: bool=False) -> list:

        if self.flatten:
            return self.flatten

        flatten_branches = []

        if self.branches:
            for branch in self.branches:
                if branch.action != T.null:

                    if branch.flatten and not update:
                        flatten_branches += branch.flatten
                    else:
                        flatten_branches += branch.flat()

            if len(flatten_branches) > 1:
                self.flatten = [self.action] + flatten_branches
            else:
                self.flatten = flatten_branches

        else:
            self.flatten = [self.action]

        return self.flatten

    def replace_by_path(self, path: list, sub_tree):
        if not path:
            return
        pass


class ActionLeaf(ActionTree):
    def __init__(self, action: T):
        # ActionTree expects a NonTerminal action, but I'm giving a Terminal and that's fine!
        super(ActionLeaf, self).__init__(action, None)


Node = ActionTree
Leaf = ActionLeaf
