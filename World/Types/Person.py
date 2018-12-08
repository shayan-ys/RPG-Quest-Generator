from World.Types import *
from World.Types.Place import Place, two_point_distance, triangle_distance


class Clan(BaseElement, Named):
    pass


class Person(Model):
    place = ForeignKeyField(Place, backref='persons')   # the place_location where Person currently is
    clan = ForeignKeyField(Clan, backref='members', null=True)
    health_meter = FloatField(default=1.0, constraints=[Check('health_meter >= 0.0'), Check('health_meter <= 1.0')])


class NPC(BaseElement, Person, Named):
    # Non Player Character
    def save(self, force_insert=False, only=None):
        for dirty in self.dirty_fields:
            if isinstance(dirty, ForeignKeyField) \
                    and dirty.rel_model == Place:
                try:
                    old_place = NPC.get_by_id(self.id).place
                except:
                    old_place = None
                if old_place != self.place:
                    print("place changed! from", old_place, "to", self.place)
                    # remove npc_place knowledge from every player's knowledge book
                    from World.Types.Intel import Intel
                    from World.Types.BridgeModels import PlayerKnowledgeBook
                    results = PlayerKnowledgeBook.select().join(Intel).where(Intel.npc_place == self.id)
                    for res in results:
                        res.delete_instance()
        super(NPC, self).save()


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
