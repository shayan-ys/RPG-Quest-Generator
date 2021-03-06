from World.Types import *
from World.Types.Place import Place, two_point_distance, triangle_distance

from Grammar.actions import NonTerminals as NT, Terminals as T


class Clan(BaseElement, Named):
    pass


class Person(Model):
    place = ForeignKeyField(Place, backref='persons')   # the place_location where Person currently is
    clan = ForeignKeyField(Clan, backref='members', null=True)
    health_meter = FloatField(default=1.0, constraints=[Check('health_meter >= 0.0'), Check('health_meter <= 1.0')])


class NPC(BaseElement, Person, Named):
    # Non Player Character
    def save(self, force_insert=False, only=None):
        if self.id is not None:
            for dirty in self.dirty_fields:
                if isinstance(dirty, ForeignKeyField) \
                        and dirty.rel_model == Place:
                    try:
                        old_place = NPC.get_by_id(self.id).place
                    except:
                        old_place = None
                    if old_place != self.place:
                        # remove npc_place knowledge from every player's knowledge book
                        from World.Types.Intel import Intel
                        from World.Types.BridgeModels import PlayerKnowledgeBook
                        results = PlayerKnowledgeBook.select().join(Intel).where(Intel.npc_place == self.id)
                        for res in results:
                            res.delete_instance()
        super(NPC, self).save()

    def top_motive(self) -> ('Motivation', NT):
        results = Motivation.select().where(Motivation.npc == self.id).order_by(Motivation.motive.desc()).limit(1)

        if results:
            motive = results[0]  # type: Motivation
            return motive, NT(motive.action)

        return 0, T.null


class NPCDead(BaseElement, Person, Named):
    health_meter = FloatField(default=0)


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


list_of_models = [Clan, NPC, NPCDead, Motivation, Player]
