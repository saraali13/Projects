import sys
import time
import pygame
import random

pygame.init()
color = (119, 118, 110)
dis_w = 800
dis_h = 600
game_dis = pygame.display.set_mode((dis_w, dis_h))  # height and width of the screen
pygame.display.set_caption("Car Game")
clock = pygame.time.Clock()  # for interval control

# Load car image
car_1 = pygame.image.load("car1.png")
car_w1 = car_1.get_width()  # Get car image width
car_h1 = car_1.get_height()  # Get car image height
# New dimensions for the car
resized_car_width1 = 70  # Desired width
resized_car_height1 = int((resized_car_width1 / car_w1) * car_h1)  # Scale height proportionally

car_1 = pygame.transform.scale(car_1, (resized_car_width1, resized_car_height1))
car_2 = pygame.image.load("car2.png")
car_2 = pygame.transform.scale(car_2, (60, int((60 / car_2.get_width()) * car_2.get_height())))
car_3 = pygame.image.load("car3.png")
car_3 = pygame.transform.scale(car_3, (60, int((60 / car_3.get_width()) * car_3.get_height())))
car_4 = pygame.image.load("car4.png")
car_4 = pygame.transform.scale(car_4, (60, int((60 / car_4.get_width()) * car_4.get_height())))
car_5 = pygame.image.load("car5.png")
car_5 = pygame.transform.scale(car_5, (60, int((60 / car_5.get_width()) * car_5.get_height())))
car_6 = pygame.image.load("car6.png")
car_6 = pygame.transform.scale(car_6, (60, int((60 / car_6.get_width()) * car_6.get_height())))

# Gap from the bottom
gap = 2  # Adjust this value for spacing from the bottom

road_background = pygame.image.load("road_.PNG")
road_background = pygame.transform.scale(road_background,
                                         ((road_background.get_width()) + 130, (road_background.get_height()) + 160))
grass_background = pygame.image.load("grass-background.jpg")
grass_background = pygame.transform.scale(grass_background, (100, grass_background.get_height()))

bg = pygame.image.load("bg.PNG")


def intro():
    intro_active = True
    while intro_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game_dis.blit(bg, (0, 0))
        font = pygame.font.SysFont(None, 130)
        text = font.render("Car Game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(400, 100))
        game_dis.blit(text, text_rect)

        button("Start", 150, 520, 100, 50, (0, 200, 0), (0, 255, 0), "play")
        button("Quit", 550, 520, 100, 50, (200, 0, 0), (255, 0, 0), "quit")
        pygame.display.update()
        clock.tick(50)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(game_dis, ic, (x, y, w, h))
    small_text = pygame.font.Font("freesansbold.ttf", 20)
    text_surf = small_text.render(msg, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + (w / 2), y + (h / 2)))
    game_dis.blit(text_surf, text_rect)


def background():
    game_dis.blit(grass_background, (0, 0))
    game_dis.blit(grass_background, (700, 0))
    game_dis.blit(road_background, (500, 0))


def car(x, y):  # x and y are the coordinates to place the car
    game_dis.blit(car_1, (x, y))


def obstacle(obs_x, obs_y, obs):
    obs_pic = car_4
    if obs == 0:
        obs_pic = car_2
    elif obs == 1:
        obs_pic = car_3
    elif obs == 2:
        obs_pic = car_4
    elif obs == 3:
        obs_pic = car_5
    elif obs == 4:
        obs_pic = car_6

    game_dis.blit(obs_pic, (obs_x, obs_y))  # Use the correct obstacle image


def score_cal(obj, score, level):
    font = pygame.font.SysFont(None, 50)
    level = font.render("Level: " + str(level), True, (255, 255, 255))
    passed_cars = font.render("Passed: " + str(obj), True, (0, 0, 0))
    score = font.render("Score: " + str(score), True, (0, 255, 0))
    game_dis.blit(level, (10, 10))
    game_dis.blit(passed_cars, (10, 50))
    game_dis.blit(score, (10, 90))


def crash():
    large_text = pygame.font.SysFont(None, 80)
    text_surface = large_text.render("Car Crashed", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(dis_w / 2, dis_h / 2))
    game_dis.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(2)
    intro()


def game_loop():
    x = (dis_w - resized_car_width1) / 2
    y = dis_h - resized_car_height1 - gap
    x_change = 0
    y_change = 0

    obstacle_ = random.randint(0, 4)
    obstacle_speed = 15
    obs_width = 70
    obs_height = resized_car_height1
    obs_start_x = random.randint(110, dis_w - 110)
    obs_start_y = -750

    level = 1
    score = 0
    passed = 0

    bgy = 7
    bumped = False

    while not bumped:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    x_change = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    y_change = 0

        x += x_change
        y += y_change

        # Restrict movement within bounds
        if x < 110:
            x = 110
        elif x > 680 - resized_car_width1:
            x = 680 - resized_car_width1
        if y < 0:
            y = 0
        elif y > dis_h - resized_car_height1:
            y = dis_h - resized_car_height1

        game_dis.fill(color)

        bgy += obstacle_speed / 2  # Update the scrolling position
        bgy1 = bgy % road_background.get_rect().height  # Wrap around when the background scrolls out

        # Draw the scrolling grass and road backgrounds
        game_dis.blit(grass_background, (0, bgy1 - grass_background.get_rect().height))
        game_dis.blit(grass_background, (700, bgy1 - grass_background.get_rect().height))
        game_dis.blit(grass_background, (0, bgy1))
        game_dis.blit(grass_background, (700, bgy1))
        game_dis.blit(road_background, (135, bgy1 - road_background.get_rect().height))
        game_dis.blit(road_background, (135, bgy1))

        obs_start_y += obstacle_speed
        obstacle(obs_start_x, obs_start_y, obstacle_)

        car(x, y)
        score_cal(passed, score, level)
        if obs_start_y > dis_h:
            obs_start_y = -obs_height
            obs_start_x = random.randint(170, dis_w - 170)
            obstacle_ = random.randint(0, 4)
            passed += 1
            score += 10

            if passed % 10 == 0:
                level += 1
                obstacle_speed += 3
                bgy += obstacle_speed / 2
       
        if y < obs_start_y + obs_height-50:
            if x > obs_start_x and x < obs_start_x + obs_width or x + resized_car_width1 > obs_start_x and x + resized_car_width1 < obs_start_x + obs_width:
                crash()

        pygame.display.update()
        clock.tick(60)


intro()
pygame.quit()
quit()
