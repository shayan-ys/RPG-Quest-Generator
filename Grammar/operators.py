from Grammar.tree import Node, Leaf

import json
from copy import deepcopy
from Logger import logger
logger.name = __name__


def flat_non_terminals_subtrees(tree: Node) -> (list, list, list):
    """
    Flatten a tree to three lists, ignoring 'Terminals':
    - List of every subtrees
    - List of types of each node (NonTerminals), actually is root type of subtrees (the previous list)
    - List of 'paths' to reach the subtree, each path itself is a list of 'branch' index (starting from 0)
    :param tree: Input tree to be flatten
    :return: A tuple of three lists described above
    """

    def recursion(root: Node, root_path: list) -> (list, list, list):

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


def replace_node_by_path(tree: Node, path_in_tree: list, replace_by: Node) -> Node:
    """
    Finds the correct node in the 'tree', using the given 'path' to it, replace it with the given node in 'replace_by'
    :param tree: tree that one of its nodes are going to be replaced by something else
    :param path_in_tree: path to the node inside the tree, path is a list of branch indices
    :param replace_by: the node which will replace the existing one inside the tree
    :return: altered tree
    """

    def recursion(root: Node, path: list) -> Node:

        if path:
            res = recursion(root.branches[path[0]], path[1:])
            root.branches[path[0]] = res
        else:
            return replace_by

        return root

    try:
        new_tree = recursion(root=deepcopy(tree), path=path_in_tree)
        new_tree.update_metrics()
        return new_tree
    except Exception as e:
        logger.error("Error in replace node | tree: %s | path_in_tree: %s | exception: %s ",
                     json.dumps(tree), str(path_in_tree), str(e))
        return None


def get_node_by_path(tree: Node, path_in_tree: list) -> Node:

    def recursion(root: Node, path: list) -> Node:

        if path:
            return recursion(root.branches[path[0]], path[1:])
        else:
            return root

    return recursion(root=tree, path=path_in_tree)
