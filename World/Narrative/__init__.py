from Grammar.actions import NonTerminals as NT
from Grammar.tree import Node
from World.Narrative.actions import motivations, strategies, non_terminals, terminals


def find(node: Node, depth: int=None) -> callable:
    if node.action == NT.quest and depth == 0:
        return getattr(motivations, 'quest_%d' % node.rule)
    elif depth == 1 and node.action in [NT.knowledge, NT.comfort, NT.reputation, NT.serenity, NT.protection,
                                        NT.conquest, NT.wealth, NT.ability, NT.equipment]:
        return getattr(strategies, '%s_%d' % (node.action.name, node.rule))
    elif node.rule:
        return getattr(non_terminals, '%s_%d' % (node.action.name, node.rule))
    else:
        return getattr(terminals, '%s' % node.action.name)
