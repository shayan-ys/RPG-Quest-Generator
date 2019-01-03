from Grammar.rules import rules
from Data.statics import GAParams
from Data.quests import *

import random
from Logger import logger
logger.name = __name__


def quest_generator(root_type: NT=NT.quest, root_rule_number: int=None) -> Node:
    """
    Generates a random tree, with max depth defined in 'GAParams.maximum_quest_depth' (no guarantee for exact depth)
    :param root_type: Type of the tree's root, default: quest
    :param root_rule_number: Optional rule number, instead of randomly generating it
    :return: a randomly generated tree
    """

    def recursion(node_type: NT, depth: int, rule_number: int=None) -> Node:

        if node_type not in rules:
            logger.error("quest_generator, rule: " + str(node_type) + " is not in the rules list.")
            return None

        rules_for_type = rules[node_type]

        if root_rule_number and rule_number and rule_number in rules_for_type:
            rule_requirements_list = rules_for_type[rule_number]
        else:
            if depth > 0:
                rule_number, rule_requirements_list = random.choice(list(rules_for_type.items()))
            else:
                """ Rule number one for each action is the shortest one, this will make the quest depth within limit """
                rule_number, rule_requirements_list = 1, rules_for_type[1]

        branches = []
        for action_type in rule_requirements_list:
            if type(action_type) == T:
                branch = Leaf(action_type)
            else:
                branch = recursion(node_type=action_type, depth=depth-1)
            branches.append(branch)

        return Node(node_type, rule_number, *branches)

    generated_tree = recursion(node_type=root_type, depth=GAParams.maximum_quest_depth, rule_number=root_rule_number)
    generated_tree.update_metrics()
    return generated_tree
