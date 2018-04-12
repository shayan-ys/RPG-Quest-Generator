from actions import *

print(tree)


def to_list(root: Node) -> list:
    traversed = [root.action]

    if root.branches:

        branches_only_terminals = True

        for branch in root.branches:
            temp_branch_listed = to_list(branch)
            if branches_only_terminals and len(temp_branch_listed) > 0 and type(temp_branch_listed[0]) != T:
                branches_only_terminals = False
            traversed += temp_branch_listed

        if branches_only_terminals:
            traversed = [root.action]

    elif type(root) == Node:
        # Not a leaf, but doesn't have any branch
        traversed = []
    return traversed


tree_small = Node(NT.steal, 1,
                  Node(NT.goto, 3,
                       Node(NT.learn, 1),
                       Leaf(T.goto)),
                  Leaf(T.stealth),
                  Leaf(T.take))
flatten = to_list(tree_small)

flt_str_list = []
for flt in flatten:
    flt_str_list.append(flt.name if type(flt) == T else "<" + flt.name + ">")

print(", ".join(flt_str_list))
