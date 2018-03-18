from atomic_actions import *


class InfiniteAction:
    action_string = ""
    story = ""

    def __init__(self, rule_number: int, *args, **kwargs):
        pass

    def effect(self):
        return self.action_string

    rule_number = 0


class Quest(InfiniteAction):
    pass


class Goto(InfiniteAction):
    action_string = "go somewhere"
    rules = {}

    def __init__(self, rule_number: int, *args, **kwargs):
        self.rules = {
            3: self.r3,
            4: self.r4,
            5: self.r5,
        }
        print("----------")
        print(rule_number)
        print(args)
        effect = self.rules[rule_number](*args)
        self.story += effect
        print("==========")
        super(Goto, self).__init__(rule_number, *args, **kwargs)

    def effect(self):
        return self.story

    def r3(self, *args, **kwargs):
        pass

    def r4(self, *args, **kwargs):
        pass

    def r5(self, *args, **kwargs):
        pass


class Learn(InfiniteAction):
    action_string = "Learn something"


class Get(InfiniteAction):
    action_string = "Get something"


class Steal(InfiniteAction):
    action_string = "Steal something"


class Spy(InfiniteAction):
    action_string = "Spy on someone"


class Capture(InfiniteAction):
    action_string = "Capture something"


class Kill(InfiniteAction):
    action_string = "Kill someone"


class GotoDef(Goto):

    def r3(self):
        pass

    def r4(self):
        # return explore
        pass

    def r5(self, learn: Learn, goto):
        effect = learn.effect() + " to know where to go, "
        effect += goto
        return effect


story = GotoDef(5,
                Learn(8, goto("somewhere"), Get(1), read("something")),
                goto("somewhere")
                ).effect()

print(story)

# GotoDef(5,
#         Learn(8, GotoDef(1), Get(1), Read("something")),
#         Goto("somewhere")
#         )
