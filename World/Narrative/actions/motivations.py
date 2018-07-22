from Grammar.actions import NonTerminals as NT

from World.elements import BaseElement, NPC

from typing import List


def quest_neutral(elements: list, motivation: NT) -> (BaseElement, List[List[BaseElement]]):
    # select an ally NPC with a certain motivation
    results = []
    for elem in elements:
        if isinstance(elem, NPC):
            if elem.motivations \
                    and motivation in elem.motivations \
                    and elem.motivations[motivation] > 0.5:
                results.append(elem)

    if results:
        NPC_motivated = results[0]
    else:
        return None, []

    # steps:
    #   give useful info to this NPC
    steps = [
        [NPC_motivated]
    ]
    print("==> '%s' has '%s' motivation!" % (NPC_motivated, motivation.name))

    return NPC_motivated, steps


def quest_1(elements: list):
    """
    An NPC desires to know an intel
    :return:
    """
    return quest_neutral(elements, NT.knowledge)


def quest_2(elements: list):
    return quest_neutral(elements, NT.comfort)


def quest_3(elements: list):
    return quest_neutral(elements, NT.reputation)


def quest_4(elements: list):
    return quest_neutral(elements, NT.serenity)


def quest_5(elements: list):
    return quest_neutral(elements, NT.protection)


def quest_6(elements: list):
    return quest_neutral(elements, NT.conquest)


def quest_7(elements: list):
    return quest_neutral(elements, NT.wealth)


def quest_8(elements: list):
    return quest_neutral(elements, NT.ability)


def quest_9(elements: list):
    return quest_neutral(elements, NT.equipment)
