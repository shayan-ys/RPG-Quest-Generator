from Grammar.actions import NonTerminals as NT, Terminals as T
from Grammar.tree import Tree, Leaf, Node
import json


def serialize_tree(tree: Tree) -> dict:
    return tree.serialize()


def deserialize_tree_json(tree_json: dict) -> Tree:

    if 'action' not in tree_json:
        raise Exception("'action' key is not presented in JSON tree")

    branches = []
    if 'branches' in tree_json and tree_json['branches']:
        for branch_json in tree_json['branches']:
            branch = deserialize_tree_json(branch_json)
            branches.append(branch)

    if 'terminal' in tree_json and tree_json['terminal']:
        return Leaf(action=T(int(tree_json['action'])))
    else:
        # NonTerminal
        return Node(
            NT(int(tree_json['action'])),
            int(tree_json['rule']),
            *branches
        )


def deserialize_tree_json_str(tree_json_str: str) -> Tree:
    tree_dict = json.loads(tree_json_str)
    return deserialize_tree_json(tree_dict)


def write_file(tree: Tree):
    with open('Results/output.json', 'w') as outfile:
        json.dump(tree.serialize(), outfile)
