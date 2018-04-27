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
