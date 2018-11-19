from World.Types import *
from World.Types.Place import Place, two_point_distance, triangle_distance


class Clan(BaseElement, Named):
    pass


class Person(Model):
    place = ForeignKeyField(Place, backref='persons')   # the place where Person currently is
    clan = ForeignKeyField(Clan, backref='members', null=True)
    health_meter = FloatField(default=1.0, constraints=[Check('health_meter >= 0.0'), Check('health_meter <= 1.0')])


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


class Player(BaseElement, Person, Named):
    next_location = ForeignKeyField(Place, backref='player_next_place', null=True)
    coins = IntegerField(default=0, constraints=[Check('coins >= 0')])

    def distance(self, candid_dest: Place) -> float:
        current = Place.get_by_id(self.place.id)
        if self.next_location is None:
            return two_point_distance(current, dest=candid_dest)

        # three point distance
        later = Place.get_by_id(self.next_location.id)
        return triangle_distance(current, dest=candid_dest, later=later)

    @staticmethod
    def current() -> 'Player':
        return Player.get()


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


list_of_models = [Clan, NPC, Motivation, Player, Enemies, Allies, PlayerEnemies, PlayerAllies]
