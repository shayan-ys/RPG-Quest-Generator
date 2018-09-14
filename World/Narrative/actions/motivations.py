from Grammar.actions import NonTerminals as NT

from World.elements import BaseElement, NPC
from World.Types.Person import Motivation

from typing import List


def quest_neutral(motivation: NT) -> (BaseElement, List[List[BaseElement]]):
    # select an ally NPC with a certain motivation

    NPC_motivated = Motivation.select()\
        .where(Motivation.action == motivation.value,
               Motivation.motive > 0.5)\
        .order_by(Motivation.motive.desc()).get().npc

    # steps:
    #   give useful info to this NPC
    steps = [
        [NPC_motivated]
    ]
    print("==> '%s' has '%s' motivation!" % (NPC_motivated.name, motivation.name))

    return steps


def quest_1():
    """
    An NPC desires to know an intel
    :return:
    """
    return quest_neutral(NT.knowledge)


def quest_2():
    return quest_neutral(NT.comfort)


def quest_3():
    return quest_neutral(NT.reputation)


def quest_4():
    return quest_neutral(NT.serenity)


def quest_5():
    return quest_neutral(NT.protection)


def quest_6():
    return quest_neutral(NT.conquest)


def quest_7():
    return quest_neutral(NT.wealth)


def quest_8():
    return quest_neutral(NT.ability)


def quest_9():
    return quest_neutral(NT.equipment)
