from Grammar.actions import Terminals as T

from World.Types import *
from World.Types.Person import NPC, Player
from World.Types.Place import Place


from enum import Enum, auto


class ItemTypes(Enum):
    unknown = auto()
    tool = auto()
    readable = auto()
    singleton = auto()


class GenericItem(BaseElement, Named):
    pass


class Item(BaseElement, Worthy, Named):
    default_worth = 0.0
    generic = ForeignKeyField(GenericItem, backref='instances')
    place = ForeignKeyField(Place, backref='items', null=True)
    belongs_to = ForeignKeyField(NPC, backref='belongings', null=True)
    belongs_to_player = ForeignKeyField(Player, backref='player_belongings', null=True)
    type = CharField(choices=[(en.value, en.name) for en in ItemTypes])
    usage = SmallIntegerField(constraints=[Check('usage >= 0')], null=True)
    impact_factor = FloatField(null=True, constraints=[Check('impact_factor > 0'), Check('impact_factor <= 1')])

    def place_(self):
        if self.place:
            return self.place
        elif self.belongs_to:
            return self.belongs_to.place
        elif self.belongs_to_player:
            return Player.current().place
        else:
            return None

    def is_singleton(self) -> bool:
        return GenericItem.get_by_id(self.generic.id).name == ItemTypes.singleton.name

    def use(self, npc: NPC):
        if self.usage == T.treat.value:
            npc.health_meter += self.impact_factor
            npc.health_meter = max(0, min(1, npc.health_meter))
            npc.save()

    def save(self, force_insert=False, only=None):
        if self.id is not None:
            for dirty in self.dirty_fields:
                if isinstance(dirty, ForeignKeyField) \
                        and dirty.rel_model == Place:
                    try:
                        old_place = Item.get_by_id(self.id).place
                    except:
                        old_place = None
                    if old_place != self.place:
                        # remove item_place knowledge from every player's knowledge book
                        from World.Types.Intel import Intel
                        from World.Types.BridgeModels import PlayerKnowledgeBook
                        results = PlayerKnowledgeBook.select().join(Intel).where(Intel.item_place == self.id)
                        for res in results:
                            res.delete_instance()
        super(Item, self).save()


list_of_models = [GenericItem, Item]
