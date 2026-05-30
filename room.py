"""
The Room class for the Ashen Depths game.

Room holds enemies, items, and exits.

"""


class Room:
    def __init__(self, name, description, enemies=None, items=None, exits=None):
        self.name = name
        self.description = description
        # =None, creates a fresh container. Room is created empty and populated later
        self.enemies = enemies if enemies is not None else []
        self.items = items if items is not None else []
        self.exits = exits if exits is not None else []

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def has_enemy(self, enemy_name):
        # Checking if room has an enemy. No targeting code lies here.
        return any(e.name.lower() == enemy_name.lower() for e in self.enemies)

    def add_item(self, item):
        # Where dropped items land and where placed items live
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_available_exits(self):
        # Returns directions "where can you go"
        # Rooms.py lists the options, game.py does the traveling
        return list(self.exits.keys())

    def display(self):
        lines = [f"== {self.name} ==", self.description]

        if self.enemies:
            lines.append("\nEnemies here:")
            # Enemies get numbered
            for i, enemy in enumerate(self.enemies, start=1):
                lines.append(f" {i}. {enemy.display()}")

        if self.items:
            lines.append("\nItems here:")
            for item in self.items:
                lines.append(f" - {item.display()}")

        exits = self.get_available_exits()
        if exits:
            lines.append(f"\nExits: {', '.join(exits)}")

        return "\n".join(lines)
