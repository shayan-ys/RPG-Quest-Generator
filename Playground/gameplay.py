from Grammar.actions import NonTerminals as NT
from Grammar.rules import rules
from Grammar.tree import Node


class GameplaySteps:

    @staticmethod
    def get_4(set_of_narrative_steps: list) -> (list, list):
        item_holder = set_of_narrative_steps[4][0]
        # return rule's actions & set_of_narrative_steps
        return \
            [NT.talk] + rules[NT.get][4], \
            [item_holder] + set_of_narrative_steps


def get_steps(node: Node, set_of_narrative_steps: list):
    steps_getter = getattr(GameplaySteps, '%s_%d' % (node.action.name, node.rule), None)
    if callable(steps_getter):
        return steps_getter(set_of_narrative_steps)
    else:
        # default steps
        return rules[node.action][node.rule]
