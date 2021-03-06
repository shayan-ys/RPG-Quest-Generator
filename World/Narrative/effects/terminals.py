from World.Types.BridgeModels import PlayerKnowledgeBook, NPCKnowledgeBook
from World.Types.Intel import Intel
from World.Types.Item import Item
from World.Types.Person import NPC, NPCDead, Player
from World.Types.Place import Place

"""return True if action is already done, look for its impact on the world"""


def null(*args):
    return True


def exchange(item_holder: NPC, item_to_give: Item, item_to_take: Item):
    player = Player.current()

    return item_to_take.belongs_to_player == player


def explore(area_location: Place, npc: NPC, item: Item):
    player = Player.current()

    if npc:
        intel = Intel.construct(npc_place=npc)
    elif item:
        intel = Intel.construct(item_place=item)
    else:
        intel = None

    if intel and not PlayerKnowledgeBook.get_or_none(player=player, intel=intel):
        return False

    return player.place == area_location


def gather(item_to_gather: Item):
    player = Player.current()

    return item_to_gather.belongs_to_player == player


def give(item: Item, receiver: NPC):
    return item.belongs_to == receiver


def spy(spy_on: NPC, intel_target: Intel):
    player = Player.current()

    return PlayerKnowledgeBook.get_or_none(player=player, intel=intel_target) is not None


def stealth(target: NPC):
    return False


def take(item_to_take: Item, item_holder: NPC=None):
    player = Player.current()

    return item_to_take.belongs_to_player == player


def read(intel: Intel, readable: Item):
    player = Player.current()

    return PlayerKnowledgeBook.get_or_none(player=player, intel=intel) is not None


def goto(destination: Place):
    player = Player.current()

    return player.place == destination


def damage(target: NPC):
    return target.health_meter < 1.0


def kill(target: NPC):
    if NPCDead.get_or_none(name=target.name):
        return True
    return target.health_meter == 0


def listen(intel: Intel, informer: NPC):
    player = Player.current()

    return PlayerKnowledgeBook.get_or_none(player=player, intel=intel) is not None


def report(intel: Intel, target: NPC):
    return NPCKnowledgeBook.get_or_none(npc=target, intel=intel) is not None


def use(item_to_use: Item, target: NPC):
    return False
