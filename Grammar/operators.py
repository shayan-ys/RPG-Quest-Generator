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
                repeats += 1
                found_indices.append(index_needle)

        if repeats >= min_repeat:
            repeats_list.append(repeats)

    return [(r, s) for r, s in Counter(repeats_list).items()]


def flat_non_terminals_subtrees(tree: Node) -> (list, list):
    """
    Flatten a tree to three lists, ignoring 'Terminals':
    - List of every subtrees
    - List of types of each node (NonTerminals), actually is root type of subtrees (the previous list)
    - List of 'paths' to reach the subtree, each path itself is a list of 'branch' index (starting from 0)
    :param tree: Input tree to be flatten
    :return: A tuple of three lists described above
    """

    def recursion(root: Node, root_path: list) -> (list, list):

        if not root or not root.branches:
            return [], [], []

        flatten = [root]
        types_flatten = [root.action]
        path = [root_path]

        for index, branch in enumerate(root.branches):
            if type(branch) == Leaf or not branch or not branch.branches:
                continue
            subtree_flatten, subtree_types_flatten, sub_path = recursion(branch, root_path + [index])
            flatten += subtree_flatten
            types_flatten += subtree_types_flatten
            path += sub_path

        return flatten, types_flatten, path

    return recursion(root=tree, root_path=[])


def replace_node_by_path(root: Node, path: list, replace_by: Node) -> Node:

    if path:
        root.branches[path[0]] = replace_node_by_path(root.branches[path[0]], path[1:], replace_by)
    else:
        return replace_by

    return root


def length_event(event) -> int:
    return 1
