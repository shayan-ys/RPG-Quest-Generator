from World.Types import *
from World.Types.Item import Item
from World.Types.Person import NPC, Player
from World.Types.Place import Place

from enum import Enum, auto


class IntelTypes(Enum):
    spell = auto()
    place = auto()
    holding = auto()


class Intel(BaseElement, Worthy):
    type = CharField()
    spell = CharField(null=True)
    npc_place = ForeignKeyField(NPC, backref='intel_place', null=True)
    holding_item = ForeignKeyField(Item, backref='intel_on_holder', null=True)
    holding_holder = ForeignKeyField(NPC, backref='intel_on_belonging', null=True)

    def data(self):
        if self.type == str(IntelTypes.spell.name):
            return self.spell
        elif self.type == str(IntelTypes.place.name):
            return self.npc_place
        elif self.type == str(IntelTypes.holding.name):
            return self.holding_item, self.holding_holder

    def __str__(self):
        if not self.type:
            return str(self.type)
        return str(self.type) + ': ' + str(self.data())


class NPCKnowledgeBook(BaseElement):
    intel = ForeignKeyField(Intel, backref='npc_bridge')
    npc = ForeignKeyField(NPC, backref='intel_bridge')


class PlayerKnowledgeBook(BaseElement):
    intel = ForeignKeyField(Intel, backref='player_bridge')
    player = ForeignKeyField(Player, backref='intel_bridge_player')


class ReadableKnowledgeBook(BaseElement):
    intel = ForeignKeyField(Intel, backref='readable_bridge')
    readable = ForeignKeyField(Item, backref='intel_bridge')


list_of_models = [Intel, NPCKnowledgeBook, PlayerKnowledgeBook, ReadableKnowledgeBook]
