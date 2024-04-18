import pygame
from objs import Tile, Room, Chest, Entity, Enemy, Weapon, HealthPotion, DamagePotion, LuckPotion
from random import randint, choice
from sort import merge_sort

pygame.init()  # Initialise PyGame


def check_tiles(tiles):
    """
    Check the specified tiles to see if any of them are already occupied by a room tile
    :param tiles: the tiles to be checked
    :type tiles: list
    :returns: False if one of the tiles is already by a room tile and True if no tiles are occupied by a floor tile
    """
    for row in tiles:  # For each list of tiles
        for tile in row:  # For each individual tile
            if tile.floor_tile is True:  # If it is already a floor tile
                return False  # End the function and return False
    return True  # If every tile has been checked and none are floor tiles then return True


def generate_tunnel_x_pos(new_map, target, x, y):
    """
    Recursive function that tunnels to a targets x value by removing the tiles block path attribute, only works if the
    starting x value is higher than the tunnels x value
    :param new_map: list of tiles with properties
    :type new_map: list
    :param target: the target x coord
    :type target: int
    :param x: the current x coord of the tunnel
    :type x: int
    :param y: the current y coord of the tunnel
    :type y: int
    """
    if x == target:  # If the tunnel has reached the target
        return new_map, x  # Return the edited map
    else:  # If not
        new_map[x][y].block_path = False  # Remove the current tiles block_path attribute
        new_map[x][y-1].block_path = False  # And the one next to it (creates a 2x wide tunnel)
        return generate_tunnel_x_pos(new_map, target, x+1, y)  # Call the function again, but increase the x value by 1


def generate_tunnel_x_neg(new_map, target, x, y):
    """
    Recursive function that tunnels to a targets x value by removing the tiles block path attribute, only works if the
    target x value is lower than the tunnels x value
    :param new_map: list of tiles with properties
    :type new_map: list
    :param target: the target x coord
    :type target: int
    :param x: the current x coord of the tunnel
    :type x: int
    :param y: the current y coord of the tunnel
    :type y: int
    """
    if x == target:
        return new_map, x
    else:
        new_map[x][y].block_path = False
        new_map[x][y-1].block_path = False
        return generate_tunnel_x_neg(new_map, target, x-1, y)  # Call the function again, but decrease the x value by 1


def generate_tunnel_y_pos(new_map, target, x, y):
    """
    Recursive function that tunnels to a targets y value by removing the tiles block path attribute, only works if the
    target y value is higher than tunnels y value
    :param new_map: list of tiles with properties
    :type new_map: list
    :param target: the target y coord
    :type target: int
    :param x: the current x coord of the tunnel
    :type x: int
    :param y: the current y coord of the tunnel
    :type y: int
    """
    if y == target:
        return new_map
    else:
        new_map[x][y].block_path = False
        new_map[x+1][y].block_path = False
        return generate_tunnel_y_pos(new_map, target, x, y+1)  # Call the function again, but increase the y value by 1


def generate_tunnel_y_neg(new_map, target, x, y):
    """
    Recursive function that tunnels to a targets y value by removing the tiles block path attribute, only works if the
    target y value is lower than the tunnels y value
    :param new_map: list of tiles with properties
    :type new_map: list
    :param target: the target y coord
    :type target: int
    :param x: the current x coord of the tunnel
    :type x: int
    :param y: the current y coord of the tunnel
    :type y: int
    """
    if y == target:
        return new_map
    else:
        new_map[x][y].block_path = False
        new_map[x+1][y].block_path = False
        return generate_tunnel_y_neg(new_map, target, x, y-1)  # Call the function again, but decrease the y value by 1


