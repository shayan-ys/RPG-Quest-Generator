from World.Types import *
from World.Types.Place import Place


class Clan(BaseElement, Named):
    pass


class Person(Model):
    place = ForeignKeyField(Place, backref='persons')   # the place where Person currently is
    clan = ForeignKeyField(Clan, backref='members', null=True)


class NPC(BaseElement, Person, Named):
    # Non Player Character
    pass


class Motivation(BaseElement):
    npc = ForeignKeyField(NPC, backref='motivations')
    action = SmallIntegerField(default=0, constraints=[Check('action >= 0')])
    motive = FloatField(constraints=[Check('motive > 0.0'), Check('motive <= 1.0')])

    class Meta:
        indexes = (
            (('npc', 'action'), True),
        )


class FavoursBook(BaseElement):
    # players favours book, how many favours he owes an NPC or they owe him
    # keeping track of who owes the player (+) and player owes to who(-).
    npc = ForeignKeyField(NPC, backref='favours_records')
    owe_factor = SmallIntegerField(default=0)

    class Meta:
        indexes = (
            (('npc', 'owe_factor'), True),
        )


class Player(BaseElement, Person, Named):
    next_location = ForeignKeyField(Place, backref='player_next_place', null=True)
    coins = IntegerField(default=0, constraints=[Check('coins >= 0')])
    # favours_book = ForeignKeyField(FavoursBook, backref='players')


class Enemies(BaseElement):
    npc_one = ForeignKeyField(NPC)
    npc_two = ForeignKeyField(NPC)

    class Meta:
        indexes = (
            (('npc_one', 'npc_two'), True),
        )


class Allies(BaseElement):
    npc_one = ForeignKeyField(NPC)
    npc_two = ForeignKeyField(NPC)

    class Meta:
        indexes = (
            (('npc_one', 'npc_two'), True),
        )


class PlayerEnemies(BaseElement):
    player = ForeignKeyField(NPC)
    npc = ForeignKeyField(NPC)

    class Meta:
        indexes = (
            (('player', 'npc',), True),
        )


class PlayerAllies(BaseElement):
    player = ForeignKeyField(NPC)
    npc = ForeignKeyField(NPC)

    class Meta:
        indexes = (
            (('player', 'npc',), True),
        )


list_of_models = [Clan, NPC, Motivation, FavoursBook, Player, Enemies, Allies, PlayerEnemies, PlayerAllies]
