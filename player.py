"""
Player class for the Ashen Depths game.

1. Shield - is_shielded is a boolean. It absorbs ONE incoming hit fully, no matter the amount of damage.
2. take_damage() reports the OUTCOME (blocked vs took-n damage) and returns it as a string.
3. Inventory is a flat list with duplicates allowed. Lookup returns the first item found.

"""


class Player:
    def __init__(self, name, health, current_room=None, inventory=None):
        self.name = name
        self.health = health
        self.max_health = health  # Full health is just the starting health
        self.current_room = current_room
        # 'inventory=None' -> fresh []
        # The starting Dagger is created in create_world() and added via add_item()
        self.inventory = inventory if inventory is not None else []
        self.is_shielded = False

    def take_damage(self, amount):
        # Shield spends itself here, at moment of impact.
        if self.is_shielded:
            self.is_shielded = False
            return "Your shield absorbs the blow!"
        self.health = max(0, self.health - amount)
        return f"You take {amount} damage. (HP: {self.health}/{self.max_health})"
