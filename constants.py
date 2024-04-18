import pygame

pygame.init()  # Initialise PyGame

# Game sizes
gameWidth = 800  # Width of game window
gameHeight = 600  # Length
cellWidth = 32  # Width of tiles
cellHeight = 32  # Height of tiles

# Map
minRoomWidth = 4  # Minimum room width - should be greater than 3
minRoomHeight = 4  # Minimum room height - should be greater than 3

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# Sprites and title
title = "Dungeon Crawler"
icon = pygame.image.load('icon.png')
floor = pygame.image.load('floor.jpg')
wall = pygame.image.load('wall.png')
ladder = pygame.image.load('ladder.png')
chest = pygame.image.load('chest.png')
font1 = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 80)
font3 = pygame.font.Font('freesansbold.ttf', 15)
gameOver = "GAME OVER"  # Text to be displayed when the game is over
levelFontCoordinates = (0, 0)
gameOverFontCoordinates = (4, 8)
inventoryItemFontCoordinates = (9, 17)
# Player sprites
playerDead = pygame.image.load('p dead.png')
playerFront = pygame.image.load('pf.png')
playerF1 = pygame.image.load('pf1.png')
playerF2 = pygame.image.load('pf2.png')
playerF3 = pygame.image.load('pf3.png')
playerF4 = pygame.image.load('pf4.png')
playerFrontAttack = [playerF1, playerF2, playerF3, playerF4, playerFront]
playerBack = pygame.image.load('pb.png')
playerB1 = pygame.image.load('pb1.png')
playerB2 = pygame.image.load('pb2.png')
playerB3 = pygame.image.load('pb3.png')
playerB4 = pygame.image.load('pb4.png')
playerBackAttack = [playerB1, playerB2, playerB3, playerB4, playerBack]
playerRight = pygame.image.load('pr.png')
playerR1 = pygame.image.load('pr1.png')
playerR2 = pygame.image.load('pr2.png')
playerR3 = pygame.image.load('pr3.png')
playerR4 = pygame.image.load('pr4.png')
playerRightAttack = [playerR1, playerR2, playerR3, playerR4, playerRight]
playerLeft = pygame.image.load('pl.png')
playerL1 = pygame.image.load('pl1.png')
playerL2 = pygame.image.load('pl2.png')
playerL3 = pygame.image.load('pl3.png')
playerL4 = pygame.image.load('pl4.png')
playerLeftAttack = [playerL1, playerL2, playerL3, playerL4, playerLeft]
# Enemy sprites
enemyDead = pygame.image.load('e dead.png')
enemyLeft = pygame.image.load('el.png')
enemyL1 = pygame.image.load('el1.png')
enemyL2 = pygame.image.load('el2.png')
enemyL3 = pygame.image.load('el3.png')
enemyL4 = pygame.image.load('el4.png')
enemyL5 = pygame.image.load('el5.png')
enemyL6 = pygame.image.load('el6.png')
enemyL7 = pygame.image.load('el7.png')
enemyL8 = pygame.image.load('el8.png')
enemyLeftAttack = [enemyL1, enemyL2, enemyL3, enemyL4, enemyL5, enemyL6, enemyL7, enemyL8, enemyLeft]
enemyRight = pygame.image.load('er.png')
enemyR1 = pygame.image.load('er1.png')
enemyR2 = pygame.image.load('er2.png')
enemyR3 = pygame.image.load('er3.png')
enemyR4 = pygame.image.load('er4.png')
enemyR5 = pygame.image.load('er5.png')
enemyR6 = pygame.image.load('er6.png')
enemyR7 = pygame.image.load('er7.png')
enemyR8 = pygame.image.load('er8.png')
enemyRightAttack = [enemyR1, enemyR2, enemyR3, enemyR4, enemyR5, enemyR6, enemyR7, enemyR8, enemyRight]
# Weapon sprites and names (must be in tuple format: (sprite, name))
swordT1 = (pygame.image.load('st1.png'), "sword (T1)")
swordT2 = (pygame.image.load('st2.png'), "sword (T2)")
swordT3 = (pygame.image.load('st3.png'), "sword (T3)")
swordT4 = (pygame.image.load('st4.png'), "sword (T4)")
swordT5 = (pygame.image.load('st5.png'), "sword (T5)")
swordT6 = (pygame.image.load('st6.png'), "sword (T6)")
bluePotion = (pygame.image.load('blue potion.png'), "blue potion")
greenPotion = (pygame.image.load('green potion.png'), "green potion")
redPotion = (pygame.image.load('red potion.png'), "red potion")
# HUD sprites
heart = pygame.image.load('heart.png')
heartHalf = pygame.image.load('heart (half).png')
inventorySprite = pygame.image.load('inventory slot.png')


# Enemies
attackDistance = 8  # The distance from which an enemy will start moving towards the player
enemyMoveSpeed = 1000  # How many milliseconds it takes for enemies to move a square
enemyDeadSpeed = 4000  # How many milliseconds it takes for enemies to de-spawn

# Player
playerDeadSpeed = 3000  # How quickly it goes to the game over screen after the player has died
playerInventorySize = 5  # The size of the players inventory / what items the player is holding
playerHealthLimit = 20  # The health limit of the player

# Frame rate and display
frameRate = 25
spriteFrames = 2
