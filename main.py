import pygame
import constants
from map import create_map, draw_map, spawn_map
from objs import Player, Camera, Font, Chest, Enemy, Weapon, LuckPotion, HealthPotion, DamagePotion


def game_draw(screen, map_surface, current_map, sprites, camera, exit_point, map_width, map_height, player, level_font):
    """
    Function that draws everything to the screen, e.g. the background
    :param screen: the screen to be drawn to
    :type screen: surface
    :param map_surface: the place where everything on the map is drawn
    :type map_surface: surface
    :param current_map: the list of tiles with their properties
    :type current_map: list
    :param sprites: a list of sprites to draw
    :type sprites: list
    :param camera: the players view of the map
    :type camera: Camera
    :param exit_point: the place where the player can exit the map
    :type exit_point: Entity
    :param map_width: the width of the map
    :type map_width: int
    :param map_height: the height of the map
    :type map_height: int
    :param player: the player character
    :type player: Player
    :param level_font: the font to be drawn to the screen that displays the current level
    :type level_font: Font
    """
    screen.fill(constants.black)  # Fill the background with the colour black

    camera.update(player.x, player.y, constants.cellWidth, constants.cellHeight)  # Update the camera

    draw_map(current_map, map_surface, map_width, map_height, constants.cellWidth,
             constants.cellHeight, constants.wall, constants.floor)  # Draw the map to the screen

    exit_point.draw(map_surface, constants.cellWidth, constants.cellHeight)  # Draw the exit to the screen
    for group in sprites:
        for sprite in group:  # For each sprite
            sprite.draw(map_surface, constants.cellWidth, constants.cellHeight)  # Draw all sprites to the screen

    player.draw(map_surface, constants.cellWidth, constants.cellHeight)  # Draw the player to the screen

    screen.blit(map_surface, (0, 0), camera.rectangle)  # Third argument is the optional width and height of the display

    # HUD
    level_font.draw(screen, constants.cellWidth, constants.cellHeight)  # Draw the font to the screen
    player.draw_display(screen, constants.cellWidth, constants.cellHeight)  # Draw the players inventory to the screen

    pygame.display.flip()  # Update the screen


def game_initialise():
    """Initialises PyGame and the game window"""

    pygame.init()  # Initialise PyGame

    # Title and icon
    pygame.display.set_caption(constants.title)  # Set the title of the window
    pygame.display.set_icon(constants.icon)  # Set the windows icon


