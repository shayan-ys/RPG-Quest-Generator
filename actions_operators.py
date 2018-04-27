from actions import Node, Leaf
from helper import nwise

from collections import Counter


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


def length_event(event) -> int:
    return 1
