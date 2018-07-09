from Grammar.actions import NonTerminals as NT

from World.elements import Element
from World.types import NPC


def quest_1(elements: list):
    """
    An NPC desires to know an intel
    :return:
    """
    # select an ally NPC with knowledge motivation
    results = []
    for elem in elements:
        elem = elem     # type: Element
        if isinstance(elem.type, NPC):
            if elem.type.motivations and NT.knowledge in elem.type.motivations:
                results.append(elem)
    return results