def game_loop():
    """Main game loop that updates the screen"""

    # Clock
    clock = pygame.time.Clock()
    enemy_move_timer = 0
    enemy_moved = False

    # Set map base stats
    level = 1  # The players current level
    room_num = 3  # The max number of rooms that can spawn on a map - original 3
    map_height = 20  # The height of the map - original 20
    map_width = 20  # The width of the map - original 20
    max_room_width = 4  # The max possible room width - must be higher than 2 - original 4
    max_room_height = 4  # The max possible room height - must be higher than 2 - original 4
    x, y = constants.levelFontCoordinates
    level_font = Font(x, y, constants.font1, constants.white, "Level " + str(level))  # Level font

    # Set player base stats
    player_health = 5  # Players health number
    player_damage = 1  # Players damage number

    # Set enemy base stats
    enemy_chance = 2  # Chance enemies spawn out of 10
    max_enemy_num = 2  # Max number of enemies that can spawn - original 2
    max_enemy_health = 2  # Max amount of enemy health
    max_enemy_damage = 1  # Max amount of enemy damage

    # Set loot base stats
    loot_chance = 6  # Base loot chance out of 10
    max_loot_num = 3  # Max amount of loot that can spawn - original 3

    # Create the screen and camera
    screen = pygame.display.set_mode((constants.gameWidth, constants.gameHeight))  # Game window size
    camera = Camera(constants.gameWidth, constants.gameHeight)

    # Create player
    player = Player(0, 0, player_health, player_damage, constants.playerFront, constants.playerFrontAttack,
                    constants.playerInventorySize, constants.inventorySprite, constants.heart, constants.font3,
                    constants.black, constants.playerHealthLimit)

    # Create loot templates
    sprite, name = constants.swordT1
    sword_t1 = {'sprite': sprite, 'name': name, 'min damage': 1, 'max damage': 2}
    sprite, name = constants.swordT2
    sword_t2 = {'sprite': sprite, 'name': name, 'min damage': 1, 'max damage': 2}
    sprite, name = constants.swordT3
    sword_t3 = {'sprite': sprite, 'name': name, 'min damage': 1, 'max damage': 3}
    sprite, name = constants.swordT4
    sword_t4 = {'sprite': sprite, 'name': name, 'min damage': 2, 'max damage': 4}
    sprite, name = constants.swordT5
    sword_t5 = {'sprite': sprite, 'name': name, 'min damage': 2, 'max damage': 5}
    sprite, name = constants.swordT6
    sword_t6 = {'sprite': sprite, 'name': name, 'min damage': 3, 'max damage': 5}
    sprite, name = constants.bluePotion
    blue_potion = {'sprite': sprite, 'name': name, 'min value': 1, 'max value': 2}
    sprite, name = constants.redPotion
    red_potion = {'sprite': sprite, 'name': name, 'min value': 1, 'max value': 2}
    sprite, name = constants.greenPotion
    green_potion = {'sprite': sprite, 'name': name, 'min value': 0.1, 'max value': 0.3}
    loot_items = {'weapons': [sword_t1, sword_t2, sword_t3, sword_t4, sword_t5, sword_t6],
                  'blue potions': [blue_potion],
                  'red potions': [red_potion],
                  'green potions': [green_potion]}

    # Game loop
    running = True
    while running:  # While the game is still running
        in_game = True
        game_over = False
        while in_game:  # While in the game
            completed = False

            # Update the map specifications
            if level % 5 == 0 and level < 101:  # Every 5 levels up to level 100
                # Increase these map / enemy stats
                room_num += 1
                map_width += 3
                map_height += 3
                max_enemy_num += 1
            if level % 10 == 0 and level < 101:  # Every 10 levels up to level 100
                # Increase these map / enemy stats
                for weapon in loot_items['weapons']:
                    weapon['min damage'] += 1
                    weapon['max damage'] += 1
                for potion in loot_items['blue potions']:
                    potion['min value'] += 1
                    potion['max value'] += 1
                for potion in loot_items['red potions']:
                    potion['min value'] += 1
                    potion['max value'] += 1
                for potion in loot_items['green potions']:
                    potion['min value'] += 0.1
                    potion['max value'] += 0.1
                max_room_width += 1
                max_room_height += 1
                max_enemy_health += 1
                max_enemy_damage += 1
            if level == 5:  # At level 5
                # Increase these enemy and chest chances / numbers
                loot_chance = 3
                max_loot_num = 1
                enemy_chance = 4
                max_enemy_num = 3
            elif level == 10:  # At level 10
                # Increase these enemy and chest chances / numbers
                loot_chance = 4
                enemy_chance = 5
            elif level == 20:  # At level 20
                # Increase these enemy and chest chances / numbers
                max_loot_num = 2
                max_enemy_num = 5
                loot_chance = 5
            elif level == 50:  # At level 50
                # Increase the enemy chance
                enemy_chance = 7
            elif level == 65:  # At level 65
                # Increase the enemy number
                max_enemy_num = 6
            elif level == 80:  # At level 80
                # Increase these enemy and chest chances / numbers
                max_loot_num = 3
                loot_chance = 6
                max_enemy_num = 8
                enemy_chance = 8

            # Generate a new map and spawn things on it and a new map surface
            map_surface = pygame.Surface((map_width * constants.cellWidth, map_height * constants.cellHeight))
            new_map, rooms = create_map(room_num, map_height, map_width, constants.minRoomWidth, max_room_width,
                                        constants.minRoomHeight, max_room_height)
            item_font = (constants.inventoryItemFontCoordinates, constants.font1, constants.blue)
            new_map, player.x, player.y, exit_point, rooms, enemies, chests = spawn_map(new_map, rooms, loot_chance,
                                                                                        max_loot_num, enemy_chance,
                                                                                        max_enemy_num,
                                                                                        max_enemy_health,
                                                                                        max_enemy_damage,
                                                                                        constants.ladder,
                                                                                        constants.chest,
                                                                                        constants.enemyLeft,
                                                                                        constants.enemyRight,
                                                                                        constants.enemyLeftAttack,
                                                                                        constants.enemyRightAttack,
                                                                                        loot_items, item_font,
                                                                                        player.luck)
            items = []  # Create a blank list of items - only includes ones to be drawn to the screen
            level_font.set_text("Level " + str(level))  # Reset the level text
            player.set_direction()  # Reset the players direction

            while not completed and in_game:  # While the current level has not been completed
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # If the user presses the button to close the window
                        running = False  # Stop the game loop
                        in_game = False  # Stop the in game loop
                    if event.type == pygame.KEYDOWN:  # If the user presses a key down
                        if not player.dead:  # If the player is not dead
                            if event.key == pygame.K_a and player.moving:  # If the key 'a' and the player can move
                                x_change = -1  # The change in the players x direction
                                new_map = player.move(new_map, x_change, 0, constants.playerLeft,
                                                      constants.playerLeftAttack)
                            if event.key == pygame.K_d and player.moving:  # If the key is 'd' and the player can move
                                x_change = 1  # The change in the players x direction
                                new_map = player.move(new_map, x_change, 0, constants.playerRight,
                                                      constants.playerRightAttack)
                            if event.key == pygame.K_w and player.moving:  # If the key is 'w' and the player can move
                                y_change = -1  # The change in the players y direction
                                new_map = player.move(new_map, 0, y_change, constants.playerBack,
                                                      constants.playerBackAttack)
                            if event.key == pygame.K_s and player.moving:  # If the key is 's' and the player can move
                                y_change = 1  # The change in the players y direction
                                new_map = player.move(new_map, 0, y_change, constants.playerFront,
                                                      constants.playerFrontAttack)
                            if event.key == pygame.K_1:  # If the '1' key is pressed
                                player.update_current_slot(0)  # Change the players inventory slot to number 1
                                player.perform_weapon_interaction()  # Attempt to perform an interaction with a weapon
                            if event.key == pygame.K_2:  # If the '2' key is pressed
                                player.update_current_slot(1)  # Change the players inventory slot to number 2
                                player.perform_weapon_interaction()  # Attempt to perform an interaction with a weapon
                            if event.key == pygame.K_3:  # If the '3' key is pressed
                                player.update_current_slot(2)  # Change the players inventory slot to number 3
                                player.perform_weapon_interaction()  # Attempt to perform an interaction with a weapon
                            if event.key == pygame.K_4:  # If the '4' key is pressed
                                player.update_current_slot(3)  # Change the players inventory slot to number 4
                                player.perform_weapon_interaction()  # Attempt to perform an interaction with a weapon
                            if event.key == pygame.K_5:  # If the '5' key is pressed
                                player.update_current_slot(4)  # Change the players inventory slot to number 5
                                player.perform_weapon_interaction()  # Attempt to perform an interaction with a weapon
                            if event.key == pygame.K_r:  # If the 'r' key is pressed
                                new_map, items = player.remove_item(new_map, items)  # Drop the players current item
                                # from their inventory
                            if event.key == pygame.K_f:  # If the 'f' key is pressed
                                player.perform_potion_interaction()  # Attempt to perform an interaction with a potion
                                player.change_heart_display()  # Update the number of hearts being displayed
                            if event.key == pygame.K_SPACE and player.moving:  # If the key is "space"
                                # and the player can move
                                x, y = player.direction  # Players direction x and y coordinates
                                tile_object = new_map[x][y].object  # The object at those x and y coordinates
                                if tile_object == exit_point:  # If the player is next to the exit
                                    level += 1  # Increase the level number
                                    completed = True  # Make the level completed
                                elif type(tile_object) == Chest:  # If the object is a chest
                                    chests, new_map, item = tile_object.remove_sprite(chests, new_map)
                                    # Remove that chest from the list of chests
                                    items.append(item)  # Add the item from the chest to the list of items
                                    # to be drawn to the screen
                                elif type(tile_object) == Enemy:  # If the object is an Enemy
                                    player.moving = False  # The player is no longer moving
                                    enemies.remove(tile_object)  # The enemy is removed from the list of enemies
                                    tile_object = player.attack_being(tile_object, constants.enemyDead)
                                    # The player attacks the enemy
                                    enemies.append(tile_object)  # The enemy is added back into the list of enemies
                                elif type(tile_object) == Weapon or type(tile_object) == LuckPotion\
                                        or type(tile_object) == HealthPotion or type(tile_object) == DamagePotion:
                                    # If the object is an item of any type
                                    if player.pick_up_item(tile_object):  # If the item can be and has been picked up
                                        items, new_map = tile_object.remove_sprite(items, new_map, x, y)
                                        # Remove that item from the list of items
                                        player.perform_weapon_interaction()  # Attempt to perform an interaction
                                        # with a weapon
                                else:  # Else
                                    player.moving = False  # Make it so that the player can't move

                if not player.moving:  # If the player isn't moving then they are attacking
                    player.perform_attack_animation(constants.spriteFrames)

                # Allow Enemies to attack the player
                player_left = (player.x-1, player.y)  # Tile to players left
                player_right = (player.x+1, player.y)  # Tile to players right
                for enemy in enemies:  # For each enemy
                    if not enemy.dead:  # If they are not dead
                        if enemy.check_distance(constants.attackDistance, player_left, player_right, new_map,
                                                player.moved_again)\
                                and enemy_move_timer >= constants.enemyMoveSpeed and enemy.moving:
                            # If they are within distance to attack the player and it is time for them to move again
                            # and they can move
                            new_map = enemy.take_object_path(new_map, constants.enemyLeft, constants.enemyLeftAttack,
                                                             constants.enemyRight, constants.enemyRightAttack)
                            # Take a path to the player
                            enemy_moved = True  # An enemy has moved
                        elif not enemy.moving:  # If the enemy is not moving they are attacking
                            enemy.perform_attack_animation(constants.spriteFrames)  # Let them perform
                            # their attack animation
                            x, y = enemy.direction  # Tile the enemy is facing
                            if type(new_map[x][y].object) == Player and not enemy.attacked_player:
                                # If the player is on the tile in front
                                # and the enemy has attacked the player this attack animation
                                player = enemy.attack_being(player, constants.playerDead)
                                # The enemy attacks the player
                    elif enemy.dead and enemy.check_dead_timer(clock.get_time(), constants.enemyDeadSpeed):
                        # If the enemy is dead and they have been dead for a specified amount of time
                        enemies, new_map = enemy.remove_sprite(enemies, new_map)  # Remove them from the list of enemies

                # Frame rate
                clock.tick(constants.frameRate)
                if enemy_moved:  # If an enemy has moved
                    enemy_move_timer = 0  # Reset the enemy move timer
                    enemy_moved = False  # Make it so an enemy has not moved
                enemy_move_timer += clock.get_time()  # Add additional time to the enemy move timer

                # Update the screen
                sprites = [enemies, chests, items]  # List of lists of sprites to be drawn
                game_draw(screen, map_surface, new_map, sprites, camera, exit_point, map_width, map_height, player,
                          level_font)

                # Update the players
                if player.moved_again:  # If the player has moved again
                    player.moved_again = False  # Make it so that they haven't moved again
                if player.dead and player.check_dead_timer(clock.get_time(), constants.playerDeadSpeed):
                    # If the player is dead and they have been dead for a specified amount of time
                    in_game = False  # Stop the game loop
                    completed = True  # Set the level to complete
                    game_over = True  # Start the game over loop

        while game_over:  # While the game is over
            screen.fill(constants.black)  # Fill the screen with black
            x, y = constants.gameOverFontCoordinates  # x and y coordinates of the game over text
            game_over_font = Font(x, y, constants.font2, constants.white, constants.gameOver)
            game_over_font.draw(screen, constants.cellWidth, constants.cellHeight)  # Draw 'GAME OVER' to the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the user presses the button to close the window
                    running = False  # Stop the game loop
                    game_over = False  # Stop the in game loop
            pygame.display.flip()  # Update the screen


if __name__ == "__main__":
    game_initialise()
    game_loop()
