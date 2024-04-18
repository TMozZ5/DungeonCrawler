import pygame
from random import randint, uniform
from math import dist
from sort import find_shortest_path


pygame.init()  # Initialise PyGame


class Tile:
    """Description - represents every tile and its properties"""

    class Vertex:
        """Represents the tiles vertex"""

        def __init__(self, x, y, adjacent_vertices):
            """
            :param x: x coord
            :type x: int
            :param y: y coord
            :type y: int
            :param adjacent_vertices: a dictionary of adjacent coordinates and the distance to them
            :type adjacent_vertices: dict
            """
            self.coords = (x, y)  # Vertexes coordinates
            self.g = 0  # Distance from start
            self.h = 0  # Heuristic (estimated) distance to end
            self.f = 0  # Total of g and h
            self.adjacent_vertices = adjacent_vertices  # The vertices adjacent to this one and the distance to them
            self.parent = None  # The parent of this vertex

        def calculate_values(self, end_vertex, total_distance=0, distance=0):
            """
            Calculates the g, h, and f values of the vertex
            :param end_vertex: the target vertex
            :type end_vertex: tuple
            :param total_distance: the total distance already travelled to get to the current vertex
            :type total_distance: float
            :param distance: the distance from the previous vertex to this one
            :type distance: float
            """
            self.g = distance + total_distance  # G cost is equal the distance from the previous vertex
            # plus the total distance already travelled
            x, y = self.coords  # Vertices x and y coords
            end_x, end_y = end_vertex  # End vertices x and y coordinates
            self.h = (x - end_x) + (y - end_y)  # H or heuristic cost is the estimated distance to the end vertex,
            # here it is calculated using its manhattan distance
            self.f = self.g + self.h  # F value is equal to the g cost plus the h cost

        def set_parent(self, parent):
            """
            Set a new parent for this vertex; this is used to trace the path taken from the start vertex to the end
            :param parent: the vertex that this one originated from
            :type parent: Vertex
            """
            self.parent = parent

    def __init__(self, block_path, floor_tile, empty, occupied, x, y, map_height, map_width):
        """
        :param block_path: determines if a tile blocks the players path
        :type block_path: bool
        :param floor_tile: checks if the tile belongs to another room
        :type floor_tile: bool
        :param empty: determines if a tile is empty
        :type empty: bool
        :param occupied: determines if a tile is occupied by something
        :type occupied: bool
        :param x: the tiles x coord
        :type x: int
        :param y: the tiles y coord
        :type y: int
        :param map_height: the map height
        :type map_height: int
        :param map_width: the map width
        :type map_width: int
        """
        self.block_path = block_path
        self.floor_tile = floor_tile
        self.empty = empty
        self.occupied = occupied
        self.object = None  # Aggregates the tile with objects that spawn on it
        adjacent_vertices = {}
        # The following if statements ensures that only adjacent vertices that are in the lists index
        # can be counted as adjacent
        if x > 0:
            adjacent_vertices.update({(x-1, y): 1})
        if x < map_width - 1:
            adjacent_vertices.update({(x+1, y): 1})
        if y > 0:
            adjacent_vertices.update({(x, y-1): 1})
        if y < map_height - 1:
            adjacent_vertices.update({(x, y+1): 1})
        self.vertex = self.Vertex(x, y, adjacent_vertices)


class Room:
    """holds the properties of each room"""

    def __init__(self, tiles, centre_x, centre_y):
        """
        :param tiles: all the tiles that the room occupies as tuples
        :type tiles: list
        :param centre_x: the centre x coord of the room
        :type centre_x: int
        :param centre_y: the centre y coord of the room
        :type centre_y: int
        """
        self.tiles = tiles
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.distance = centre_x + centre_y  # The rooms distance form the origin


