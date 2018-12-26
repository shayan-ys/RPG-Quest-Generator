from World.Types import fn, JOIN
from World.Types import BaseElement
from World.Types.Person import Clan, NPC, Motivation
from World.Types.Place import Place
from World.Types.Log import Message

from Grammar.actions import NonTerminals as NT

from random import randint
from typing import List


def quest_neutral(motivation: NT) -> List[List[BaseElement]]:
    # select an ally NPC with a certain motivation

    results = Motivation.select()\
        .where(Motivation.action == motivation.value,
               Motivation.motive > 0.5)\
        .order_by(Motivation.motive.desc()).limit(1)

    if results:
        motivated = results.get().npc
    else:
        # No motivated NPC found, create one
        place = Place.select().order_by(fn.Random()).get()
        clan = Clan.select().order_by(fn.Random()).get()
        motivated = NPC.create(place=place, clan=clan, name='arbitrary_npc_' + str(randint(100, 999)))
        Motivation.create(npc=motivated, action=motivation.value, motive=0.65)

    # steps:
    #   give useful info to this NPC
    steps = [
        [motivated]
    ]
    # print("==> '%s' has '%s' motivation!" % (motivated.name, motivation.name))
    Message.instruction("NPC '%s' has '%s' motivation" % (motivated.name, motivation.name))
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
