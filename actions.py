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
    knowledge = auto()
    quest = auto()
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
    NT.knowledge: {
        1: [NT.get, NT.goto, T.give],
        2: [NT.spy],
        3: [NT.goto, T.listen, NT.goto, T.report],
        4: [NT.get, NT.goto, T.use, NT.goto, T.give]
    },
    NT.quest: {
        1: [NT.knowledge]
    },
    NT.sub_quest: {
        1: [NT.goto],
        2: [NT.goto, NT.quest, T.goto]
    },
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
        1: [],
        2: [NT.steal],
        3: [NT.goto, T.gather],
        4: [NT.goto, NT.get, NT.goto, NT.sub_quest, T.exchange]
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


Node = ActionTree
Leaf = ActionLeaf

tree = Node(NT.quest, 1,
            Node(NT.knowledge, 3,
                 Node(NT.goto, 3,
                      Node(NT.learn, 3,
                           Node(NT.goto, 1),
                           Node(NT.get, 2,
                                Node(NT.steal, 1,
                                     Node(NT.goto, 2,
                                          Leaf(T.explore)),
                                     Leaf(T.stealth),
                                     Leaf(T.take))),
                           Leaf(T.read)),
                      Leaf(T.goto)),
                 Leaf(T.listen),
                 Node(NT.goto, 1),
                 Leaf(T.report)))

print(tree)

# Output:
# NonTerminals.quest(1):{NonTerminals.knowledge(3):{NonTerminals.goto(3):{NonTerminals.learn(3):{NonTerminals.goto(1), NonTerminals.get(2):{NonTerminals.steal(1):{NonTerminals.goto(2):{Terminals.explore}, Terminals.stealth, Terminals.take}}, Terminals.read}, Terminals.goto}, Terminals.listen, NonTerminals.goto(1), Terminals.report}}
