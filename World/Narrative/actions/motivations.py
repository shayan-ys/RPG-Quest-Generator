from Grammar.actions import NonTerminals as NT

from World.elements import list_of_elements, BaseElement, NPC


def quest_1(elements: list):
    """
    An NPC desires to know an intel
    :return:
    """
    # select an ally NPC with knowledge motivation
    results = []
    for elem in elements:
        elem = elem     # type: BaseElement
        if isinstance(elem, NPC):
            if elem.motivations \
                    and NT.knowledge in elem.motivations \
                    and elem.motivations[NT.knowledge] > 0.5:
                results.append(elem)

    if results:
        NPC_knowledge_motivated = results[0]
    else:
        return None, []

    # steps:
    #   give useful info to this NPC
    steps = [
        [NPC_knowledge_motivated]
    ]
    print("==> '%s' wants to know something useful!" % NPC_knowledge_motivated)

    return NPC_knowledge_motivated, steps
