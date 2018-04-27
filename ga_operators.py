from actions import rules
from actions_operators import pattern_finder, flat_non_terminals_subtrees, replace_node_by_path
from quests import *

import random


def repetition_factor(flatten_events: list, pattern_min_length: int=2, pattern_max_length: int=None) -> float:
    if not pattern_max_length:
        pattern_max_length = int(len(flatten_events) / 2)

    q = 0
    for n in range(pattern_min_length, pattern_max_length):
        for r, s in pattern_finder(flatten_events, pat_length=n, min_repeat=2):
            q += n * r * s

    return q


def crossover_flatten(parent1: Node, parent2: Node) -> (Node, Node):

    p1_flat, p1_types_flat, p1_paths = flat_non_terminals_subtrees(parent1)
    p2_flat, p2_types_flat, p2_paths = flat_non_terminals_subtrees(parent2)

    p1_rand = 0
    p2_indices_with_selected_type = []
    p1_rand_validity_for_p2 = 1000

    while p1_rand_validity_for_p2:
        p1_rand = random.randint(0, len(p1_flat) - 1)
        selected_type = p1_types_flat[p1_rand]

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


def quest_generator(root_type: NT, depth: int=7) -> Node:

    if root_type not in rules:
        print("###### rule: " + str(root_type) + " is not in the rules list !!!")
    rules_for_type = rules[root_type]
    if depth > 0:
        rule_number, rule_requirements_list = random.choice(list(rules_for_type.items()))
    else:
        rule_number, rule_requirements_list = 1, rules_for_type[1]

    branches = []
    for action_type in rule_requirements_list:
        if type(action_type) == T:
            branch = Leaf(action_type)
        else:
            branch = quest_generator(root_type=action_type, depth=depth-1)
        branches.append(branch)

    return Node(root_type, rule_number, *branches)
