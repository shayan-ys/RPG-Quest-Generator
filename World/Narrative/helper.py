from World.Types.Item import Item
from World.Types.Person import Player
from World.Types.Intel import Intel
from World.Types.Place import Place
from World.Types.BridgeModels import PlayerKnowledgeBook
from World.Types.Names import PlaceName

from Data.statics import World as WorldParams
from random import random, randint


def add_item_place_intel(item: Item):
    player = Player.current()

    if item.place:
        PlayerKnowledgeBook.get_or_create(player=player, intel=Intel.construct(item_place=item))
        PlayerKnowledgeBook.get_or_create(player=player, intel=Intel.construct(place_location=item.place))
    elif item.belongs_to:
        PlayerKnowledgeBook.get_or_create(player=player, intel=Intel.construct(holding_item=item,
                                                                               holding_holder=item.belongs_to))
        PlayerKnowledgeBook.get_or_create(player=player, intel=Intel.construct(npc_place=item.belongs_to))
        PlayerKnowledgeBook.get_or_create(player=player, intel=Intel.construct(place_location=item.belongs_to.place))
    else:
        # player has the item
        pass

    return True


def add_intel(intel: Intel):
    player = Player.current()
    PlayerKnowledgeBook.get_or_create(player=player, intel=intel)

    # add additional intel if needed
    if intel.npc_place:
        place = intel.npc_place.place
        PlayerKnowledgeBook.get_or_create(player=player, intel=Intel.construct(place_location=place))

    elif intel.item_place:
        add_item_place_intel(intel.item_place)


def create_place():
    player = Player.current()
    player_place = player.place  # type: Place
    new_x = abs(player_place.x
                + randint(WorldParams.minimum_distance, WorldParams.reachable_distance)
                * (1 if random() < 0.5 else -1))
    new_y = abs(player_place.y
                + randint(WorldParams.minimum_distance, WorldParams.reachable_distance)
                * (1 if random() < 0.5 else -1))
    place_to_go = Place.create(name=PlaceName.fetch_new(), x=new_x, y=new_y)
    PlayerKnowledgeBook.create(player=player, intel=Intel.construct(place_location=place_to_go))

    return place_to_go
