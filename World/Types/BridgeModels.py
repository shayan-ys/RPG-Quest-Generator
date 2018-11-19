from World.Types import *
from World.Types.Person import NPC, Player
from World.Types.Item import Item
from World.Types.Intel import Intel


class Need(BaseElement):
    npc = ForeignKeyField(NPC, backref='needs')
    item = ForeignKeyField(Item, null=True)
    intel = ForeignKeyField(Intel, null=True)
    item_count = IntegerField(default=1)


# class BelongItem(BaseElement):
#     npc = ForeignKeyField(NPC, backref='belongings')
#     item = ForeignKeyField(Item, backref='owners')
#     count = IntegerField(default=1)


# class BelongItemPlayer(BaseElement):
#     player = ForeignKeyField(Player, backref='belongings')
#     item = ForeignKeyField(Item, backref='owner_players')
#     count = IntegerField(default=1)


class Exchange(BaseElement):
    item = ForeignKeyField(Item, null=True)
    intel = ForeignKeyField(Intel, null=True)
    item_count = IntegerField(default=1)

    need = ForeignKeyField(Need, backref='exchanges')


class NPCKnowledgeBook(BaseElement):
    intel = ForeignKeyField(Intel, backref='npc_bridge')
    npc = ForeignKeyField(NPC, backref='intel_bridge')


class PlayerKnowledgeBook(BaseElement):
    intel = ForeignKeyField(Intel, backref='player_bridge')
    player = ForeignKeyField(Player, backref='intel_bridge_player')


class ReadableKnowledgeBook(BaseElement):
    intel = ForeignKeyField(Intel, backref='readable_bridge')
    readable = ForeignKeyField(Item, backref='intel_bridge')


class FavoursBook(BaseElement):
    # players favours book, how many favours he owes an NPC or they owe him
    # keeping track of who owes the player (+) and player owes to who(-).
    # ex: player1, npc1, owe_factor:+5 means npc1 owes 5 favour points to the player1
    npc = ForeignKeyField(NPC, backref='favours_records')
    owe_factor = SmallIntegerField(default=0)
    player = ForeignKeyField(Player, backref='player_favour_books')

    class Meta:
        indexes = (
            (('npc', 'owe_factor'), True),
        )

    @staticmethod
    def construct(npc: NPC, owe_factor: float, player: Player=None):
        if not player:
            player = Player.current()

        fav, created = FavoursBook.get_or_create(player=player, npc=npc, defaults={'owe_factor': owe_factor})
        if not created:
            fav.owe_factor += owe_factor


list_of_models = [Need, Exchange, NPCKnowledgeBook, PlayerKnowledgeBook, ReadableKnowledgeBook, FavoursBook]