def create_map(room_num, map_height, map_width, min_room_width, max_room_width, min_room_height, max_room_height):
    """
    Creates a list of map tiles with properties
    :param room_num: the max number of rooms that can be drawn
    :type room_num: int
    :param map_height: the height of the map
    :type map_height: int
    :param map_width: the width of the map
    :type map_width: int
    :param min_room_width: the minimum room width
    :type min_room_width: int
    :param max_room_width: the max room width
    :type max_room_width: int
    :param min_room_height: the minimum room height
    :type min_room_height: int
    :param max_room_height: the maximum room height
    :type max_room_height: int
    :return: a map with tiles that each have their own properties
    """
    # Generate the blank map
    new_map = [[Tile(True, False, True, False, x, y, map_width, map_height)
                for y in range(0, map_height)] for x in range(0, map_width)]
    # Creates a map with nothing but wall tiles
    # Also makes all the tiles blank until it can be determined if they are a floor or wall tile
    # It does this by creating a 2d array, with the x being the number of lists in the list,
    # y being the index of every tile in each of those lists

    # Add the rooms to the map
    rooms = []  # This list contains all of the room objects in use
    room_count = 0  # This counts how many rooms have been placed
    while room_count <= room_num or len(rooms) < 2:  # While there are less rooms than the max amount to be placed
        # or there are less than two rooms placed (which is required for the game to function)
        room_count += 1

        # Generate room coords
        x_coord = randint(2, map_width - max_room_width - 2)  # Generate a random x coord based on
        # the max specified value
        y_coord = randint(2, map_height - max_room_height - 2)  # Generate a random y coord based on
        # the max specified value
        #  The start of the range is 1 to ensure that no rooms generate on the very edge of the map
        #  The end of the range is the map height/width take away the max room height/width - 1 to ensure that no rooms
        #  generate on the very edge of the map and that the rooms have enough space for their max potential size
        width = randint(min_room_width, max_room_width)  # Generate a random room width based on the
        # max specified value
        height = randint(min_room_height, max_room_height)  # Generate a random room height based on the
        # max specified values

        # Check if the room can be placed
        x_range = new_map[x_coord-1:x_coord+width+2]  # Slice the map array to the x coords of the room
        tiles = [y[y_coord-1: y_coord+height+2] for y in x_range]  # Slice that slice to the y coords of the room
        #  The -1 and the +2 are added to the slices arguments to ensure
        #  that rooms generate a reasonable distance from one another
        if check_tiles(tiles) is True:  # If none of the specified tiles are already room tiles
            x_coordinates = []  # This list will hold the lists of y coords
            for x in range(x_coord, x_coord + width):  # For each x coord in the range of the room width
                y_coordinates = []  # This list will hold the tuples of coords
                for y in range(y_coord, y_coord + height):  # For each y coord in the range of the room height
                    new_map[x][y].floor_tile = True  # Turn the tile to a floor tile
                    new_map[x][y].block_path = False  # Make the tile no longer a wall tile
                    y_coordinates.append((x, y))  # Add the coords to the list of y coords as a tuple
                x_coordinates.append(y_coordinates)  # Add the list of tuples to the x coords

            # Tunnel to another room
            x_centre = x_coord + (width // 2)  # Calculate the x coord centre of the room
            y_centre = y_coord + (height // 2)  # Calculate the y coord centre of the room
            room = Room(x_coordinates, x_centre, y_centre)  # Instance the room object
            if len(rooms) > 0:  # if there are more than one room
                if len(rooms) == 2:  # If there are only 2 rooms
                    target_room = rooms[0]  # The target room is the first one to generate - this ensures that there is
                    # a tunnel to the first room
                else:  # Else
                    target_room = choice(rooms)  # Choose a random room to tunnel to
                target_x = target_room.centre_x  # Target x value
                target_y = target_room.centre_y  # Target y values
                if room.centre_x <= target_x:  # If the target is x is higher than the rooms x
                    new_map, tunnel_x = generate_tunnel_x_pos(new_map, target_x+1, room.centre_x, room.centre_y)
                    # Tunnel right
                    if room.centre_y <= target_y:  # If the target is x is higher than the rooms x
                        new_map = generate_tunnel_y_pos(new_map, target_y, tunnel_x-2, room.centre_y)  # Tunnel down
                    else:  # If not
                        new_map = generate_tunnel_y_neg(new_map, target_y, tunnel_x-2, room.centre_y)  # Tunnel up
                else:  # If not
                    new_map, tunnel_x = generate_tunnel_x_neg(new_map, target_x-2, room.centre_x, room.centre_y)
                    if room.centre_y <= target_y:  # If the target is x is higher than the rooms x
                        new_map = generate_tunnel_y_pos(new_map, target_y, tunnel_x+1, room.centre_y)  # Tunnel down
                    else:  # If not
                        new_map = generate_tunnel_y_neg(new_map, target_y, tunnel_x+1, room.centre_y)  # Tunnel up
                    # Tunnel left
            rooms.append(room)  # Add the current room object to the list of rooms

    # Make all valid tiles visible
    for x in range(1, map_width-1):  # For each x coord (ignoring those on the boundary to avoid index error)
        for y in range(1, map_height-1):  # For each y coord (ignoring those on the boundary to avoid index error)
            if new_map[x][y].block_path is False:  # If it is not a wall tile
                new_map[x][y].empty = False  # It will be shown to the screen
            if new_map[x][y].block_path is True:  # If it is a wall tile
                if new_map[x+1][y].block_path is False\
                        or new_map[x-1][y].block_path is False\
                        or new_map[x][y+1].block_path is False\
                        or new_map[x][y-1].block_path is False\
                        or new_map[x+1][y+1].block_path is False\
                        or new_map[x+1][y-1].block_path is False\
                        or new_map[x-1][y-1].block_path is False\
                        or new_map[x-1][y+1].block_path is False:
                    # If the tile to the right is a floor tile
                    # or the one to the left
                    # or the one below
                    # or the one above
                    # or the one diagonally right and down
                    # or the one diagonally right and up
                    # or the one diagonally left and up
                    # or the one diagonally left and down
                    new_map[x][y].empty = False  # The current tile will be shown to the screen
                    # This means that only wall tiles on the borders of rooms will be shown

    return new_map, rooms


def spawn_map(new_map, rooms, loot_chance, max_loot_num, enemy_chance, max_enemy_num, max_enemy_health,
              max_enemy_damage, ladder, chest, enemy_left, enemy_right, enemy_left_attack, enemy_right_attack,
              loot_items, item_font, player_luck):
    """
    Choose the spawn location for things on the map such as the player and loot chests
    :param new_map: the list of map tiles with their properties
    :type new_map: list
    :param rooms: list of room objects
    :type rooms: list
    :param loot_chance: the chance that loot will spawn out of 10
    :type loot_chance: int
    :param max_loot_num: the max amount of loot than can spawn
    :type max_loot_num: int
    :param enemy_chance: the chance an enemy will spawn out of 10
    :type enemy_chance: int
    :param max_enemy_num: the max amount of enemies that can spawn
    :type max_enemy_num: int
    :param max_enemy_health: the max amount of enemy health
    :type max_enemy_health: int
    :param max_enemy_damage: the max amount of enemy damage
    :type max_enemy_damage: int
    :param ladder: the sprite for a ladder
    :type ladder: surface
    :param chest: the sprite for a chest
    :type chest: surface
    :param enemy_left: the left-facing sprite for an enemy
    :type enemy_left: surface
    :param enemy_right: the right-facing sprite for an enemy
    :type enemy_right: surface
    :param enemy_left_attack: the left-facing attack of an enemy
    :type enemy_left_attack: list
    :param enemy_right_attack: the right-facing attack of an enemy
    :type enemy_right_attack: list
    :param loot_items: dictionary of loot items that will spawn
    :type loot_items: dict
    :param item_font: the values for the item font, colour, type, etc
    :type item_font: tuple
    :param player_luck: the players luck stat
    :type player_luck: float
    :returns: a list of tiles that now have spawn locations, the players spawn coords, the exit location,
    a list of sorted rooms, a list of Enemy objects, and a list of Chest objects
    """
    distances = [room.distance for room in rooms]  # Create a list of the rooms distances
    distances = merge_sort(distances)  # Sort those from smallest to largest
    sorted_rooms = []  # This list is used to store the rooms objects but in order of smallest to largest distance
    for distance in distances:  # For each distance
        for room in rooms:  # For each room
            if room.distance == distance:  # If the current rooms distance is the next one in order
                sorted_rooms.append(room)  # Add it to the sorted list
                break  # Break the loop to avoid adding rooms multiple times if different rooms have the same distance
    player_x = sorted_rooms[0].centre_x  # Set the players x coord to the room centre that has the smallest distance
    player_y = sorted_rooms[0].centre_y  # Same for the y coord
    exit_x = sorted_rooms[-1].centre_x  # Set the exit to the room centre that has the largest distance
    exit_y = sorted_rooms[-1].centre_y  # Same for the y coord
    if (player_x, player_y) == (exit_x, exit_y):
        exit_x = sorted_rooms[1].centre_x
        exit_y = sorted_rooms[1].centre_y
    exit_point = Entity(exit_x, exit_y, ladder)
    new_map[exit_x][exit_y].occupied = True  # Make it so that the exit tile cannot be walked through
    new_map[exit_x][exit_y].object = exit_point

    enemy_sprites = [(enemy_left, enemy_left_attack), (enemy_right, enemy_right_attack)]
    # Create a list of enemy sprites to allow randomisation of their direction
    enemies = []  # List of enemy objects
    chests = []  # List of chest objects
    font_coords, font, colour = item_font  # Unpack fonts coordinates, font, and colour
    font_x, font_y = font_coords
    for num in range(0, int(player_luck)+1, 2):  # For every 2 of the players luck
        max_loot_num += 1  # Increase the max amount of loot that can spawn per room
    for room in sorted_rooms:  # For each room
        if sorted_rooms.index(room) != 0:  # If the room is not the same as the one the player will spawn in
            for _ in range(0, max_enemy_num):  # For the max amount of enemies that can spawn
                chance = randint(0, 10)  # The chance an enemy will spawn
                if chance <= enemy_chance:  # If an enemy will spawn
                    searching = True
                    attempts = 0
                    while searching and attempts < 6:  # While searching for a spot to place an enemy
                        # and it has been attempted less than 6 times
                        attempts += 1
                        tiles = choice(room.tiles)  # Choose a random tile row from the rooms tiles
                        tile = choice(tiles)  # Choose a random tile in that row
                        x, y = tile  # Tiles x and y coordinates
                        if new_map[x][y].occupied is False and new_map[x][y].block_path is False:  # If the tile
                            # isn't already occupied and isn't a wall tile
                            enemy_sprite_direction = choice(enemy_sprites)  # Choose a random direction
                            # for the enemy to spawn in facing
                            enemy_sprite, enemy_attack = enemy_sprite_direction  # Unpack the sprite and attack from it
                            enemy_health = randint(1, max_enemy_health)  # Generate random health value for enemy
                            enemy_damage = randint(1, max_enemy_damage)  # Generate random damage value for enemy
                            new_enemy = Enemy(x, y, enemy_health, enemy_damage, enemy_sprite, enemy_attack)
                            # Create the new enemy object
                            enemies.append(new_enemy)  # Add it to the list
                            new_map[x][y].object = new_enemy  # Set it as the object for the tiles it spawned on
                            new_map[x][y].occupied = True  # Set the tile it spawned on as occupied
                            searching = False  # Stop searching for a place to spawn an enemy
        for _ in range(0, max_loot_num):  # For the max amount of loot that can spawn
            chance = randint(0, 10)  # The chance that loot will spawn
            if chance <= loot_chance:  # If it will spawn
                searching = True
                attempts = 0
                while searching and attempts < 6:  # While searching for a spot to place loot
                    # and it has been attempted less that 6 times
                    attempts += 1
                    tiles = choice(room.tiles)  # Select a random column to place the loot
                    tile = choice(tiles)  # Select a random tile in that column
                    x, y = tile  # Unpack the x and y values from the tuple
                    if new_map[x][y].occupied is False and tile != (player_x, player_y)\
                            and new_map[x][y].block_path is False:
                        # If the tile isn't occupied
                        # and it isn't the tile that the player spawns on
                        loot_type = choice(['weapons', 'blue potions', 'red potions', 'green potions'])
                        loot = choice(loot_items[loot_type])
                        if loot_type == 'weapons':
                            item = Weapon(x, y, loot['sprite'], loot['name'], 1, loot['min damage'],
                                          loot['max damage'], font_x, font_y, font, colour)
                        elif loot_type == 'blue potions':
                            item = DamagePotion(x, y, loot['sprite'], loot['name'], 1, loot['min value'],
                                                loot['max value'], font_x, font_y, font, colour)
                        elif loot_type == 'red potions':
                            item = HealthPotion(x, y, loot['sprite'], loot['name'], 1, loot['min value'],
                                                loot['max value'], font_x, font_y, font, colour)
                        elif loot_type == 'green potions':
                            item = LuckPotion(x, y, loot['sprite'], loot['name'], 0.1, loot['min value'],
                                              loot['max value'], font_x, font_y, font, colour)
                        else:
                            item = Weapon(x, y, ladder, '', 0, 0, 1, font_x, font_y, font, colour)
                            # Default item if no valid loot type is found
                        item.generate_value()  # Generate a value for the item
                        new_chest = Chest(x, y, chest, item)
                        chests.append(new_chest)  # Add a new chest object to the list of chests
                        new_map[x][y].occupied = True  # Make the tile occupied
                        new_map[x][y].object = new_chest  # Make the tile a chest tile
                        searching = False  # Stop searching for a space to put the chest
    return new_map, player_x, player_y, exit_point, sorted_rooms, enemies, chests


def draw_map(map_to_draw, screen, map_width, map_height, cell_width, cell_height, wall, floor):
    """
    Draws the finished map with the correct properties for each tile
    :param map_to_draw: the list of tiles with their properties
    :type map_to_draw: list
    :param screen: the screen to be drawn to
    :type screen: surface
    :param map_width: the height of the map in tiles
    :type map_width: int
    :param map_height: the width of the map in tiles
    :type map_height: int
    :param cell_width: the width of a cell
    :type cell_width: int
    :param cell_height: the height of a cell
    :type cell_height: int
    :param wall: the sprite for a wall tile
    :type wall: surface
    :param floor: the sprite for a floor tile
    :type floor: surface
    """
    for x in range(0, map_width):  # For each x coord
        for y in range(0, map_height):  # For each y coord
            # The tiles are drawn by multiplying their x and y the specified cell width and height to convert
            # the map address to a pixel on the screen
            if map_to_draw[x][y].empty is False:  # If the tile can be drawn
                if map_to_draw[x][y].block_path is True:  # If the tile
                    # blocks the players path
                    screen.blit(wall, (x * cell_width, y * cell_height))  # Draw a wall tile
                elif map_to_draw[x][y].floor_tile is True:  # If the tile is part of a room
                    screen.blit(floor, (x * cell_width, y * cell_height))  # Draw a floor tile
                else:  # If none of the above
                    screen.blit(floor, (x * cell_width, y * cell_height))  # Draw a floor tile
