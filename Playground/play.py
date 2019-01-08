from Playground.info import print_player_intel, print_player_belongings, print_player_places, \
    print_npc_intel, print_npc_belongings, print_npc_place
from Playground.progress import Progress
from Playground.helper import query_yes_no, ga_quest_generator

from Data.statics import Playground
from Grammar.actions import Terminals as T, NonTerminals as NT
from Grammar.plot import export_semantics_plot
from Grammar.rules import rules

from World.Narrative.actions import terminals
from World.Narrative.effects import is_done_method
from World.Types.Intel import Intel
from World.Types.Item import Item
from World.Types.Person import NPC, NPCDead, Player
from World.Types.Place import Place
from World.Types.Log import Message

import cmd


class Play(cmd.Cmd):
    intro = 'Welcome to the game. Type help or ? to list commands.\n'
    prompt = '(Player) '
    error_invalid = '*** Invalid command:'
    progress: Progress = None
    last_action = T.null
    last_args = []
    last_action_doable = False
    quest_in_progress = False
    quest_done = False

    def start_quest(self, quest):
        print("Starting a quest from:", quest.action)
        self.quest_in_progress = True
        self.quest_done = False
        self.last_action = T.null
        self.last_args = []
        self.last_action_doable = False
        quest.set_indices()
        self.progress = Progress(quest=quest)
        self.progress.check_action_proceed(self.last_action, self.last_args)
        self.progress.print_progress()
        Message.print_queue(debug_mode=Playground.debug_mode)
        export_semantics_plot(quest, semantics_indices=self.progress.semantics_indices,
                              current_level_index=self.progress.current_node.index)

    def finish_quest(self):
        print("WOW quest completed!!!!")
        self.progress.current_node = self.progress.quest
        self.quest_in_progress = False
        self.quest_done = True
        Intel.delete_all_arbitrary()
        query = Item.delete().where(Item.name.contains('arbitrary'))
        query.execute()
        query = Place.delete().where(Place.name.contains('arbitrary'))
        query.execute()
        query = NPC.delete().where(NPC.name.contains('arbitrary'))
        query.execute()

    # ----- basic player commands -----
    def do_talk(self, args):
        """Talk to an NPC. TALK goblin (starts a quest if possible)"""
        args = parse(args)
        if not self.check_length(args, 1):
            return
        npc = NPC.get_or_none(NPC.name == args[0])

        found = terminals.talk(npc=npc)
        if not found:
            print("failed!")
            return

        if self.quest_in_progress:
            print("talk and talk and talk ..!")
        else:
            motive, nt = npc.top_motive()

            if nt == T.null:
                print("not motivated, let's talk and talk ..!")
                return

            # find quest rule number based on motive type
            quest_rule_number = None
            for rule_number, set_of_actions in rules[NT.quest].items():
                if len(set_of_actions) and set_of_actions[0] == nt:
                    quest_rule_number = rule_number
                    break

            quest = ga_quest_generator(quest_rule_number)
            if quest:
                if query_yes_no("Do you want to play quest '%s'" % quest.genre()):
                    motive.delete_instance()
                    self.start_quest(quest)
                else:
                    print("Quest", quest.genre(), "refused to be played! Maybe later, huh?")
            else:
                print('quest not found!')
                print('failed!')

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
        print("player's belongings updated.")
        print_player_belongings()
        print("NPC belongings updated.")
        print_npc_belongings(item_holder)
        self.last_action_doable = True

    def do_explore(self, args):
        """Explore current location to find an NPC or Item. EXPLORE item potion | EXPLORE npc goblin"""
        args = parse(args)
        if not self.check_length(args, 2):
            return

        dest = Player.current().place
        if args[0] == 'item':
            item = Item.get_or_none(Item.name == args[1])
            if not self.set_inputs(action=T.explore, args=[dest, '', item]):
                return
            found = terminals.explore(area_location=dest, item=item)
        else:
            npc = NPC.get_or_none(NPC.name == args[1])

            if not self.set_inputs(action=T.explore, args=[dest, npc, '']):
                return
            found = terminals.explore(area_location=dest, npc=npc)

        if not found:
            print("failed!")
            return

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
        print("player's belongings updated.")
        print_player_belongings()
        self.last_action_doable = True

    def do_give(self, args):
        """Give an NPC something. GIVE bandage Goblin"""
        args = parse(args)
        if not self.check_length(args, 2):
            return

        item = Item.get_or_none(Item.name == args[0])
        npc = NPC.get_or_none(NPC.name == args[1])

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

        self.last_action_doable = True

    def do_take(self, args):
        """Take something from an NPC. TAKE bandage Goblin"""
        args = parse(args)
        if not self.check_length(args, 2):
            return

        item = Item.get_or_none(Item.name == args[0])
        npc = NPC.get_or_none(NPC.name == args[1])
        dead = NPCDead.get_or_none(NPCDead.name == args[1])

        if not npc and dead:
            # npc is dead, loot him
            if not self.set_inputs(action=T.take, args=[item]):
                return
            found = terminals.take_loot(item_to_take=item, loot_npc=dead)
        else:
            # npc is alive, or not found among dead, can't loot
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
        """Read a piece of intel from a book (intel: type intel_value). READ location goblin_place address_book"""
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

        self.last_action_doable = True

    def do_damage(self, args):
        """Damage an NPC. Damage Goblin"""
        args = parse(args)
        if not self.check_length(args, 1):
            return

        npc = NPC.get_or_none(NPC.name == args[0])

        if not self.set_inputs(action=T.damage, args=[npc]):
            return

        found = terminals.damage(target=npc)
        if not found:
            print("failed!")
            return

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
        print("NPC health meter:", npc.health_meter)
        self.last_action_doable = True

    # ---- listing information commands ----
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
            print_npc_intel(npc, debug=True)
        elif cat == "items" or cat == "item" or cat == "belongings" or cat == "belonging":
            print_npc_belongings(npc, debug=True)
        elif cat == "places" or cat == "place_location" or cat == "locations" or cat == "location":
            print_npc_place(npc, debug=True)
        else:
            print_npc_intel(npc, debug=True)
            print_npc_belongings(npc, debug=True)
            print_npc_place(npc, debug=True)

    def do_progress(self, args):
        """Print Progress status, PROGRESS"""
        args = parse(args)
        if not self.check_length(args, 0):
            return

        self.progress.print_progress(full=True)

    # ----- helper methods -----
    def set_inputs(self, action: T, args: list) -> bool:
        if None in args:
            print("Error: Typo in one of the inputs")
            return False
        if action in [T.goto, T.explore] or \
                (self.progress and
                 action == self.progress.current_node.action and args == self.progress.get_current_semantics()):
            # action is among sanctioned actions or it is the next action with correct arguments
            pass
        else:
            print("Error: Action is not allowed at the moment")
            return False
        for i, value in enumerate(args):
            if value == '':
                args[i] = None

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
        if self.quest_in_progress:

            if self.last_action_doable:
                self.last_action_doable = False
                level_completed = False

                for i in range(Playground.max_level_skip_loop):
                    level_completed = self.progress.check_action_proceed(self.last_action, self.last_args)
                    # next step updated

                    if level_completed:
                        # check if next step is already done before (check world's effects)
                        level_already_done = is_done_method(self.progress.current_node)(*self.progress.get_current_semantics())
                        if level_already_done:
                            self.last_action = self.progress.current_node.action
                            self.last_args = self.progress.get_current_semantics()
                        else:
                            break

                self.progress.print_progress()

                # check if quest is completed
                if level_completed and 0 in self.progress.completed_indices:
                    self.finish_quest()

            export_semantics_plot(self.progress.quest, semantics_indices=self.progress.semantics_indices,
                                  current_level_index=self.progress.current_node.index)

        Message.print_queue(debug_mode=Playground.debug_mode)


def parse(arg):
    return tuple(map(str, arg.split()))


if __name__ == '__main__':
    Play().cmdloop()
