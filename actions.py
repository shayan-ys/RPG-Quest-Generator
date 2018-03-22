from enum import Enum, auto


class Terminals(Enum):
    goto = auto
    read = auto
    explore = auto
    listen = auto
    give = auto


class NonTerminals(Enum):
    sub_quest = auto
    goto = auto
    learn = auto
    get = auto


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
    data = None

    def __init__(self, data=None, *branches):
        self.data = data
        if not branches:
            self.branches = []
        else:
            self.branches = branches

    def __str__(self):
        if not self.branches:
            return str(self.data)
        return str(self.data) + ":{" + ", ".join(map(str, self.branches)) + "}"

    def __repr__(self):
        return self.__str__()


root = Tree("root",
            Tree("left"),
            Tree("right", Tree("r1"), Tree("r2"), Tree("r3")))

print(root)

