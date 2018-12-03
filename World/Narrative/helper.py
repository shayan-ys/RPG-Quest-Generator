from World.Types.Item import Item
from World.Types.Person import Player
from World.Types.Intel import Intel
from World.Types.BridgeModels import PlayerKnowledgeBook


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