class Camera:
    """Represents the players view of the map so that the screen moves with the player"""

    def __init__(self, width, height):
        """
        :param width: the pixel width of the screen
        :type width: int
        :param height: the pixel height of the screen
        :type height: int

        """
        self.__width = width
        self.__height = height
        self.__x = 0
        self.__y = 0

    def update(self, x, y, cell_width, cell_height):
        """
        :param x: new x coord
        :type x: int
        :param y: new y coord
        :type y: int
        :param cell_width: the width of a cell
        :type cell_width: int
        :param cell_height: the height of a cell
        :type cell_width: int
        """
        self.__x = x * cell_width + (cell_width // 2)
        self.__y = y * cell_height + (cell_height // 2)

    @property
    def rectangle(self):
        """
        Creates the rectangle that is the player view of the map
        :return: the position of the rectangle
        """
        rect_position = pygame.Rect((0, 0), (self.__width, self.__height))
        rect_position.center = (self.__x, self.__y)
        return rect_position


class Entity:
    """Represents any entity to exist on the map, e.g. player, loot chest, etc."""

    def __init__(self, x, y, sprite):
        """
        :param x: x coord
        :type x: int
        :param y: y coord
        :type y: int
        :param sprite: the entities sprite
        :type sprite: surface
        """
        self.x = x  # Map address not pixel address
        self.y = y  # Map address not pixel address
        self._sprite = sprite

    def draw(self, screen, cell_width, cell_height):
        """
        Draws the entity to the screen
        :param screen: the screen to be drawn to
        :type screen: surface
        :param cell_width: the map width
        :type cell_width: int
        :param cell_height: the map height
        :type cell_height: int
        """
        screen.blit(self._sprite, (self.x * cell_width, self.y * cell_height))  # Draw the sprite to the screen

    def remove_sprite(self, sprites, new_map, x=-1, y=-1):
        """
        Removes the sprite from the list of sprites to draw
        :param sprites: the list that the sprite is being removed from
        :type sprites: list
        :param new_map: the list of map tiles with their properties
        :type new_map: list
        :param x: the sprites x coordinate
        :type x: int
        :param y: the sprites y coordinate
        :type y: int
        :return: sprites, new_map
        """
        if x == -1:
            x = self.x
        if y == -1:
            y = self.y
        sprites.remove(self)
        new_map[x][y].occupied = False
        new_map[x][y].object = None
        return sprites, new_map


class Font(Entity):
    """Represents font to be drawn"""

    def __init__(self, x, y, font, colour, text):
        """
        :param font: the font style
        :type font: font
        :param colour: the colour of the font
        :type colour: tuple
        :param text: the text to be drawn
        :type text: str
        """
        super().__init__(x, y, None)
        self.__font = font
        self.__colour = colour
        self.__text = text

    def draw(self, screen, cell_width, cell_height):
        """Draw the font to the screen"""
        self._sprite = self.__font.render(self.__text, True, self.__colour)  # Set the sprite to the text
        screen.blit(self._sprite, (self.x * cell_width, self.y * cell_height))  # Draw it to the screen

    def set_text(self, text):
        """
        Set new text for the font
        :param text: the new text to be drawn
        :type text: str
        """
        self.__text = text


class Chest(Entity):
    """Represents loot chests"""

    def __init__(self, x, y, sprite, item):
        """
        :param item: the item that the chest will contain
        :type item: Item
        """
        super().__init__(x, y, sprite)
        self.item = item

    def remove_sprite(self, sprites, new_map, x=-1, y=-1):
        """
        Removes the sprite from the list of sprites to draw
        :param sprites: the list that the sprite is being removed from
        :type sprites: list
        :param new_map: the list of map tiles with their properties
        :type new_map: list
        :param x: the sprites x coordinate
        :type x: int
        :param y: the sprites y coordinate
        :type y: int
        :return: sprites, new_map, item
        """
        if x == -1:
            x = self.x
        if y == -1:
            y = self.y
        sprites.remove(self)
        new_map[x][y].occupied = True
        new_map[x][y].object = self.item
        item = self.item  # Also have to return the item from the chest
        return sprites, new_map, item


class Item(Entity):
    """Represents a loot item"""

    def __init__(self, x, y, sprite, name, value, min_value, max_value, font_x, font_y, font, colour):
        """
        :param name: the items name
        :type name: str
        :param font_x: the fonts x value
        :type font_x: int
        :param font_y: the fonts y value
        :type font_y: int
        :param font: the items font
        :type font: surface
        :param colour: the fonts colour
        :type colour: tuple
        """
        super().__init__(x, y, sprite)
        self.name = name
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._font = Font(font_x, font_y, font, colour, name)

    def generate_value(self):
        """Generate a new value for the item"""
        self._value = randint(self._min_value, self._max_value)

    def set_coords(self, x, y):
        """
        Set the x and y coords of the item
        :param x: the items x coord
        :type x: int
        :param y: the items y coord
        :type y: int
        """
        self.x = x
        self.y = y

    def draw_font(self, screen, cell_width, cell_height):
        """
        Draws the items font to the screen
        :param screen: screen tp be drawn to
        :type screen: surface
        :param cell_width: width of cells
        :type cell_width: int
        :param cell_height: height of cells
        :type cell_height: int
        """
        self._font.draw(screen, cell_width, cell_height)


class Weapon(Item):
    """Represents a weapon loot item"""

    def __init__(self, x, y, sprite, name, damage, min_damage, max_damage, font_x, font_y, font, colour):
        """
        :param damage: the amount of damage the weapon deals
        :type damage: int
        :param min_damage: the min damage the weapon can do
        :type min_damage: int
        :param max_damage: the max damage the weapon can do
        :type max_damage: int
        """
        super().__init__(x, y, sprite, name, damage, min_damage, max_damage, font_x, font_y, font, colour)

    def player_interaction(self, player):
        """Increases the players damage"""
        player.damage += self._value

    def remove_interaction(self, player):
        """Decreases the players damage back to what it originally was"""
        player.damage -= self._value


class HealthPotion(Item):
    """Represents a health potion loot item"""

    def __init__(self, x, y, sprite, name, health, min_health, max_health, font_x, font_y, font, colour):
        """
        :param health: the amount of health the potion will give back to the player
        :type health: int
        :param min_health: the min health a potion can give to the player
        :type min_health: int
        :param max_health: the max health a potion can give to the player
        :type max_health: int
        """
        super().__init__(x, y, sprite, name, health, min_health, max_health, font_x, font_y, font, colour)

    def player_interaction(self, player):
        """Increases the players health if it is below the limit and removes the potion from their inventory"""
        if player.health <= player.health_limit:
            player.health += self._value
            player.delete_item()


class DamagePotion(Item):
    """Represents a damage potion loot item"""

    def __init__(self, x, y, sprite, name, damage, min_damage, max_damage, font_x, font_y, font, colour):
        """
        :param damage: the amount of damage a potion can give to the player
        :type damage: int
        :param min_damage: the min damage a potion can give to the player
        :type min_damage: int
        :param max_damage: the max damage a potion can give to the player
        :type max_damage: int
        """
        super().__init__(x, y, sprite, name, damage, min_damage, max_damage, font_x, font_y, font, colour)

    def player_interaction(self, player):
        """Increases the players damage and removes the potion from the players inventory"""
        player.damage += self._value
        player.delete_item()


class LuckPotion(Item):
    """Represents a damage potion loot item"""

    def __init__(self, x, y, sprite, name, luck, min_luck, max_luck, font_x, font_y, font, colour):
        """
        :param luck: the amount of luck a potion can give to a player
        :type luck: float
        :param min_luck: the min luck a potion can give to a player
        :type min_luck: float
        :param max_luck: the max luck a potion can give to a player
        :type max_luck: float
        """
        super().__init__(x, y, sprite, name, luck, min_luck, max_luck, font_x, font_y, font, colour)

    def generate_value(self):
        """Generates a new value for the luck potion"""
        self._value = uniform(self._min_value, self._max_value)  # Uniform
        # used instead of randint since it handles floats

    def player_interaction(self, player):
        """Increases the players luck value and removes the potion from the players inventory"""
        player.luck += self._value
        player.delete_item()


class Being(Entity):
    """Represents any physical being such as the player or the enemy"""

    def __init__(self, x, y, health, damage, sprite_f, sprite_f_attack):
        """
        :param health: the health or hit points of the being
        :type health: int
        :param damage: the beings base damage
        :type damage: int
        :param sprite_f: the beings front sprite
        :type sprite_f: surface
        :param sprite_f_attack: the list of the beings front attack animations
        :type sprite_f_attack: list
        """
        super().__init__(x, y, sprite_f)
        self.health = health
        self.damage = damage
        self._attack = sprite_f_attack
        self.moving = True
        self._attack_count = 0
        self.direction = (self.x, self.y + 1)
        self.dead = False
        self.dead_timer = 0

    def move(self, new_map, x_change, y_change, sprite, attack):
        """
        Allows the being to change their current position
        :param new_map: the map of tiles with properties
        :type new_map: list
        :param x_change: the amount the being is trying to change their x value by
        :type x_change: int
        :param y_change: the amount the being is trying to change their y value by
        :type y_change: int
        :param sprite: the beings new sprite
        :type sprite: surface
        :param attack: the new list of the beings attacks
        :type attack: list
        """
        if not self.dead:
            self._sprite = sprite  # Change the beings sprite
            self._attack = attack  # Change the beings attack
            if new_map[self.x + x_change][self.y + y_change].block_path is False\
                    and new_map[self.x + x_change][self.y + y_change].occupied is False:
                # If the tile isn't a wall tile or occupied and the being isn't dead
                new_map[self.x][self.y].occupied = False
                new_map[self.x][self.y].object = None
                self.x += x_change  # Change the beings x coords
                self.y += y_change  # Change the beings y coords
                new_map[self.x][self.y].occupied = True
                new_map[self.x][self.y].object = self
            self.direction = (self.x + x_change, self.y + y_change)  # Change the tile that they are facing
        return new_map

    def _attack_animation(self, frames):
        """
        Displays beings attack animation frames
        :param frames: the number of frames each image of the animation will be shown
        :type frames: int
        """
        self._sprite = self._attack[self._attack_count//frames]
        self._attack_count += 1

    def set_direction(self):
        """Reset the beings direction"""
        self.direction = (self.x, self.y+1)

    def check_if_dead(self, sprite_dead, damage):
        """
        Checks if the being is dead
        :param sprite_dead: the beings dead sprite
        :type sprite_dead: surface
        :param damage: the amount of damage taken by the being
        :type damage: int
        """
        self.health -= damage
        if self.health <= 0:
            self._sprite = sprite_dead
            self.dead = True

    def attack_being(self, being, sprite_dead):
        """
        Allows a being to attack another being
        :param being: the being to be attacked
        :type being: Being
        :param sprite_dead: the dead sprite of the being to be attacked
        :type sprite_dead: surface
        :return being: the being object with their updates attributes
        """
        being.check_if_dead(sprite_dead, self.damage)
        return being

    def perform_attack_animation(self, sprite_frames):
        """
        Allows a being object to cycle through their attack animation
        :param sprite_frames: the amount of frames an image from the attack animation is shown on screen
        :type sprite_frames: int
        """
        if self._attack_count + 1 >= (len(self._attack) * sprite_frames):  # If the beings attack count is
            # above the limit that would cause an index error
            self._attack_count = 0  # Reset the attack count
            self.moving = True  # Allow them to move again
        else:  # If not
            self._attack_animation(sprite_frames)  # Allow the being to attack

    def check_dead_timer(self, extra_time, dead_timer):
        """
        Checks if the being should de-spawn or not
        :param extra_time: the extra time from the previous time
        :type extra_time: int
        :param dead_timer: the amount of time an enemy has to be dead before they de-spawn
        :type dead_timer: int
        :returns: True if the enemy should de-spawn and False if not
        """
        self.dead_timer += extra_time
        if self.dead_timer >= dead_timer:
            return True
        else:
            return False


class Player(Being):
    """Represents the player character"""

    class InventorySlot(Entity):
        """Represents the players inventory slots"""

        def __init__(self, x, y, sprite, number, font, colour):
            """
            :param x: the entities x coord
            :type x: int
            :param y: the entities y coord
            :type y: int
            :param sprite: the sprite for the inventory slot
            :type sprite: surface
            :param number: the number for this inventory slot
            :type number: int
            :param font: the font for the number
            :type font: surface
            :param colour: the colour of the font
            :type colour: tuple
            """
            super().__init__(x, y, sprite)
            self.item = None  # The item in this inventory slot
            self.__number = Font(x, y, font, colour, str(number+1))

        def update_item(self, item):
            """
            Update the item stored in this inventory slot
            :param item: the item to be stored
            :type item: Item
            :return: True if the item can be stored and false if not
            """
            if self.item is None:  # If there isn't an item in this slot
                self.item = item  # Update the item to this one
                self.item.x = self.x  # Set the items x and y coords to the inventory slots
                self.item.y = self.y
                return True
            else:  # Else
                return False

        def remove_item(self, player_direction, new_map, items):
            """
            Remove an item from the inventory slot
            :param player_direction: the tile the player is facing
            :type player_direction: tuple
            :param new_map: the list of map tiles with their properties
            :type new_map: list
            :param items: the list of items that the item is to be added to
            :type items: list
            :return: new_map, items
            """
            x, y = player_direction  # Players direction x and y coords
            if self.item is not None and new_map[x][y].occupied is False and new_map[x][y].block_path is False:
                # If there is an item in this inventory slot and the tile the player is facing
                # is not a floor tile or occupied
                item = self.item  # Set the item to be returned as this item
                item.x = x  # Set the item x and y to the players direction x and y coords
                item.y = y
                new_map[x][y].object = item  # Set the object on the tile to this item
                new_map[x][y].occupied = True  # Make the tile occupied
                items.append(item)  # Add the item to the list of items
                self.item = None  # Set this slots item to none
            return new_map, items

        def delete_item(self):
            """Deletes the current inventory item and it is not dropped on the floor"""
            self.item = None

        def draw(self, screen, cell_width, cell_height):
            """
            Draws the entity to the screen
            :param screen: the screen to be drawn to
            :type screen: surface
            :param cell_width: the map width
            :type cell_width: int
            :param cell_height: the map height
            :type cell_height: int
            """
            screen.blit(self._sprite, (self.x * cell_width, self.y * cell_height))  # Draw the sprite to the screen
            if self.item is not None:  # Only attempt to draw the item if it exists
                self.item.draw(screen, cell_width, cell_height)
            self.__number.draw(screen, cell_width, cell_height)  # Draw the number font to the screen

        def draw_item_font(self, screen, cell_width, cell_height):
            """Draws the items font to the screen"""
            if self.item is not None:
                self.item.draw_font(screen, cell_width, cell_height)

    def __init__(self, x, y, health, damage, sprite_f, sprite_f_attack, inventory_size, inventory_sprite,
                 full_heart, font, colour, health_limit):
        """
        :param inventory_size: the players inventory size
        :type inventory_size: int
        :param inventory_sprite: the sprite for the player inventory slots
        :type inventory_sprite: surface
        :param full_heart: the sprite for a full heart of the players health
        :type full_heart: surface
        :param font: the font to be used for the inventory slots numbers
        :type font: surface
        :param colour: the colour for the font to be used for the inventory slots numbers
        :type colour: tuple
        :param health_limit: the maximum amount of health that the player can have at any time
        :type health_limit: int
        """
        super().__init__(x, y, health, damage, sprite_f, sprite_f_attack)
        self.moved_again = False
        self.__inventory = [self.InventorySlot(num, 1, inventory_sprite, num, font, colour)
                            for num in range(0, inventory_size)]
        self.__current_slot = 0
        self.__full_heart = full_heart
        self.__hearts = [Entity(num, 2, self.__full_heart) for num in range(0, self.health)]
        self.luck = 0.0
        self.health_limit = health_limit

    def move(self, new_map, x_change, y_change, sprite, attack):
        """
        Allows the being to change their current position
        :param new_map: the map of tiles with properties
        :type new_map: list
        :param x_change: the amount the being is trying to change their x value by
        :type x_change: int
        :param y_change: the amount the being is trying to change their y value by
        :type y_change: int
        :param sprite: the beings new sprite
        :type sprite: surface
        :param attack: the new list of the beings attacks
        :type attack: list
        """
        self._sprite = sprite  # Change the beings sprite
        self._attack = attack  # Change the beings attack
        if new_map[self.x + x_change][self.y + y_change].block_path is False\
                and new_map[self.x + x_change][self.y + y_change].occupied is False:
            # If the tile isn't a wall tile or occupied
            new_map[self.x][self.y].occupied = False
            new_map[self.x][self.y].object = None
            self.x += x_change  # Change the beings x coords
            self.y += y_change  # Change the beings y coords
            new_map[self.x][self.y].occupied = True
            new_map[self.x][self.y].object = self
            self.moved_again = True  # Update weather or not the player has moved
        self.direction = (self.x + x_change, self.y + y_change)  # Change the tile that they are facing
        return new_map

    def draw_display(self, screen, cell_width, cell_height):
        """
        Draws the entity to the screen
        :param screen: the screen to be drawn to
        :type screen: surface
        :param cell_width: the map width
        :type cell_width: int
        :param cell_height: the map height
        :type cell_height: int
        """
        for slot in self.__inventory:
            slot.draw(screen, cell_width, cell_height)
        self.__inventory[self.__current_slot].draw_item_font(screen, cell_width, cell_height)
        for heart in self.__hearts:
            heart.draw(screen, cell_width, cell_height)

    def update_current_slot(self, number):
        """
        Updates the currently selected inventory slot
        :param number: the new inventory slot number
        :type number: int
        """
        self.__remove_interaction()
        self.__current_slot = number

    def __remove_interaction(self):
        """Removes the interaction with a weapon in the players inventory"""
        if type(self.__inventory[self.__current_slot].item) == Weapon:
            self.__inventory[self.__current_slot].item.remove_interaction(self)

    def perform_weapon_interaction(self):
        """Performs the players interaction with a weapon in their inventory"""
        if type(self.__inventory[self.__current_slot].item) == Weapon:
            self.__inventory[self.__current_slot].item.player_interaction(self)

    def perform_potion_interaction(self):
        """Performs the players interaction with a potion in their inventory"""
        if type(self.__inventory[self.__current_slot].item) == HealthPotion \
                or type(self.__inventory[self.__current_slot].item) == DamagePotion \
                or type(self.__inventory[self.__current_slot].item) == LuckPotion:
            self.__inventory[self.__current_slot].item.player_interaction(self)

    def pick_up_item(self, item):
        """
        Attempt to pick up an item
        :param item: the item to be picked up
        :type item: Item
        :return: True or False
        """
        return self.__inventory[self.__current_slot].update_item(item)

    def remove_item(self, new_map, items):
        """
        Attempt to remove an item from the players inventory
        :param new_map: the list of map tiles with their properties
        :type new_map: list
        :param items: the list of items
        :type items: list
        :return: new_map, items
        """
        new_map, items = self.__inventory[self.__current_slot].remove_item(self.direction, new_map, items)
        return new_map, items

    def delete_item(self):
        """Deletes the current item being used by the player"""
        self.__inventory[self.__current_slot].delete_item()

    def change_heart_display(self):
        """Update the number of hearts to be displayed to the players HUD"""
        self.__hearts = [Entity(num, 2, self.__full_heart) for num in range(0, self.health)]

    def check_if_dead(self, sprite_dead, damage):
        """
        Checks if the being is dead
        :param sprite_dead: the beings dead sprite
        :type sprite_dead: surface
        :param damage: the damage done to the being
        :type damage: int
        """
        self.health -= damage
        self.change_heart_display()
        if self.health <= 0:
            self._sprite = sprite_dead
            self.dead = True


class Enemy(Being):
    """Represents enemy sprites"""

    def __init__(self, x, y, health, damage, sprite_f, sprite_f_attack):
        """
        :param x: the enemies x coordinate
        :type x: int
        :param y: the enemies y coordinate
        :type y: int
        :param health: the enemies health
        :type health: int
        :param damage: the enemies damage
        :type damage: int
        :param sprite_f: the sprite for the enemy facing their default position
        :type sprite_f: surface
        :param sprite_f_attack: the list of sprites for the enemies default attack position
        :type sprite_f_attack: surface
        """
        super().__init__(x, y, health, damage, sprite_f, sprite_f_attack)
        self.__path = (0, 0)
        self.__route = []
        self.__clock = 0
        self.attacked_player = False

    def check_distance(self, attack_distance, object_left, object_right, new_map, player_moved_again):
        """
        Checks if the player is within a certain distance based on the length of the path to it
        :param attack_distance: the distance that an enemy will path towards the player if they are within
        :type attack_distance: int
        :param object_left: the tile to the left of the player
        :type object_left: tuple
        :param object_right: the tile to the right of the player
        :type object_right: tuple
        :param new_map: the list of tiles with their properties and vertices
        :type new_map: list
        :param player_moved_again: weather or not the player has moved
        :type player_moved_again: bool
        :returns: True if the player is within attack distance and False if not
        """
        x, y = self.__path
        if player_moved_again or new_map[x][y].occupied is True:
            coords = (self.x, self.y)  # Enemy coordinates
            left_distance = dist(coords, object_left)  # Distance between enemy and players left side coordinates
            right_distance = dist(coords, object_right)  # Distance between enemy and players right side coordinates
            x, y = object_left
            left_tile = new_map[x][y]
            x, y = object_right
            right_tile = new_map[x][y]
            if left_distance <= right_distance and left_tile.block_path is False and left_tile.occupied is False\
                    or coords == object_left:
                # If the left distance is less than or equal to the right distance
                # and the tile isn't occupied or a wall tile or the enemy is already at the objects left
                self.__path = object_left  # Path to the left side of the player
            elif right_tile.block_path is False and right_tile.occupied is False \
                    or coords == object_right:
                # If the left distance is less than or equal to the right distance
                # and the tile isn't occupied or a wall tile or the enemy is already at the objects left
                self.__path = object_right  # Path to the right side of the player
            elif left_tile.block_path is False and left_tile.occupied is False:
                self.__path = object_left
            else:
                return False  # Return False as there is no shortest distance to the player
            self.__route = find_shortest_path(new_map, (self.x, self.y), self.__path)  # Find a root to the player
            # using the shortest path algorithm
        if len(self.__route) + 1 <= attack_distance:  # If the length of the list
            # (+1 since the path includes the tile the enemy is currently on) is less than the attack distance
            return True  # Return True as the player is within attack distance
        else:  # Else
            return False  # Return False as they are not within attack distance

    def take_object_path(self, new_map, sprite_left, attack_left, sprite_right, attack_right):
        """
        Move the enemy onto the next tile in their self.path
        :param new_map: The list of tiles with their properties
        :type new_map: list
        :param sprite_left: The sprite for the enemy facing left
        :type sprite_left: surface
        :param attack_left: The list of enemy attack animations for facing left
        :type attack_left: list
        :param sprite_right: The sprite for the enemy facing right
        :type sprite_right: surface
        :param attack_right: The list of enemy attack animations for facing right
        :type attack_right: list
        :return new_map: an updated list of tiles with their properties
        """
        left_tile = new_map[self.x-1][self.y]
        right_tile = new_map[self.x+1][self.y]
        if len(self.__route) > 1 and self.moving is True:  # If the length the root to the player is greater than 1
            target_tile = self.__route[1]  # The target tile is the next one in the list
            self.__route.remove(self.__route[0])
            x, y = target_tile  # Target tiles x and y values
            if target_tile == (self.x+1, self.y):  # If the target tile is on the right
                new_map = self.move(new_map, x - self.x, y - self.y, sprite_right, attack_right)  # Move right
            elif target_tile == (self.x-1, self.y):  # If the target is on the left
                new_map = self.move(new_map, x - self.x, y - self.y, sprite_left, attack_left)  # Move left
            else:  # Else
                new_map = self.move(new_map, x - self.x, y - self.y, self._sprite, self._attack)  # Move
                # to the target tile
        elif type(left_tile.object) == Player:  # If the enemy is at the target
            self._sprite = sprite_left
            self._attack = attack_left
            self.moving = False  # They are no longer moving so they attack
            self.direction = (self.x - 1, self.y)
        elif type(right_tile.object) == Player:
            self._sprite = sprite_right
            self._attack = attack_right
            self.moving = False
            self.direction = (self.x + 1, self.y)
        return new_map  # Return an updated list of tiles with properties

    def attack_being(self, being, sprite_dead):
        """
        Allows a being to attack another being
        :param being: the being to be attacked
        :type being: Being
        :param sprite_dead: the dead sprite of the being to be attacked
        :type sprite_dead: surface
        :return being: the being object with their updates attributes
        """
        self.attacked_player = True
        being.check_if_dead(sprite_dead, self.damage)
        return being

    def perform_attack_animation(self, sprite_frames):
        """
        Allows a being object to cycle through their attack animation
        :param sprite_frames: the amount of frames an image from the attack animation is shown on screen
        :type sprite_frames: int
        """
        if self._attack_count + 1 >= (len(self._attack) * sprite_frames):  # If the beings attack count is
            # above the limit that would cause an index error
            self._attack_count = 0  # Reset the attack count
            self.moving = True  # Allow them to move again
            self.attacked_player = False
        else:  # If not
            self._attack_animation(sprite_frames)  # Allow the being to attack
