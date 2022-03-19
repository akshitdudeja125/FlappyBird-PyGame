import time
import pygame
import random
import keyboard
from pygame import mixer

speed_background = 7

pygame.init()

screen_dimensions = (1280, 720)
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
player_size = (70, 70)

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

player_Y_change = 5

# OBSTACLES
obstacle_size = (480, 900)

obstacle_upper = pygame.image.load('obstacle_upper.png')
obstacle_upper = pygame.transform.scale(obstacle_upper, obstacle_size)

obstacle_lower = pygame.transform.rotate(obstacle_upper, 180)

obstacle_change = -speed_background

obstacle_X = [300, 650, 1000, 1350]

obstacle_upper_Y = [random.randint(-820, -520) for i in range(4)]
obstacle_lower_Y = [1100-abs(i) for i in obstacle_upper_Y]

# FONT
font_score = pygame.font.Font('Minecraft.ttf', 50)
font_score_2 = pygame.font.Font('Minecraft.ttf', 150) 
font_score_3 = pygame.font.Font('Minecraft.ttf', 100)
font_score_4 = pygame.font.Font('Minecraft.ttf', 30)

# SCORE
score = 0
highest_score = 0
score_Img = pygame.image.load("Score.png")

# End Game
end_game = pygame.image.load('end_game.png')
end_game = pygame.transform.scale(end_game, (400, 100))
end_game_X = 430
end_game_Y = 200
end_game_change = -3

# Assigning various variables
attempt_no=1
flap = 0
restarter=0
start_time=time.time()
sound_played = 0
score_added = False
killed = False
restart_status=False
run_state = True
game_started=False
quit_game=False
# Game Loop
while run_state:
    # Filling Screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Score Comparision
    if score > highest_score:
        highest_score = score
    if game_started:
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
            if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE and not killed: 
                        mixer.Sound("jump.mpeg").play()
                        player_Y_change = -12
            if event.type == pygame.KEYUP and not killed:
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
            play_again = font_score.render('press "q" to quit or "r" for restart', True, (0, 0, 0))
            screen.blit(play_again, (195, 480))
            # screen.blit(play_again, (330, 480))
            screen.blit(score_Img, (500, 330))
            sc = font_score.render(str(score), True, (0, 0, 0))
            screen.blit(sc, (555, 365))
            bsc = font_score.render(str(highest_score), True, (0, 0, 0))
            screen.blit(bsc, (675, 365))
            end_game_X += end_game_change
        else:
            sc = font_score_2.render(str(score), True, (0, 0, 0))
            screen.blit(sc, (600, 10))

        # Obstacle Movement
        for i in range(len(obstacle_X)):
            if obstacle_X[i] <= -300:
                obstacle_X[i] = 1080
                score_added = False
                obstacle_upper_Y[i] = random.randint(-820, -520)
                obstacle_lower_Y[i] = 1100-abs(obstacle_upper_Y[i])
            obstacle_X[i] += obstacle_change
            screen.blit(obstacle_upper, (obstacle_X[i], obstacle_upper_Y[i]))
            screen.blit(obstacle_lower, (obstacle_X[i], obstacle_lower_Y[i]))

            # Collision
            if killed == False:
                if obstacle_X[i] in range(-67, 53):
                    if player_Y not in range(obstacle_upper_Y[i]+885, obstacle_lower_Y[i]-60):
                        killed = True
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

        # Lower Part Movement
        screen.blit(lower_part, (lower_part_X, 660))
        lower_part_X += lower_part_change
        screen.blit(lower_part_2, (lower_part_2_X, 660))
        lower_part_2_X += lower_part_change
        if lower_part_X <= -1280:
            lower_part_X = 0
            lower_part_2_X = 1280

        # Game Quit/Restart
        if killed:
            try:
                if keyboard.is_pressed('r'):
                    killed = False   
                    restarter=0
                    restart_status=False
                    player_Y = 360
                    obstacle_X = [300, 650, 1000, 1350]
                    score = 0
                    player_Y_change = 5
                    sound_played=0
                    speed_background=7
                    end_game_change = -3
                    obstacle_change = -speed_background
                    attempt_no+=1
                    # if attempt_no>10:
                    #     break
                if keyboard.is_pressed('q'):
                    run_state=False
                
            except:
                pass
            if quit_game:
                run_state = False
    
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_state = False
        # if time.time()-start_time > 10:
            # game_started = True
        start_screen_text = font_score_3.render('FLAPPY  BIRD', True, (0, 0, 0))
        screen.blit(start_screen_text, (290, 230))
        
        start_screen_text = font_score_4.render('Press "SPACE" to START', True, (0, 0, 0))
        screen.blit(start_screen_text, (450, 430))

        try:
            if keyboard.is_pressed('space'):
                game_started = True
        except:
            pass

    pygame.display.update()