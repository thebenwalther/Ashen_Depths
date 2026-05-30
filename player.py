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

    def heal(self, amount):
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - before

    def is_alive(self):
        return self.health > 0

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item_name):
        # Remove first item matching the name
        item = self._find_item(item_name)
        if item is not None:
            self.inventory.remove(item)
        return item

    def _find_item(self, item_name):
        # First name match. Case-sensitive
        for item in self.inventory:
            if item_name.lower() == item_name.lower():
                return item
        return None

    def check_inventory(self):
        if not self.inventory:
            return "Your inventory is empty."
        lines = ["Inventory:"] + [f" - {item.display()}" for item in self.inventory]
        return "\n".join(lines)

    def use_item(self, item_name, target=None):
        item = self._find_item(item_name)
        if item is None:
            return (f"You don't have an {item_name}.", False)

        if not item.is_usable():
            # Catch the Amulet "special" case
            if item.item_type == "special":
                return (
                    f"The {item.name} hums with power, but there's nothing to use it on.",
                    False,
                )
            return (f"The {item.name} is used up.", False)

        if item.item_type in ("damage", "disable") and target is None:
            return (f"There's nothing to use the {item.name} on.", False)

        if item.item_type == "damage":
            target.take_damage(item.effect_value)
            message = f"You strike {target.name} with {item.name} for {item.effect_value} damage!"

        elif item.item_type == "disable":
            target.skip_next_turn = True
            message = f"You use {item.name} - {target.name} will skip its next turn!"

        elif item.item_type == "heal":
            healed = self.heal(item.effect_value)
            message = f"You use {item.name} and recover {healed} HP."

        elif item.item_type == "shield":
            self.is_shielded = True
            message = f"You raise the {item.name}. The next attack with be blocked."

        else:
            return (f"You can't use the {item.name}", False)

        item.consume()
        if not item.is_usable():
            self.inventory.remove(item)

        return (message, True)

    def move_to_room(self, room):
        self.current_room = room

    def display_stats(self):
        location = self.current_room.name if self.current_room else "Unknown"
        shield = " [Shielded]" if self.is_shielded else ""
        return f"{self.name} - HP: {self.health}/{self.max_health} - {location}{shield}"
