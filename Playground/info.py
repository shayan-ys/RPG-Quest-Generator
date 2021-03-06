from World.Types.BridgeModels import PlayerKnowledgeBook, NPCKnowledgeBook
from World.Types.Intel import Intel, IntelTypes
from World.Types.Item import Item
from World.Types.Person import NPC, Player

from Data.statics import Playground as Params


def print_indented(data: list):
    for i in data:
        print(" --", i)


def print_player_intel(player: Player=None, print_locations: bool=False):
    if not player:
        player = Player.current()

    results = Intel.select().join(PlayerKnowledgeBook).where(PlayerKnowledgeBook.player == player)
    if not print_locations:
        results = results.where(Intel.type != IntelTypes.location)
    detailed = []
    for intel in results:
        detailed.append(intel.detail())
    print("intel:")
    print_indented(detailed)


def print_player_belongings(player: Player=None):
    if not player:
        player = Player.current()

    results = Item.select().where(Item.belongs_to_player == player)
    print("items:")
    print_indented(results)


def print_player_places(player: Player=None):
    if not player:
        player = Player.current()

    results = ["current: " + str(player.place), "next: " + str(player.next_location)]
    print("places:")
    print_indented(results)


def print_npc_intel(npc: NPC, debug=False):
    if debug or Params.debug_mode:
        results = Intel.select().join(NPCKnowledgeBook).where(NPCKnowledgeBook.npc == npc)
        print("intel:")
        print_indented(results)


def print_npc_belongings(npc: NPC, debug=False):
    if debug or Params.debug_mode:
        results = Item.select().where(Item.belongs_to == npc)
        print("items:")
        print_indented(results)


def print_npc_place(npc: NPC, debug=False):
    if debug or Params.debug_mode:
        results = [npc.place]
        print("place_location:")
        print_indented(results)
