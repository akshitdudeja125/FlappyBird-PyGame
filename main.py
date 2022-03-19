import time
import pygame
import random
import os
import sys
import math
from pygame import mixer

screen_dimensions = (1280, 720)
player_size = (70, 70)
obstacle_size = (480, 900)
speed_background = 3

pygame.init()

screen = pygame.display.set_mode(screen_dimensions)

# CAPTION AND ICON
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# BACKGROUND
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, screen_dimensions)

# BACKGROUND SOUND
# mixer.music.load("Background.mpeg")
# mixer.music.play(-1)

# Lower Part
lower_part = pygame.image.load('lower_part.png')
lower_part = pygame.transform.scale(lower_part, (1280, 70))
lower_part_X = 0

lower_part_2 = pygame.image.load('lower_part.png')
lower_part_2 = pygame.transform.scale(lower_part, (1280, 70))
lower_part_2_X = 1280

lower_part_change = -speed_background

# BIRD
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, player_size)

player_up = pygame.image.load('player_up.png')
player_up = pygame.transform.scale(player_up, player_size)

player_down = pygame.image.load('player_down.png')
player_down = pygame.transform.scale(player_down, player_size)

player_down_killed = pygame.transform.rotate(player_down, -90)
player_up_killed = pygame.transform.rotate(player_up, -90)


player_X = 200
player_Y = 360

player_Y_change = 3

# OBSTACLES
obstacle_upper = pygame.image.load('obstacle_upper.png')
obstacle_upper = pygame.transform.scale(obstacle_upper, obstacle_size)

obstacle_lower = pygame.transform.rotate(obstacle_upper, 180)

obstacle_change = -speed_background

obstacle_X = [300, 650, 1000, 1350]

obstacle_upper_Y = [random.randint(-820, -520) for i in range(4)]
obstacle_lower_Y = [1100-abs(i) for i in obstacle_upper_Y]

# FONT
font = pygame.font.Font('FONTS/sweet_kiss/Sweet Kiss.ttf', 200)
font2 = pygame.font.Font('FONTS/sweet_kiss/Sweet Kiss.ttf', 75)
font_score = pygame.font.Font('Minecraft.ttf', 50)

# SCORE
score = 0
highest_score = 0
score_coordinates = (600, 10)
score_coordinates_killed = (500, 330)
score_Img = pygame.image.load("Score.png")

score_text_coordinates = (555, 365)
best_score_text_coordinates = (675, 365)

# End Game
end_game = pygame.image.load('end_game.png')
end_game = pygame.transform.scale(end_game, (400, 100))
end_game_X = 430
end_game_Y = 200
end_game_change = -3

play_again_coordinates = (150, 520)

score_added = False
attempt_no=1
is_Collision = False
flap = 0
restarter=0
restart_status=False
sound_played = 0
game_started=False
run_state = True
killed = False
while run_state:
    # Filling Screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # Score Comparision
    
    if score > highest_score:
        highest_score = score

    # Player
    if killed == False:
        if flap in range(0, 6):
            player = player_up
        elif flap in range(6, 11):
            player = player_down
        else:
            flap = -1
    else:
        if flap in range(0, 6):
            player = player_up_killed
        elif flap in range(6, 11):
            player = player_down_killed
        else:
            flap = -1
    flap += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_state = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if killed == False:
                    mixer.Sound("jump.mpeg").play()
                    player_Y_change = -12

        if event.type == pygame.KEYUP:
            if killed == False:
                player_Y_change = 7

    if player_Y <= -10:
        player_Y = -10
        player_Y_change = 3
    if player_Y > 600:
        killed = True
        player = player_down
        player_Y = 600

    if end_game_X <= -30 or end_game_X > 900:
        end_game_change = -end_game_change

    player_Y += player_Y_change
    screen.blit(player, (player_X, player_Y))

    # Obstacle Movement
    for i in range(len(obstacle_X)):
        if obstacle_X[i] <= -300:
            obstacle_X[i] = 1080
            score_added = False
            is_Collision = False
            obstacle_upper_Y[i] = random.randint(-820, -520)
            obstacle_lower_Y[i] = 1100-abs(obstacle_upper_Y[i])
        obstacle_X[i] += obstacle_change
        screen.blit(obstacle_upper, (obstacle_X[i], obstacle_upper_Y[i]))
        screen.blit(obstacle_lower, (obstacle_X[i], obstacle_lower_Y[i]))

        # Collision
        if is_Collision == False:
            if obstacle_X[i] in range(-67, 53):
                if player_Y not in range(obstacle_upper_Y[i]+885, obstacle_lower_Y[i]-60):
                    is_Collision = True
            elif obstacle_X[i] < -67 and score_added == False:
                score += 1
                if score % 5 == 0:
                    obstacle_change -= 1
                    lower_part_change -= 1
                score_added = True
        else:
            if sound_played == 1:
                mixer.Sound("coll2.mpeg").play()
            elif sound_played == 50:
                mixer.Sound("coll.mpeg").play()
            sound_played += 1
            killed = True

    # Lower Part Movement
    screen.blit(lower_part, (lower_part_X, 660))
    lower_part_X += lower_part_change
    screen.blit(lower_part_2, (lower_part_2_X, 660))
    lower_part_2_X += lower_part_change
    if lower_part_X <= -1280:
        lower_part_X = 0
        lower_part_2_X = 1280

    # Score
    if killed:
        if flap in range(0, 6):
            screen.blit(end_game, (end_game_X, end_game_Y))
            if flap > 10:
                flap = 0
        player_Y_change = 7
        lower_part_change = 0
        obstacle_change = 0
        for i in range(len(obstacle_X)):
            obstacle_X[i] = 2000
        play_again = font_score.render('press "QUIT" to quit or "WAIT" for restart', True, (0, 0, 0))
        screen.blit(play_again, play_again_coordinates)
        screen.blit(score_Img, (score_coordinates_killed))
        sc = font_score.render(str(score), True, (0, 0, 0))
        screen.blit(sc, score_text_coordinates)
        bsc = font_score.render(str(highest_score), True, (0, 0, 0))
        screen.blit(bsc, best_score_text_coordinates)
        end_game_X += end_game_change
    else:
        sc = font.render(str(score), True, (0, 0, 0))
        screen.blit(sc, score_coordinates)

    # GAME RESTART
    if killed and not restart_status:
        restarter+=1 
    if restarter==200:
        restart_status=True
    if restart_status:
        is_Collision = False   
        killed=False
        restarter=0
        restart_status=False
        player_Y = 360
        obstacle_X = [300, 650, 1000, 1350]
        score = 0
        player_Y_change = 3
        sound_played=0
        speed_background=3
        end_game_change = -3
        obstacle_change = -speed_background
        attempt_no+=1

        if attempt_no>10:
            break


    pygame.display.update()
