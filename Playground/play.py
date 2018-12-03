from Playground.info import print_player_intel, print_player_belongings, print_player_places, \
    print_npc_intel, print_npc_belongings, print_npc_place
from Playground.progress import Progress

from Data import quests
from Data.statics import Playground
from Grammar.actions import Terminals as T

from World.Narrative.actions import terminals
from World.Narrative.effects import is_done_method
from World.Types.Intel import Intel
from World.Types.Item import Item
from World.Types.Person import NPC, Player
from World.Types.Place import Place

import cmd


class Play(cmd.Cmd):
    intro = 'Welcome to the game. Type help or ? to list commands.\n'
    prompt = '(Player) '
    error_invalid = '*** Invalid command:'
    progress: Progress = None
    last_action = T.null
    last_args = []
    last_action_doable = False
    quest_done = False

    def __init__(self, quest=None):
        super(Play, self).__init__()
        # very beginning
        self.quest_done = False

        if not quest:
            quest = quests.cure
        self.progress = Progress(quest=quest)

        self.progress.check_action_proceed(self.last_action, self.last_args)
        self.progress.print_progress()

    # ----- basic player commands -----
    def do_exchange(self, args):
        """Exchange an Item with another with an NPC. EXCHANGE goblin potion bandage
        <means give potion to goblin and take bandage from him>"""
        args = parse(args)
        if not self.check_length(args, 3):
            return

        item_holder = NPC.get_or_none(NPC.name == args[0])
        item_to_give = Item.get_or_none(Item.name == args[1])
        item_to_take = Item.get_or_none(Item.name == args[2])

        if not self.set_inputs(action=T.exchange, args=[item_holder, item_to_give, item_to_take]):
            return

        found = terminals.exchange(
            item_holder=item_holder,
            item_to_give=item_to_give,
            item_to_take=item_to_take)
        if not found:
            print("failed!")
            return
        print("gave", item_to_give, ", took", item_to_take)
        print_player_belongings()
        self.last_action_doable = True

    def do_explore(self, args):
        """Move player to a named position. EXPLORE Rivervale"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        dest = Place.get_or_none(Place.name == args[0])

        if not self.set_inputs(action=T.explore, args=[dest]):
            return

        found = terminals.explore(area_location=dest)
        if not found:
            print("failed!")
            return
        print("moved to:", Player.current().place)
        self.last_action_doable = True

    def do_gather(self, args):
        """Gather an item. GATHER bandage"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        item = Item.get_or_none(Item.name == args[0])

        if not self.set_inputs(action=T.gather, args=[item]):
            return

        found = terminals.gather(item_to_gather=item)
        if not found:
            print("failed!")
            return
        print("Item added to belongings.")
        print_player_belongings()
        self.last_action_doable = True

    def do_give(self, args):
        """Give an NPC something. GIVE Goblin bandage"""
        args = parse(args)
        if not self.check_length(args, 2):
            return

        item = Item.get_or_none(Item.name == args[1])
        npc = NPC.get_or_none(NPC.name == args[0])

        if not self.set_inputs(action=T.give, args=[item, npc]):
            return

        found = terminals.give(item=item, receiver=npc)
        if not found:
            print("failed!")
            return
        print("player's belongings updated.")
        print_player_belongings()
        print("NPC belongings updated.")
        print_npc_belongings(npc)
        self.last_action_doable = True

    def do_spy(self, args):
        """Spy on an NPC to gather some information (intel: type intel_value). SPY Goblin place_location tomas_place"""
        args = parse(args)
        if not self.check_length(args, 3):
            return

        target = NPC.get_or_none(NPC.name == args[0])
        intel = Intel.find_by_name(args[1], [args[2]])

        if not self.set_inputs(action=T.spy, args=[target, intel]):
            return

        found = terminals.spy(spy_on=target, intel_target=intel)
        if not found:
            print("failed!")
            return
        print("Player intel updated.")
        print_player_intel()
        self.last_action_doable = True

    def do_stealth(self, args):
        """Stealth on an NPC. STEALTH Goblin"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        target = NPC.get_or_none(NPC.name == args[0])

        if not self.set_inputs(action=T.stealth, args=[target]):
            return

        found = terminals.stealth(target=target)
        if not found:
            print("failed!")
            return
        print("stealth done!")
        self.last_action_doable = True

    def do_take(self, args):
        """Take something from an NPC. TAKE Goblin bandage"""
        args = parse(args)
        if not self.check_length(args, 2):
            return

        item = Item.get_or_none(Item.name == args[1])
        npc = NPC.get_or_none(NPC.name == args[0])

        if not self.set_inputs(action=T.take, args=[item, npc]):
            return

        found = terminals.take(item_to_take=item, item_holder=npc)
        if not found:
            print("failed!")
            return
        print("player's belongings updated.")
        print_player_belongings()
        print("NPC belongings updated.")
        print_npc_belongings(npc)
        self.last_action_doable = True

    def do_read(self, args):
        """Read a piece of intel from a book (intel: type intel_value). READ place_location goblin_place address_book"""
        args = parse(args)
        if not self.check_length(args, 3):
            return

        intel = Intel.find_by_name(args[0], [args[1]])
        readable = Item.get_or_none(Item.name == args[2])

        if not self.set_inputs(action=T.read, args=[intel, readable]):
            return

        found = terminals.read(intel=intel, readable=readable)
        if not found:
            print("failed!")
            return
        print("Player intel updated.")
        print_player_intel()
        self.last_action_doable = True

    def do_goto(self, args):
        """Move player to a named position. GOTO Rivervale"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        dest = Place.get_or_none(Place.name == args[0])

        if not self.set_inputs(action=T.goto, args=[dest]):
            return

        found = terminals.goto(destination=dest)
        if not found:
            print("failed!")
            return
        print("moved to:", Player.current().place)
        self.last_action_doable = True

    def do_kill(self, args):
        """Kill an NPC. KILL Goblin"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        npc = NPC.get_or_none(NPC.name == args[0])

        if not self.set_inputs(action=T.kill, args=[npc]):
            return

        found = terminals.kill(target=npc)
        if not found:
            print("failed!")
            return
        print("target killed (health_meter set to " + str(npc.health_meter) + ")")
        self.last_action_doable = True

    def do_listen(self, args):
        """Listen a piece of intel from an NPC (intel: type intel_value). LISTEN spell needs_path Goblin"""
        args = parse(args)
        if not self.check_length(args, 3):
            return

        intel = Intel.find_by_name(args[0], [args[1]])
        npc = NPC.get_or_none(NPC.name == args[2])

        if not self.set_inputs(action=T.listen, args=[intel, npc]):
            return

        found = terminals.listen(intel=intel, informer=npc)
        if not found:
            print("failed!")
            return
        print("Player intel updated.")
        print_player_intel()
        self.last_action_doable = True

    def do_report(self, args):
        """Report a piece of intel to an NPC (intel: type intel_value). REPORT spell needs_path Steve"""
        args = parse(args)
        if not self.check_length(args, 3):
            return

        intel = Intel.find_by_name(args[0], [args[1]])
        npc = NPC.get_or_none(NPC.name == args[2])

        if not self.set_inputs(action=T.report, args=[intel, npc]):
            return

        found = terminals.report(intel=intel, target=npc)
        if not found:
            print("failed!")
            return
        print("NPC intel updated.")
        print_npc_intel(npc)
        self.last_action_doable = True

    def do_use(self, args):
        """Use an item (tool) on an NPC. USE potion Lempeck"""
        args = parse(args)
        if not self.check_length(args, 2):
            return

        item = Item.get_or_none(Item.name == args[0])
        npc = NPC.get_or_none(NPC.name == args[1])

        if not self.set_inputs(action=T.use, args=[item, npc]):
            return

        found = terminals.use(item_to_use=item, target=npc)
        if not found:
            print("failed!")
            return
        print("Item effect on the NPC,", item.impact_factor, "NPC health meter:", npc.health_meter)
        self.last_action_doable = True

    def do_player(self, args):
        """Print player's info (type player <category>). PLAYER intel"""
        args = parse(args)
        player = Player.current()

        if args:
            cat = args[0].lower()
        else:
            cat = None

        if cat == "intel":
            print_player_intel(player)
        elif cat == "items" or cat == "item" or cat == "belongings" or cat == "belonging":
            print_player_belongings(player)
        elif cat == "places" or cat == "place_location" or cat == "locations" or cat == "location":
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

        npc = NPC.get_or_none(NPC.name == npc_name)
        if not npc:
            print("Error: npc", npc_name, "not found")
            return

        if cat == "intel":
            print_npc_intel(npc)
        elif cat == "items" or cat == "item" or cat == "belongings" or cat == "belonging":
            print_npc_belongings(npc)
        elif cat == "places" or cat == "place_location" or cat == "locations" or cat == "location":
            print_npc_place(npc)
        else:
            print_npc_intel(npc)
            print_npc_belongings(npc)
            print_npc_place(npc)

    def do_progress(self, args):
        """Print Progress status, PROGRESS"""
        args = parse(args)
        if not self.check_length(args, 0):
            return

        self.progress.print_progress(full=True)

    def set_inputs(self, action: T, args: list) -> bool:
        if None in args:
            print("Error: Typo in one of the inputs")
            return False

        self.last_action = action
        self.last_args = args
        return True

    def check_length(self, args: tuple, desired: int) -> bool:
        if len(args) != desired:
            print(self.error_invalid, "Number of arguments should be exactly", desired, ", not", len(args))
            return False
        return True

    def postcmd(self, stop, line):
        # after loop

        if not self.quest_done and self.last_action_doable:
            self.last_action_doable = False

            level_completed = False

            for i in range(Playground.max_level_skip_loop):
                level_completed = self.progress.check_action_proceed(self.last_action, self.last_args)
                # next step updated

                if level_completed:
                    # check if next step is already done before (check world's effects)
                    level_already_done = is_done_method(self.progress.current_node)(*self.progress.get_current_semantics())
                    if level_already_done:
                        print("Already done, skip")
                        self.last_action = self.progress.current_node.action
                        self.last_args = self.progress.get_current_semantics()
                    else:
                        break

            # check if quest is completed
            if level_completed and 0 in self.progress.completed_indices:
                print("WOW quest completed!!!!")
                self.progress.current_node = self.progress.quest
                self.quest_done = True
        self.progress.print_progress()


def parse(arg):
    return tuple(map(str, arg.split()))


if __name__ == '__main__':
    Play().cmdloop()
