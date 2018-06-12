from Grammar.operators import flat_non_terminals_subtrees, replace_node_by_path
from Grammar.tree import Node

import random
from Logger import logger
logger.name = __name__


def crossover_flatten(parent1: Node, parent2: Node) -> (Node, Node):
    """
    Crossover between two trees ('parent1', 'parent2') using their 'flat_non_terminal_subtrees'
    :param parent1:
    :param parent2:
    :return: 'child1' and 'child2' if successful, if not None
    """

    p1_flat, p1_node_types, p1_paths = flat_non_terminals_subtrees(parent1)
    p2_flat, p2_node_types, p2_paths = flat_non_terminals_subtrees(parent2)

    if len(p1_flat) <= 2 or len(p2_flat) <= 2:
        """ parents doesn't have any node except 'quest' and main 'strategy' """
        return None

    p1_rand = 0
    p2_rand = 0
    p1_node = None
    p2_node = None
    p1_rand_validity_for_p2 = 1000

    while p1_rand_validity_for_p2:
        p1_rand = random.randint(2, len(p1_flat) - 1)
        selected_type = p1_node_types[p1_rand]

        p2_indices_with_selected_type = [i for i, node_type in enumerate(p2_node_types) if node_type == selected_type]
        if p2_indices_with_selected_type:
            p2_rand = random.choice(p2_indices_with_selected_type)
            p1_node = p1_flat[p1_rand]
            p2_node = p2_flat[p2_rand]
            if p1_node != p2_node:
                break

        p1_rand_validity_for_p2 -= 1

    if not p1_rand_validity_for_p2 and (not p1_node or not p2_node):
        """ There were no matching, yet different nodes found between two parents """
        return None

    child1 = replace_node_by_path(parent1, p1_paths[p1_rand], p2_node)
    child2 = replace_node_by_path(parent2, p2_paths[p2_rand], p1_node)

    if child1 and child2 and child1 != parent1 and child2 != parent2:
        child1.update_metrics()
        child2.update_metrics()
        return child1, child2

    return None


crossover = crossover_flatten
