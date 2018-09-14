from World.Types import *
from World.Types.Person import NPC, Player
from World.Types.Item import Item
from World.Types.Intel import Intel


class Need(BaseElement):
    npc = ForeignKeyField(NPC, backref='needs')
    item = ForeignKeyField(Item, null=True)
    intel = ForeignKeyField(Intel, null=True)
    item_count = IntegerField(default=1)


class BelongItem(BaseElement):
    npc = ForeignKeyField(NPC, backref='belongings')
    item = ForeignKeyField(Item, backref='owners')
    count = IntegerField(default=1)


class BelongItemPlayer(BaseElement):
    player = ForeignKeyField(Player, backref='belongings')
    item = ForeignKeyField(Item, backref='owner_players')
    count = IntegerField(default=1)


class Exchange(BaseElement):
    item = ForeignKeyField(Item, null=True)
    intel = ForeignKeyField(Intel, null=True)
    item_count = IntegerField(default=1)

    need = ForeignKeyField(Need, backref='exchanges')


list_of_models = [Need, BelongItem, BelongItemPlayer, Exchange]
