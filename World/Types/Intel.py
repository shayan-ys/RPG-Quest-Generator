from World.Types import *
from World.Types.Item import Item
from World.Types.Person import NPC, Player
from World.Types.Place import Place

from enum import Enum, auto


class Spell(BaseElement):
    name = CharField()
    text = CharField()

    def __str__(self):
        # return self.name + " (\"" + self.text + "\")"
        return self.name


class IntelTypes(Enum):
    spell = auto()
    place = auto()
    holding = auto()


class Intel(BaseElement, Worthy):
    type = CharField()
    spell = ForeignKeyField(Spell, backref='intel_spell', null=True)
    place = ForeignKeyField(Place, backref='intel_place', null=True)
    npc_place = ForeignKeyField(NPC, backref='intel_npc_place', null=True)
    holding_item = ForeignKeyField(Item, backref='intel_on_holder', null=True)
    holding_holder = ForeignKeyField(NPC, backref='intel_on_belonging', null=True)

    def data(self):
        if self.type == str(IntelTypes.spell.name):
            return self.spell
        elif self.type == str(IntelTypes.place.name):
            return self.place
        elif self.type == str(IntelTypes.holding.name):
            return str(self.holding_item), str(self.holding_holder)

    @staticmethod
    def find_by_name(intel_type: str, *args) -> 'Intel' or None:
        if intel_type == IntelTypes.spell.name:
            return Intel.select().join(Spell).where(Intel.type == intel_type, Spell.name == args[0]).get()
        elif intel_type == IntelTypes.place.name:
            return Intel.select().join(Place).where(Intel.type == intel_type, Place.name == args[0]).get()
        elif intel_type == IntelTypes.holding.name:
            return Intel.select()\
                .join(Item, on=(Intel.holding_item == Item.id))\
                .where(Intel.type == intel_type, Item.name == args[0]).get()
        return None

    def __str__(self):
        if not self.type:
            return str(self.type)
        return str(self.type) + ': ' + str(self.data())


list_of_models = [Intel, Spell]
