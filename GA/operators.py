from Grammar.rules import rules
from Grammar.operators import flat_non_terminals_subtrees, replace_node_by_path
from Data.statics import GAParams
from Data.quests import *

import random
from Logger import logger
logger.name = __name__


def crossover_flatten(parent1: Node, parent2: Node) -> (Node, Node):

    p1_flat, p1_types_flat, p1_paths = flat_non_terminals_subtrees(parent1)
    p2_flat, p2_types_flat, p2_paths = flat_non_terminals_subtrees(parent2)

    p1_rand = 0
    p2_indices_with_selected_type = []
    p1_rand_validity_for_p2 = 1000

    while p1_rand_validity_for_p2:
        p1_rand = random.randint(0, len(p1_flat) - 1)
        selected_type = p1_types_flat[p1_rand]

        if p1_rand_validity_for_p2 > 750 and (selected_type == NT.quest or selected_type in rules[NT.quest].values()):
            p1_rand_validity_for_p2 -= 1
            continue

        p2_indices_with_selected_type = [i for i, node_type in enumerate(p2_types_flat) if node_type == selected_type]
        if p2_indices_with_selected_type:
            break
        p1_rand_validity_for_p2 -= 1

    p2_rand = random.choice(p2_indices_with_selected_type)

    p1_node = p1_flat[p1_rand]
    p2_node = p2_flat[p2_rand]

    child1 = replace_node_by_path(parent1, p1_paths[p1_rand], p2_node)
    child2 = replace_node_by_path(parent2, p2_paths[p2_rand], p1_node)

    return child1, child2


def quest_generator(root_type: NT=NT.quest) -> Node:
    """
    Generates a random tree, with max depth defined in 'GAParams.maximum_quest_depth' (no guarantee for exact depth)
    :param root_type: Type of the tree's root, default: quest
    :return: a randomly generated tree
    """

    def recursion(node_type: NT, depth: int) -> Node:

        if node_type not in rules:
            logger.error("quest_generator, rule: " + str(node_type) + " is not in the rules list.")
            return None

        rules_for_type = rules[node_type]
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

    generated_tree = recursion(node_type=root_type, depth=GAParams.maximum_quest_depth)
    generated_tree.update()
    return generated_tree
