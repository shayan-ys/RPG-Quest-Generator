from Grammar.actions import NonTerminals as NT
from Grammar.tree import Node
from World.Narrative.results import motivations, strategies, non_terminals, terminals


def find(node: Node) -> callable:
    if node.action == NT.quest:
        return getattr(motivations, 'quest')
    elif node.action in [NT.knowledge, NT.comfort, NT.reputation, NT.serenity, NT.protection, NT.conquest,
                         NT.wealth, NT.ability, NT.equipment]:
        return getattr(strategies, '%s' % node.action.name)
    elif node.rule:
        return getattr(non_terminals, '%s' % node.action.name)
    else:
        return getattr(terminals, '%s' % node.action.name)
