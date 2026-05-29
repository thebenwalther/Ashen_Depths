"""
The item class for Ashen Depths.

Design: It holds what an item is and tracks its own use count. The Game class switches on 'item_type' and nothing else. 'name' is display-only and
never drives logic.
"""


class Item:
    # Valid types for the Game:
    # "damage" -> hit a chosen enemy for effect_value (needs a target)
    # "disable" -> make a chosen enemy skip its next turn (needs a target)
    # "heal" -> restore effect_value health to the player (no target needed)
    # "shield" -> block the player's next incoming hit" (no target needed)
    # "special" -> the Amulet. No active use. You win by HOLDING it.

    def __init__(self, name, item_type, effect_value=0, uses_left=float("inf")):
        self.name = name
        self.item_type = item_type
        self.effect_value = (
            effect_value  # magnitude: damage dealt / health restored / turns skipped
        )
        self.uses_left = uses_left  # count remaining. inf == unlimited (the Dagger)

    def is_usable(self):
        # The Amulet is a special case: it is never "used" per se, but it's a win condition you carry, not an action.
        if self.item_type == "special":
            return False
        # inf > is True, so unlimited uses always return True and pass without a special case.
        return self.uses_left > 0

    def consume(self):
        # Spend one use. The Game class calls this when an item is used AFTER it has applied the effect.
        # Infinite items stay infinite for free: inf - 1 == inf.
        self.uses_left -= 1

    def display(self):
        # Returns a string instead of printing.
        # Show the use count only when it's finite; "5 uses left" on the Dagger, for example.
        # would be a lie, and "inf uses left" looks silly.
        if self.uses_left == float("inf"):
            return f"{self.name} ({self.item_type})"
        return f"{self.name} ({self.item_type}, {int(self.uses_left)} uses left)"
