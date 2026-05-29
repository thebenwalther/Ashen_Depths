"""
The Enemy class represents an enemy character in the game.

1. An enemy drops exactly what it carries, every time.
2. Items are born once in create_world() and handed to the enemy.
3. drop_loot() always returns a list. [] when nothing drops (not None or a bare item.)
4. Two identical Goblins are told apart by their POSITION in the room's enemy list.
"""


class Enemy:
    def __init__(self, name, health, attack_damage, loot=None):
        self.name = name
        self.health = health
        self.max_health = health  # Max health is just the starting health
        self.attack_damage = attack_damage  # Fixed amount per enemy
        self.skip_next_turn = False  # set True by a disable item

        # Carried loot. 'loot = None' default (not loot=[])
        # every enemy gets it own list, not one list shared by all enemies
        self.loot = loot if loot is not None else []

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def attack(self, target):
        # Returns a message string for the Game to print

        if self.skip_next_turn:
            # Consume the stun at the moment of attack then clear it so we aren't skipping forever.
            self.skip_next_turn = False
            return f"{self.name} is stunned and skips its turn!"

        # Hand over the damage computation to the player.
        player.take_damage(self.attack_damage)
        return f"{self.name} attacks you for [self.attack_damage} damage!"

    def is_alive(self):
        return self.health > 0

    def drop_loot(self):
        # Hand back what loot the enemy is holding.
        # The corpse gets removed from the room when the enemy dies and is discarded.
        return self.loot

    def display(self):
        # Returns a string so the room/Game can control the layout
        return f"{self.name} ({self.health}/{self.max_health} HP)"
