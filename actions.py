import atomic_actions


class InfiniteAction:
    def __init__(self):
        pass

    def effect(self):
        pass

    rule_number = 0
    definition = []


class Quest(InfiniteAction):
    pass


class Goto(InfiniteAction):
    pass


class Learn(InfiniteAction):
    pass


class Get(InfiniteAction):
    pass


class Steal(InfiniteAction):
    pass


class Spy(InfiniteAction):
    pass


class Capture(InfiniteAction):
    pass


class Kill(InfiniteAction):
    pass


class GotoDef(Goto):

    def r3(self):
        pass

    def r4(self):
        # return explore
        pass

    def r5(self, learn: Learn):
        effect = learn.effect()
        effect += atomic_actions.null()
        return effect
    


rules = {
    0: None,
    3: Goto
}
