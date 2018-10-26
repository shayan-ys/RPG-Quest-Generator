from World.Narrative.effects import terminals

from Grammar.tree import Node


def not_done(*args, **kwargs) -> bool:
    return False


def is_done_method(node: Node) -> callable:
    if not node.branches:
        return getattr(terminals, node.action.name)

    return not_done
