"""
The Game class for Ashen Depths

A turn is 2 phases. Player acts, then room retaliates

Actions that provoke a retaliation (attack and use item). Move and check inventory are free and don't initiate a retaliation.

"""

from re import L

from enemy import Enemy
from item import Item
from player import Player
from room import Room


class Game:
    def __init__(self):
        self.player = None
        self.rooms = {}
        self.running = False

    # =====================================================
    #       Build Empty Rooms and exits
    # =====================================================

    def create_world(self):
        self.rooms["room_1"] = Room(
            "Starting Chamber",
            "You stand in a quiet chamber. Dust covers the floor.",
        )
        self.rooms["room_2"] = Room(
            "Goblin Den",
            "The stench of Goblins fills the air. You hear chittering.",
        )
        self.rooms["room_3"] = Room(
            "Orc Hall",
            "A massive hall with stone pillars. Orc war paint covers the walls.",
        )
        self.rooms["room_4"] = Room(
            "Dragon's Lair",
            "A cavernous chamber. Gold coins litter the floor. ",
            "A massive dragon sleeps before you.",
        )

        # Create exits, now that rooms exist. Bidirectional pairs: build return directions also
        r1, r2, r3, r4 = (self.rooms["room_1"], self.rooms["room_2"], self.rooms["room_3"], self.rooms["room_4"])
        r1.exits["north"] = r2
        r2.exits["south"] = r1
        r2.exits["north"] = r3
        r3.exits["south"] = r2
        r3.exits["north"] = r4
        r4.exits["south"] = r3



    def place_items_and_enemies(self):
        r1, r2, r3, r4 = (self.rooms["room_1"], self.rooms["room_2"], self.rooms["room_3"], self.rooms["room_4"])

        # Player with starting dagger
        self.player = Player("Hero", 100, current_room=r1)
        self.player.add_item(Item("Dagger", "damage", effect_value=10)) # inf uses

        # Room 2 - Goblin Den
        r2.add_item(Item("Healing Potion", "heal", effect_value=30, uses_left=1))
        r2.add_item(Item("Magic Scroll", "disable", effect_value=1, uses_left=3))
        r2.add_enemy(Enemy("Goblin", 20, 5, loot=[Item("Healing Potion", "heal", 30, 1)]))
        r2.add_enemy(Enemy("Goblin", 20, 5, loot=[Item("Healing Potion", "heal", 30, 1)]))

        # Room 3- Orc Hall
        r3.add_item(Item("Shield Charm", "shield", effect_value=1, uses_left=1))
        r3.add_item(Item("Poison Vial", "disable", effect_value=1, uses_left=1))
        r3.add_item(Item("Fireball Scroll", "damage", effect_value=20, uses_left=1))
        r3.add_enemy(Enemy("Orc", 40, 8, loot=[Item("Shield Charm", "shield", 1, 1)]))

        # Room 4 - Dragon Lair - Dragon drops nothing. The Amulet is a placed floor item. Win by holding the Amulet
        r4.add_enemy(Enemy("Dragon", 100, 15, loot=[]))
        r4.add_item(Item("Amulet", "special"))



        # ============================================
        #           Main Loop
        # ============================================


    def run(self):
        self.create_world()
        self.place_items_and_enemies()
        self.running = True
        print("=" * 55)
        print(" Ashen Depths - Find the Amulet, escape the dungeon.")
        print("=" * 55)


        while self.running:
            # Display info
            print("\n" + self.player.current_room.display())
            print("\n" + self.player.display_stats())


            # Get Action
            action  = self.get_player_action()

            # Action Phase
            spent_turn = self.process_action(action)

            # Check if win or lose
            if self.check_win():
                self.end_game("WIN")
                break
            if self.check_lose():
                self.end_game("LOSE")
                break

            # Retaliation phase - only if action 2 was a turn
            if spent_turn:
                self.room_retaliation()

            # After retaliation...did it kill you?
            if self.check_win():
                self.end_game("WIN")
                break
            if self.check_lose():
                self.end_game("LOSE")
                break


    # ==================================================
    #               INPUT
    # ==================================================


    def get_player_action(self):
        # Returns a (verb, argument) tuple. Re-prompts until the verb is known
        while True:
            raw = input(
                "\nWhat do you do? "
                "[attack / use <item> / move <dir> / inventory / quit] > "
            ).strip().lower()

        if not raw:
            print("Say something")
            continue

        parts = raw.split(maxsplit=1)
        verb = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        if verb in ("attack", "inventory", "quit", "use", "move"):
            return (verb, arg)
        print(f"I don't understand '{verb}'.")




    # ===========================================
    #       ACTIONS
    # ===========================================


    def process_action(self, action):
        verb, arg = action

        if verb == "attack":
            return self.resolve_attack()        # provokes

        if verb == "use":
            return self.resolve_use_item(arg)

        if verb == "move":
            self.resolve_move(arg)

        if verb == "inventory":
            print("\n" + self.player.check_inventory")
            return False

        if verb == "quit":
            self.running = False
            print("You lay down your weapon and leave the dungeon.")
            return False

        return False


    # ==========================================
    #           Targeting
    # ==========================================


    def resolve_target(self, room):
        # Returns an enemy object, or None (which means no action happened)
        enemies = room.enemies

        if len(enemies) == 0:
            print("There's nothing here to attack.")
            return None

        if len(enemies) == 1:
            return enemies[0]               # Auto-target enemy if there is only one in the room


        # If 2+ enemies, we need to make a choice
        while True:
            print("\nWhich enemy?")
            for i, enemy in enumerate(enemies, start=1):
                print(f" {i}. {enemy.display()}")
            choice = input(" Pick a number (or 'back' to cancel) > ").strip.lower()

            if choice in ("back", "0"):
                return None             # abort - no turn spent

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(enemies):
                    return enemies[idx]
            print(" Invalid choice.")


    # ==================================================
    #           Action phase - attack and item use
    # ==================================================


    def resolve_attack(self):
        room = self.player.current_room
        target = self.resolve_target(room)
        if target is None:
            return False            # Nothing happened, no turn spent

        damage = 10
        target.take_damage(damage)
        print(f"\nYou strike {target.name} for {damage} damage! "
              f"({target.name}: {target.health}/{target.max_health} HP)")

        self.handle_possible_death(target, room):
        return True                     # A turn was spent, provoke

    def resolve_use_item(self, item_name):
        if not item_name:
            print("Use what? Try 'use healing potion'.")
            return False

        room = self.player.current_room
        item = self.player._find_item(item_name)

        target = None
        if item is not None and item.item_type in ("damage", "disable"):
            target = self.resolve_target(room)
            if target is None:
                return False            # no target -- cancelled

        message, did_act = self.player.use_item(item_name, target=target)
        print("\n" + message)

        if not did_act:
            return False        # Typo / Amulet / spent free item

        if target is not None:
            self.handle_possible_death(target, room)

        return True


    def handle_possible_death(self, enemy, room):
        if not enemy.is_alive():
            print(f"{enemy.name} collapses!")
            for loot_item in enemy.drop_loot():
                room.add_item(loot_item)
                print(f" {enemy.name} dropped: {loot_item.name}")
            room.remove_enemy(enemy)


    def resolve_move(self, direction):
        room = self.player.current_room
        if direction is None:
            print("Move where? Try 'move north'.")
            return
        if direction in room.exits:
            self.player.move_to_room(room.exits[direction])
            # Auto pickup any floor items in new room
            self.auto_pickup(self.player.current_room)
        else:
            print(f"You can't go {direction} from here.")


    def auto_pickup(self, room):
        # Items found in rooms are auto picked up. Iterate over a copy since we mutate room
        for item in list(room.items):
            self.player.add_item(item)
            room.remove_item(item)
            print(f"You pick up: {item.name}")



    # =============================================
    #       RETALIATION PHASE
    # =============================================


    def room_retaliation(self):
        room = self.player.current_room
        for enemy in list(room.enemies):
            if not self.player.is_alive():
                break
            attempt = enemy.attack(self.player)
            print("\n" + attempt)



    # =============================================
    #          WIN / LOSE / END
    # =============================================


    def check_win(self):
        # WIN = player holds the Amulet
        return any(i.name == "Amulet" for i in self.player.inventory)

    def check_lose(self):
        return not self.player.is_alive()

    def end_game(self, reason):
        self.running = False
        print("\n" + "=" * 55)
        if reason == "WIN":
            print(" You raise the Amulet high. The dungeon trembles -")
            print(" and you walk out alive. VICTORY.")
        else:
            print(" Your vision fades. The dungeon keeps its secrets.")
            print(" GAME OVER.")
        print("=" * 55)


    if __name__ == "__main__":
        Game().run()
