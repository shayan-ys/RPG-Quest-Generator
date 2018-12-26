from World.Types import *

from random import randint


class BaseName(Model):
    used = BooleanField(default=False)
    base = ''

    @staticmethod
    def fetch_from_model(model) -> str:
        results = model.select().where(model.used == False).order_by(fn.Random()).limit(1)
        if results:
            obj = results[0]
            obj.used = True
            obj.save()
            return obj.name
        else:
            return 'arbitrary_' + model.base + '_' + str(randint(100, 999))


class NPCName(BaseElement, BaseName, Named):
    base = 'npc'

    @staticmethod
    def fetch_new() -> str:
        return BaseName.fetch_from_model(NPCName)


class ItemName(BaseElement, BaseName, Named):
    base = 'item'

    @staticmethod
    def fetch_new() -> str:
        return BaseName.fetch_from_model(ItemName)


class PlaceName(BaseElement, BaseName, Named):
    base = 'place'

    @staticmethod
    def fetch_new() -> str:
        return BaseName.fetch_from_model(PlaceName)


class SpellName(BaseElement, BaseName, Named):
    base = 'spell'

    @staticmethod
    def fetch_new() -> str:
        return BaseName.fetch_from_model(SpellName)


list_of_models = [NPCName, ItemName, PlaceName, SpellName]
