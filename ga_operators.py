from statics import terminal_xp_map
from helper import list_to_str, nwise, bell_curve
from quests import *

from collections import Counter
import random


def pattern_finder(items: list, pat_length: int=2, min_repeat: int=2, in_order: bool=True) -> (int, int):

    repeats_list = []
    found_indices = []

    for index, comp_base in enumerate(nwise(items, n=pat_length)):

        if index in found_indices:
            # this pattern is already counted, nothing new will be found here. => skip!
            continue
        repeats = 1

        for index_needle, comp_needle in enumerate(nwise(items[index+1:], n=pat_length)):
            if (in_order and comp_base == comp_needle) or (not in_order and set(comp_base) == set(comp_needle)):
                # print(str(list(x.name for x in comp_base)) + " == " + str(list(x.name for x in comp_needle)))
                repeats += 1
                found_indices.append(index_needle)

        if repeats >= min_repeat:
            repeats_list.append(repeats)

    return [(r, s) for r, s in Counter(repeats_list).items()]


def repetition_factor(flatten_events: list, pattern_min_length: int=2, pattern_max_length: int=None) -> float:
    if not pattern_max_length:
        pattern_max_length = int(len(flatten_events) / 2)

    q = 0
    for n in range(pattern_min_length, pattern_max_length):
        for r, s in pattern_finder(flatten_events, pat_length=n, min_repeat=2):
            q += n * r * s

    return q


def flat_non_terminals_subtrees(root: Node, root_path: list=None) -> (list, list):
    if not root.branches:
        return [], [], []

    flatten = [root]
    types_flatten = [root.action]
    if not root_path:
        root_path = []
    path = [root_path]

    for index, branch in enumerate(root.branches):
        if type(branch) == Leaf:
            continue
        subtree_flatten, subtree_types_flatten, sub_path = flat_non_terminals_subtrees(branch, root_path + [index])
        flatten += subtree_flatten
        types_flatten += subtree_types_flatten
        path += sub_path

    return flatten, types_flatten, path


def replace_node_by_path(root: Node, path: list, replace_by: Node) -> Node:

    if path:
        root.branches[path[0]] = replace_node_by_path(root.branches[path[0]], path[1:], replace_by)
    else:
        return replace_by

    return root


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

    # print(p1_rand)
    # print(p2_rand)

    p1_node = p1_flat[p1_rand]
    p2_node = p2_flat[p2_rand]

    child1 = replace_node_by_path(parent1, p1_paths[p1_rand], p2_node)
    child2 = replace_node_by_path(parent2, p2_paths[p2_rand], p1_node)

    return child1, child2


print("----- cure -----")
print(list_to_str(cure.flatten))

# patterns = pattern_finder(cure.flatten, pat_length=2, in_order=True)
# print(patterns)


def length_event(event) -> int:
    return 1


print("repr_factor= " + str(repetition_factor(cure.flatten, pattern_max_length=3)))
print("length_factor= " + str(sum(map(length_event, cure.flatten))))
print("xp_factor= " + str(sum(map(terminal_xp_map, cure.flatten))))
print("occurrence_factor= " + str(cure.flatten.count(T.kill)))

f_cure = (
             bell_curve(repetition_factor(cure.flatten, pattern_max_length=4), opt_value=0, scaling_value=(1/1024)) +
             bell_curve(sum(map(length_event, cure.flatten)), opt_value=24, scaling_value=(1/8)) +
             bell_curve(sum(map(terminal_xp_map, cure.flatten)), opt_value=25, scaling_value=(1/8))
         ) / 3

print("fitness: cure= " + str(f_cure))

print("----- spy -----")
print(list_to_str(spy.flatten))
print("repr_factor= " + str(repetition_factor(spy.flatten, pattern_max_length=3)))
print("length_factor= " + str(sum(map(length_event, spy.flatten))))
print("xp_factor= " + str(sum(map(terminal_xp_map, spy.flatten))))
print("occurrence_factor= " + str(spy.flatten.count(T.kill)))

print("------- flat non_terminals subtree - arbitrary quest 2 ------")
flatten_subtrees_arbitrary_2, flatten_types_arbitrary_2, path_nodes_arbitrary_2 = flat_non_terminals_subtrees(arbitrary_quest2)
print(flatten_types_arbitrary_2)
print(["".join(map(str, path_ls)) for path_ls in path_nodes_arbitrary_2])
# print(path_nodes_arbitrary_2)
for subtree in flatten_subtrees_arbitrary_2:
    print(subtree)

print("------- flat non_terminals subtree - arbitrary quest 1 ------")
flatten_subtrees_arbitrary_1, flatten_types_arbitrary_1, path_nodes_arbitrary_1 = flat_non_terminals_subtrees(arbitrary_quest1)
print(flatten_types_arbitrary_1)
print(["".join(map(str, path_ls)) for path_ls in path_nodes_arbitrary_1])
for subtree in flatten_subtrees_arbitrary_1:
    print(subtree)

print("------- find sub-tree - arbitrary quest 1 ------")
steal_type_2 = Node(NT.steal, 2,
                    Node(NT.goto, 1,
                         Leaf(T.null)),
                    Node(NT.kill, 1,
                         Node(NT.goto, 1,
                              Leaf(T.null)),
                         Leaf(T.kill)),
                    Leaf(T.take))
subtree_arbitrary_1 = replace_node_by_path(arbitrary_quest1, [0, 0, 0, 1, 0], steal_type_2)
print(subtree_arbitrary_1)

# NonTerminals.quest(1):{NonTerminals.knowledge(3):{NonTerminals.goto(3):{NonTerminals.learn(3):{NonTerminals.goto(1):{Terminals.null}, NonTerminals.get(2):{NonTerminals.steal(1):{NonTerminals.goto(2):{Terminals.explore}, Terminals.stealth, Terminals.take}}, Terminals.read}, Terminals.goto}, Terminals.listen, NonTerminals.goto(1):{Terminals.null}, Terminals.report}}
# NonTerminals.quest(1):{NonTerminals.knowledge(3):{NonTerminals.goto(3):{NonTerminals.learn(3):{NonTerminals.goto(1):{Terminals.null}, NonTerminals.get(2):{NonTerminals.steal(2):{NonTerminals.goto(1):{Terminals.null}, NonTerminals.kill(1):{NonTerminals.goto(1):{Terminals.null}, Terminals.kill}, Terminals.take}}, Terminals.read}, Terminals.goto}, Terminals.listen, NonTerminals.goto(1):{Terminals.null}, Terminals.report}}

print("------- Crossover - arbitrary quest 1 & 2 ----------")
arb_child1, arb_child2 = crossover_flatten(arbitrary_quest1, arbitrary_quest2)
print(arb_child1)
print(arb_child2)
