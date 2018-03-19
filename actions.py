from atomic_actions import *


class InfiniteAction:
    action_string = ""
    null_action_string = ""
    target = ""
    rule_number = 0
    action_types = {}
    steps = []

    def __init__(self, target: str, rule_number: int, *args):
        self.target = target
        self.rule_number = rule_number
        print(rule_number)
        if rule_number == 1 or self.action_types[rule_number] is None:
            return
        if rule_number not in self.action_types:
            print("Error: Rule number should be one of " + str(self.action_types.keys()))
            return
        for index, action_type in enumerate(self.action_types[rule_number]):
            if index >= len(args):
                print("tuple index will get out of range, because index=" + str(index) +
                      " while tuple has length of=" + str(len(args)) + " :hint: rule_number=" + str(rule_number))
            if not isinstance(args[index], action_type):
                print("Error: " + str(index) + "th argument should be of type '" + str(action_type) +
                      "' instead, you've entered '" + str(type(args[index])) + "' type.")
                return
        self.steps = list(args)

    def story(self, depth: int=0) -> str:
        story_line = ""
        # story_line += ("\t" * depth)
        story_line += self.action_string + " " + self.target + ": {"
        if not self.steps:
            story_line += "You already " + self.null_action_string
        # story_line += "\n"
        steps_story_lines_list = []
        for step in self.steps:
            if type(step) == str:
                steps_story_lines_list.append(step)
            else:
                steps_story_lines_list.append(step.story(depth + 1))

        story_line += ", ".join(steps_story_lines_list) + "}"

        return story_line


class QuestType(InfiniteAction):
    pass


class GotoType(InfiniteAction):
    action_string = "Goto"
    null_action_string = "have it"


class LearnType(InfiniteAction):
    action_string = "Learn"
    null_action_string = "know it"


class GetType(InfiniteAction):
    action_string = "Get"
    null_action_string = "have it"


class StealType(InfiniteAction):
    action_string = "Steal"


class SpyType(InfiniteAction):
    action_string = "Spy on"


class CaptureType(InfiniteAction):
    action_string = "Capture"


class KillType(InfiniteAction):
    action_string = "Kill"


class Goto(GotoType):
    action_types = {
        3: None,
        4: [str],
        5: [LearnType, str]
    }


class Learn(LearnType):
    action_types = {
        6: None,
        7: [GotoType, QuestType, str],
        8: [GotoType, GetType, str],
        9: [GetType, QuestType, str, str]
    }


class Get(GetType):
    action_types = {
        10: None
    }


# story = GotoDef(5,
#                 Learn(8, goto("somewhere"), Get(1), read("something")),
#                 goto("somewhere")
#                 ).effect()

# Goto("Azeroth", 5,
#      Learn("how to go to Azeroth", 1),
#      goto("Azeroth"))

story = Goto("Azeroth", 5,
             Learn("how to go to Azeroth", 8,
                   Goto("Dark Gate", 4,
                        explore("the forest")),
                   Get("portal's manual", 10),
                   read("portal's manual")),
             goto("Azeroth")).story()

print(story)

# Goto("Azeroth", 5,
#      Learn("how to go to Azeroth", 8,
#            Goto("Dark Gate", 4,
#                 explore("the forest")),
#            Get("map", 10),
#            read("map")),
#      goto("Azeroth"))

# GotoDef(5,
#         Learn(8, GotoDef(1), Get(1), Read("something")),
#         Goto("somewhere")
#         )

# Goto Azeroth: {
#     Learn how to go to Azeroth: {
#         Goto Dark Gate: {
#             explore the forest
#         },
#         Get portal manual: {
#             You already have it
#         },
#         read: portal manual
#     }, goto: Azeroth
# }
