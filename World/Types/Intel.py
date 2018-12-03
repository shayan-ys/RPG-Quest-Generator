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
    location = auto()
    npc_place = auto()
    # item_place is a general information about an item's place, belonging (to an NPC), or the player himself
    item_place = auto()
    # probably should be removed since item_place is generalized
    holding = auto()
    other = auto()


class Intel(BaseElement, Worthy):
    default_worth = 0.5
    type = CharField()
    spell = ForeignKeyField(Spell, backref='intel_spell', null=True)
    place_location = ForeignKeyField(Place, backref='intel_place_location', null=True)
    npc_place = ForeignKeyField(NPC, backref='intel_npc_place', null=True)
    item_place = ForeignKeyField(Item, backref='intel_item_place', null=True)
    holding_item = ForeignKeyField(Item, backref='intel_on_holder', null=True)
    holding_holder = ForeignKeyField(NPC, backref='intel_on_belonging', null=True)

    def data(self):
        if self.type == str(IntelTypes.spell.name):
            return self.spell
        elif self.type == str(IntelTypes.location.name):
            return self.place_location
        elif self.type == str(IntelTypes.npc_place.name):
            return self.npc_place
        elif self.type == str(IntelTypes.item_place.name):
            return self.item_place
        elif self.type == str(IntelTypes.holding.name):
            return str(self.holding_item), str(self.holding_holder)

    @staticmethod
    def construct(spell: Spell=None, place_location: Place=None, npc_place: NPC=None, item_place: Item=None,
                  holding_item: Item=None, holding_holder: NPC=None, worth: float=None) -> 'Intel':
        if spell:
            intel_type = IntelTypes.spell
        elif place_location:
            intel_type = IntelTypes.location
        elif npc_place:
            intel_type = IntelTypes.npc_place
        elif item_place:
            intel_type = IntelTypes.item_place
        elif holding_item and holding_holder:
            intel_type = IntelTypes.holding
        else:
            intel_type = IntelTypes.other

        if not worth:
            worth = Intel.default_worth

        intel, created = Intel.get_or_create(
            type=intel_type.name, spell=spell, place_location=place_location, npc_place=npc_place, item_place=item_place,
            holding_item=holding_item, holding_holder=holding_holder, worth=worth)

        return intel

    @staticmethod
    def find_by_name(intel_type: str, *args) -> 'Intel' or None:
        if intel_type == IntelTypes.spell.name:
            return Intel.select().join(Spell).where(Intel.type == intel_type, Spell.name == args[0]).get()

        elif intel_type == IntelTypes.location.name:
            return Intel.select().join(Place, on=(Intel.place_location == Place.id))\
                .where(Intel.type == intel_type, Place.name == args[0]).get()

        elif intel_type == IntelTypes.npc_place.name:
            return Intel.select().join(NPC, on=(Intel.npc_place == NPC.id))\
                .where(Intel.type == intel_type, NPC.name == args[0]).get()

        elif intel_type == IntelTypes.item_place.name:
            return Intel.select().join(Item, on=(Intel.item_place == Item.id))\
                .where(Intel.type == intel_type, Item.name == args[0]).get()

        elif intel_type == IntelTypes.holding.name:
            return Intel.select()\
                .join(Item, on=(Intel.holding_item == Item.id))\
                .where(Intel.type == intel_type, Item.name == args[0]).get()
        return None

    def __str__(self):
        if not self.type:
            return str(self.type)
        return str(self.data())


list_of_models = [Intel, Spell]
