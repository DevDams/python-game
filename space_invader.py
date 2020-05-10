"""
A Python Game Project build with Pygame
I create my own player, enemy, background and bullet for this game

"""

import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Game background
background = pygame.image.load('background.png')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Ennemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 9

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.8)
    enemyY_change.append(6.8)

# Bullet
# Ready - mean you can't see the bullet yet
# Fire - the bullet is shooting
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
over_text = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (2, 255, 2))
    screen.blit(score, (x, y))

def game_over():
    over = over_text.render("Game Over", True, (0, 0, 0))
    screen.blit(over, (250, 205))

def player(x, y):
    screen.blit(playerImg, (playerX, playerY)) # blit mean : to draw

def enemy(x, y, i):
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # Color of the window
    screen.fill((119, 179, 212))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Get the current X cordinate of the player
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # To make the player move
    playerX += playerX_change

    # Prevent the player go out of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Shoot multiple bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy movement
    # To make the enemy move
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
               enemyY[j] = 2000 
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] += 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] -= 1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
