from random import randint, choice
from map import create_map  # TODO remove


# TODO TEST


new_map, rooms = create_map(5, 30, 30, 4, 6, 4, 6)


def random_spawn(max_num, spawn_chance, new_map, player_coords):
    def decorator_spawn(spawn_func, tile_func):
        def wrapper_spawn(*args, **kwargs):
            new_objects = []
            for _ in range(0, max_num):
                chance = randint(0, 10)
                if chance <= spawn_chance:
                    searching = True
                    while searching:
                        tiles = choice(room_tiles)
                        tile = choice(tiles)
                        x, y = tile
                        if new_map[x][y].occupied is False and tile != player_coords:
                            new_objects = spawn_func(*args, **kwargs)
                            new_map[x][y].occupied = True
                            searching = False
            return new_objects, new_map
        return wrapper_spawn
    return decorator_spawn


@random_spawn(5, 8, new_map, (5, 6))
def spawn_enemies(new_map, rooms):
    pass

