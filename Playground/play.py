from Playground.info import print_indented, print_player_intel, print_player_belongings, print_player_places, \
    print_npc_intel, print_npc_belongings, print_npc_place

from World.Narrative.actions import terminals
from World.Types.BridgeModels import PlayerKnowledgeBook
from World.Types.Intel import Intel
from World.Types.Item import Item
from World.Types.Person import NPC, Player
from World.Types.Place import Place

import cmd


class Play(cmd.Cmd):
    intro = 'Welcome to the game. Type help or ? to list commands.\n'
    prompt = '(Player) '
    error_invalid = '*** Invalid command:'

    # ----- basic player commands -----
    def do_exchange(self, args):
        """Exchange an Item with another with an NPC. EXCHANGE goblin potion bandage
        <means give potion to goblin and take bandage from him>"""
        args = parse(args)
        if not self.check_length(args, 3):
            return

        terminals.exchange(
            item_holder=NPC.get(NPC.name == args[0]),
            item_to_give=Item.get(Item.name == args[1]),
            item_to_take=Item.get(Item.name == args[2]))

    def do_explore(self, args):
        """Move player to a named position. EXPLORE Rivervale"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        found = terminals.explore(area_location=Place.get(Place.name == args[0]))
        if not found:
            print("failed!")
            return
        print("moved to:", Player.get().place)

    def do_gather(self, args):
        """Gather an item. GATHER bandage"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        found = terminals.gather(item_to_gather=Item.get(Item.name == args[0]))
        if not found:
            print("failed!")
            return
        print("Item added to belongings.")
        print_player_belongings()

    def do_goto(self, args):
        """Move player to a named position. GOTO Rivervale"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        found = terminals.goto(destination=Place.get(Place.name == args[0]))
        if not found:
            print("failed!")
            return
        print("moved to:", Player.get().place)

    def do_give(self, args):
        """Give an NPC something. GIVE Goblin bandage"""
        args = parse(args)
        if not self.check_length(args, 2):
            return

        npc = NPC.get(NPC.name == args[0])
        found = terminals.give(item=Item.get(Item.name == args[1]), receiver=npc)
        if not found:
            print("failed!")
            return
        print("player's belongings updated.")
        print_player_belongings()
        print("NPC belongings updated.")
        print_npc_belongings(npc)

    def do_spy(self, args):
        """Spy on an NPC to gather some information (intel: type intel_value). SPY Goblin place lempeck_place"""
        args = parse(args)
        if not self.check_length(args, 3):
            return

        found = terminals.spy(spy_on=NPC.get(NPC.name == args[0]), intel_target=Intel.find_by_name(args[1], [args[2]]))
        if not found:
            print("failed!")
            return
        print("Player intel updated.")
        print_player_intel()

    def do_stealth(self, args):
        """Stealth on an NPC. STEALTH Goblin"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        found = terminals.stealth(target=NPC.get(NPC.name == args[0]))
        if not found:
            print("failed!")
            return
        print("stealth done!")

    def do_player(self, args):
        """Print player's info (type player <category>). PLAYER intel"""
        args = parse(args)
        player = Player.get()

        if args:
            cat = args[0].lower()
        else:
            cat = None

        if cat == "intel":
            print_player_intel(player)
        elif cat == "items" or cat == "item" or cat == "belongings" or cat == "belonging":
            print_player_belongings(player)
        elif cat == "places" or cat == "place" or cat == "locations" or cat == "location":
            print_player_places(player)
        else:
            print_player_intel(player)
            print_player_belongings(player)
            print_player_places(player)

    def do_npc(self, args):
        """Print NPC's info (type npc <category). NPC Goblin intel"""
        args = parse(args)
        if not args:
            # less than 1 arg
            self.check_length(args, 1)
            return
        else:
            npc_name = args[0]
        if len(args) == 1:
            cat = None
        elif len(args) == 2:
            cat = args[1]
        else:
            # more than 2 args
            self.check_length(args, 2)
            return
        npc = NPC.get(NPC.name == npc_name)

        if cat == "intel":
            print_npc_intel(npc)
        elif cat == "items" or cat == "item" or cat == "belongings" or cat == "belonging":
            print_npc_belongings(npc)
        elif cat == "places" or cat == "place" or cat == "locations" or cat == "location":
            print_npc_place(npc)
        else:
            print_npc_intel(npc)
            print_npc_belongings(npc)
            print_npc_place(npc)

    def check_length(self, args: tuple, desired: int) -> bool:
        if len(args) != desired:
            print(self.error_invalid, "Number of arguments should be exactly", desired, ", not", len(args))
            return False
        return True


def parse(arg):
    return tuple(map(str, arg.split()))


if __name__ == '__main__':
    Play().cmdloop()