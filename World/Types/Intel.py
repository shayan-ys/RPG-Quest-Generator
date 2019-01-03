from World.Types import *
from World.Types.Item import Item
from World.Types.Person import NPC
from World.Types.Place import Place
from World.Types.Log import Message

from Data.statics import Playground as PlayParams

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
    other = auto()


class Intel(BaseElement, Worthy):
    default_worth = 0.5
    type = CharField()
    spell = ForeignKeyField(Spell, backref='intel_spell', null=True)
    place_location = ForeignKeyField(Place, backref='intel_place_location', null=True)
    npc_place = ForeignKeyField(NPC, backref='intel_npc_place', null=True)
    item_place = ForeignKeyField(Item, backref='intel_item_place', null=True)
    other = CharField(null=True)

    def data(self):
        if self.type == str(IntelTypes.spell.name):
            return self.spell
        elif self.type == str(IntelTypes.location.name):
            return self.place_location
        elif self.type == str(IntelTypes.npc_place.name):
            return self.npc_place
        elif self.type == str(IntelTypes.item_place.name):
            return self.item_place
        else:
            return self.other

    @staticmethod
    def construct(spell: Spell=None, place_location: Place=None, npc_place: NPC=None, item_place: Item=None,
                  other: str=None, worth: float=None) -> 'Intel':
        if not worth:
            worth = Intel.default_worth

        if spell:
            intel, created = Intel.get_or_create(type=IntelTypes.spell.name, spell=spell, defaults={'worth': worth})
        elif place_location:
            intel, created = Intel.get_or_create(type=IntelTypes.location.name, place_location=place_location,
                                                 defaults={'worth': worth})
        elif npc_place:
            intel, created = Intel.get_or_create(type=IntelTypes.npc_place.name, npc_place=npc_place,
                                                 defaults={'worth': worth})
        elif item_place:
            intel, created = Intel.get_or_create(type=IntelTypes.item_place.name, item_place=item_place,
                                                 defaults={'worth': worth})
        else:
            intel, created = Intel.get_or_create(type=IntelTypes.other.name, other=other, defaults={'worth': worth})

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
        elif intel_type == IntelTypes.other.name:
            return Intel.select()\
                .where(Intel.type == intel_type, Intel.other == args[0]).get()
        return None

    @staticmethod
    def delete_all_arbitrary():
        # delete all Spell intel
        results = Intel.select(Intel.id).join(Spell).where(Spell.name.contains('arbitrary'))
        # delete all Place intel
        results += Intel.select(Intel.id).join(Place, on=(Intel.place_location == Place.id))\
            .where(Place.name.contains('arbitrary'))
        # delete all NPC intel
        results += Intel.select(Intel.id).join(NPC, on=(Intel.npc_place == NPC.id))\
            .where(NPC.name.contains('arbitrary'))
        # delete all Item intel
        results += Intel.select(Intel.id).join(Item, on=(Intel.item_place == Item.id))\
            .where(Item.name.contains('arbitrary'))
        # delete all Other intel
        results += Intel.select(Intel.id).where(Intel.other.contains('arbitrary'))
        results = list(results)

        query = Intel.delete().where(Intel.id.in_(results))
        query.execute()

    def __str__(self) -> str:
        if not self.type:
            return str(self.type)

        if self.type == str(IntelTypes.spell.name):
            return str(self.spell) + " spell"
        elif self.type == str(IntelTypes.location.name):
            return str(self.place_location) + " location"
        elif self.type == str(IntelTypes.npc_place.name) or self.type == str(IntelTypes.item_place.name):
            if self.npc_place:
                if PlayParams.debug_mode:
                    return "%s's place (%s)" % (self.npc_place, self.npc_place.place)
                else:
                    return "%s's place" % self.npc_place
            elif self.item_place:
                if PlayParams.debug_mode:
                    return "%s's place (%s)" % (self.item_place, self.item_place.place)
                else:
                    return "%s's place" % self.item_place
            else:
                Message.debug(
                    "Error! neither item_place nor npc_place but type: %s. Intel id:%i" % (self.type, self.id))
                return "unknown"
        else:
            # self.type == str(IntelTypes.other.name)
            return str(self.other)

    def detail(self) -> str:
        if not self.type:
            return str(self.type)

        if self.type == str(IntelTypes.spell.name):
            return "spell %s: %s" % (self.spell, self.spell.text)
        elif self.type == str(IntelTypes.location.name):
            return "location %s is at: %s,%s" % (self.place_location, self.place_location.x, self.place_location.y)
        elif self.type == str(IntelTypes.npc_place.name) or self.type == str(IntelTypes.item_place.name):
            if self.npc_place:
                return "NPC %s located at %s" % (self.npc_place, self.npc_place.place)
            elif self.item_place:
                return "Item %s located at %s" % (self.item_place, self.item_place.place)
            else:
                Message.debug(
                    "Error! neither item_place nor npc_place but type: %s. Intel id:%i" % (self.type, self.id))
                return "unknown"
        else:
            # self.type == str(IntelTypes.other.name)
            return str(self.other)


list_of_models = [Intel, Spell]
