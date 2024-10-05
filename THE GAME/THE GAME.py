import pygame
import sys
import random

pygame.init()

# resolution

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Wars")

# text positions

menu_text_width = 350
menu_text_height = 30
smaller_text_height = menu_text_height + 75

# colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BROWN = (116, 97, 79)

# fonts

font = pygame.font.SysFont(None, 70)
font2 = pygame.font.Font(None, 50)
font3 = pygame.font.Font(None, 25)
smaller_font = pygame.font.SysFont(None, 20)
button_font = pygame.font.SysFont(None, 40)
score_and_time_font = pygame.font.SysFont(None, 10)

# sounds

paddle_sound = pygame.mixer.Sound('sounds/paddle.wav')
pygame.mixer.music.load('sounds/megaman - soundtrack.mp3')
pygame.mixer.music.play(-1)

# upload images

heart_image = pygame.image.load('img/heart.png')
heart_image = pygame.transform.scale(heart_image, (40, 40))
character_image = pygame.image.load('img/character.png')
character_image = pygame.transform.scale(character_image, (60, 60))
character_image_up = pygame.image.load('img/character_up.png')
character_image_up = pygame.transform.scale(character_image_up, (60, 60))
character_image_down = pygame.image.load('img/character_down.png')
character_image_down = pygame.transform.scale(character_image_down, (60, 60))
background_image = pygame.image.load("img/background_image.png")
lvl_img = pygame.image.load('img/lvl.jpg')


# draw texts

def draw_text(text, font, color, surface, pos):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = pos
    surface.blit(text_obj, text_rect)


def draw_button(text, font, color, surface, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    text_obj = font.render(text, True, WHITE)
    text_rect = text_obj.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_obj, text_rect)
    return button_rect

def draw_answer(surface, text, font, color, x, y):
    answer_surface = pygame.Surface((50, 40), pygame.SRCALPHA)
    text_surface = font.render(str(text), True, color)

    text_rect = text_surface.get_rect(center=(25, 20))

    answer_surface.blit(text_surface, text_rect)

    surface.blit(answer_surface, (x, y))
    pygame.draw.rect(surface, WHITE, (x, y, 50, 40), 3)


def draw_header(surface, score, problem, lives):
    draw_text(f'{score:01}', font, WHITE, surface, (40, 15))
    draw_text(f'score:', smaller_font, WHITE, surface, (1, 1))
    draw_text(f'time:', smaller_font, WHITE, surface, (87, 1))
    problem_text_width = font.size(problem)[0]
    draw_text(problem, font, WHITE, surface,
              (screen_width // 2 - problem_text_width // 2, 10))
    for i in range(lives):
        surface.blit(heart_image, (990 - (i + 1) * 50, 15))


def draw_character(surface, x_position, y_position, image):
    surface.blit(image, (x_position, y_position))

# function for draw the time


def draw_timer(surface, time_left):
    minutes = time_left // 60000
    seconds = (time_left % 60000) // 1000
    timer_text = f"{minutes}:{seconds:02}"
    draw_text(timer_text, font, WHITE, surface, (120, 15))


# random positions to answers

def generate_random_positions(num_answers, square_width, square_height, screen_width, screen_height, square_gap):
    positions = []
    while len(positions) < num_answers:
        x = random.randint(70, screen_width - 70)
        y = random.randint(105, screen_height - 50)
        new_position = (x, y)
        if not (400 < x < 600 and 400 < y < 600):
            if all(not (abs(new_position[0] - pos[0]) < square_width + square_gap and
                        abs(new_position[1] - pos[1]) < square_height + square_gap) for pos in positions):
                positions.append(new_position)

    return positions


def level_1():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-'])
    problem = f"({num1} {operation} {num2})"
    if operation == '+':
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2
    answers = [correct_answer]

    while len(answers) < 13:
        wrong_answer = random.randint(1, 20)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)

    random.shuffle(answers)
    return problem, answers


def level_2():
    operation = random.choice(['*', '/'])
    if operation == '*':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        problem = f"({num1} {operation} {num2})"
        correct_answer = num1 * num2
    else:
        num2 = random.randint(1, 10)
        num1 = num2 * random.randint(1, 10)
        problem = f"({num1} {operation} {num2})"
        correct_answer = num1 // num2
    answers = [correct_answer]

    while len(answers) < 13:
        wrong_answer = random.randint(1, 20)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)

    random.shuffle(answers)
    return problem, answers


def level_3():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    num3 = random.randint(1, 10)
    operation1 = random.choice(['+', '-', '*'])
    operation2 = random.choice(['+', '-', '*'])
    problem = f"({num1} {operation1} {num2}) {operation2} {num3}"
    if operation1 == '+':
        result1 = num1 + num2
    elif operation1 == '-':
        result1 = num1 - num2
    else:
        result1 = num1 * num2
    if operation2 == '+':
        correct_answer = result1 + num3
    elif operation2 == '-':
        correct_answer = result1 - num3
    else:
        correct_answer = result1 * num3
    answers = [correct_answer]

    while len(answers) < 13:
        wrong_answer = random.randint(1, 50)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)

    random.shuffle(answers)
    return problem, answers

# check if the character collided with any blocks

def check_collision_with_blocks(character_rect, answer_rects):
    for rect, _ in answer_rects:
        if character_rect.colliderect(rect):
            return rect
    return None

# game status


MENU = 'menu'
LEVEL_1 = 'level_1'
LEVEL_2 = 'level_2'
LEVEL_3 = 'level_3'
VICTORY = 'victory'
GAME_OVER = 'game_over'
state = MENU

# game variables

score = 0
lives = 3
problem = ""
answers = []
positions = []
move_speed = 0.3
start_time = pygame.time.get_ticks()
time_limit = 60000
time_left = time_limit

# projectile variables

projectile_color = RED
projectile_speed = 1
projectile = None
projectile_fired_direction = None
character_image_current = character_image
projectile_direction = 1
projectile_vertical_direction = 0

# character's starting position

x_position = 500
y_position = 500

# game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    lives_deducted = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_position -= move_speed
        character_image_current = pygame.transform.flip(character_image, True, False)
        projectile_direction = -1
        projectile_vertical_direction = 0
    if keys[pygame.K_RIGHT]:
        x_position += move_speed
        character_image_current = character_image
        projectile_direction = 1
        projectile_vertical_direction = 0
    if keys[pygame.K_UP]:
        y_position -= move_speed
        character_image_current = character_image_up
        projectile_direction = 0
        projectile_vertical_direction = -1
    if keys[pygame.K_DOWN]:
        y_position += move_speed
        character_image_current = character_image_down
        projectile_direction = 0
        projectile_vertical_direction = 1

    # prevent the character from leaving the screen (horizontal)

    if x_position < 0:
        x_position = 0
    elif x_position > screen_width - 60:
        x_position = screen_width - 60

    # prevent the character from leaving the screen (vertical)

    if y_position < 70:
        y_position = 70
    elif y_position > screen_height - 60:
        y_position = screen_height - 60

    # check if the player pressed SPACE to shoot

    if keys[pygame.K_SPACE] and projectile is None:

        # projectile's initial position

        projectile = [x_position + 35, y_position + 35]
        projectile_fired_direction = projectile_direction
        projectile_vertical_direction = projectile_vertical_direction
        pygame.time.delay(150)

    # calculates the character's rectangle to check collision

    character_rect = pygame.Rect(x_position, y_position, 40, 40)

    if state == MENU:
        screen.blit(background_image, (0, 0))
    elif state == LEVEL_1 or state == LEVEL_2 or state == LEVEL_3:
        screen.blit(lvl_img, (0, 0))

    if state == MENU:

        # upload images

        screen.blit(background_image, (0, 0))

        # draw menu interface

        menu_text_pos = (menu_text_width, menu_text_height)
        secondary_text_pos = (menu_text_width + 70, smaller_text_height)
        draw_text('ESCOLHA A DIFICULDADE:', smaller_font,
                  WHITE, screen, secondary_text_pos)
        secondary_text_pos_2 = (200, smaller_text_height + 410)
        draw_text(
            '*Nível 1 - Adição e Subtração *Nível 2 - Multiplicação e Divisão *Nível 3 - Expressões Númericas',
            smaller_font, WHITE, screen, secondary_text_pos_2)

        # draw buttons

        button_width = 150
        button_height = 50
        button_gap = 50

        level1_button = draw_button('NÍVEL 1', button_font, BROWN, screen, 235, 295, button_width,
                                    button_height)
        level2_button = draw_button('NÍVEL 2', button_font, BROWN, screen, 235 + button_width + button_gap,
                                    295, button_width, button_height)
        level3_button = draw_button('NÍVEL 3', button_font, BROWN, screen, 235 + (button_width + button_gap) * 2,
                                    295, button_width, button_height)

        # detect clicks

        mouse_pos = pygame.mouse.get_pos()

        # detect level and generate random positions to answers

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if level1_button.collidepoint(mouse_pos):
                state = LEVEL_1
                problem, answers = level_1()
                positions = generate_random_positions(13, 30, 20, screen_width,
                                                      screen_height, 70)
                start_time = pygame.time.get_ticks()
            elif level2_button.collidepoint(mouse_pos):
                state = LEVEL_2
                problem, answers = level_2()
                positions = generate_random_positions(13, 30, 20, screen_width,
                                                      screen_height, 70)
                start_time = pygame.time.get_ticks()
            elif level3_button.collidepoint(mouse_pos):
                state = LEVEL_3
                problem, answers = level_3()
                positions = generate_random_positions(13, 30, 20, screen_width,
                                                      screen_height, 70)
                start_time = pygame.time.get_ticks()

    elif state == LEVEL_1 or state == LEVEL_2 or state == LEVEL_3:

        # update the timer

        current_time = pygame.time.get_ticks()
        time_left = time_limit - (current_time - start_time)

        if time_left <= 0:
            state = 'victory'

        # draw level interface

        draw_timer(screen, time_left)
        draw_header(screen, score, problem, lives)
        pygame.draw.line(screen, WHITE, (0, 70), (screen_width, 70), 1)
        draw_character(screen, x_position, y_position, character_image_current)

        # stock answers

        answer_rects = []

        # draw answers

        for i in range(13):
            square_x, square_y = positions[i]
            square_rect = pygame.Rect(square_x, square_y, 50, 40)
            draw_answer(screen, answers[i], button_font, WHITE, square_x, square_y)
            text_surface = button_font.render(str(answers[i]), True, WHITE)
            text_rect = text_surface.get_rect(center=square_rect.center)
            screen.blit(text_surface, text_rect)
            answer_rects.append((square_rect, answers[i]))

        # checks collision between the character and the blocks

        collided_block = check_collision_with_blocks(character_rect, answer_rects)
        if collided_block:
            if keys[pygame.K_RIGHT]:
                x_position = collided_block.left - character_rect.width
            elif keys[pygame.K_LEFT]:
                x_position = collided_block.right
            if keys[pygame.K_DOWN]:
                y_position = collided_block.top - character_rect.height
            elif keys[pygame.K_UP]:
                y_position = collided_block.bottom

        # confer number of lives

        lives_deducted = False

        # draw projectiles and assigns functions

        if projectile is not None:
            pygame.draw.circle(screen, projectile_color, projectile, 5)
            if projectile_fired_direction == 1:  # shoot to right
                projectile[0] += projectile_speed
            elif projectile_fired_direction == -1:  # shoot to left
                projectile[0] -= projectile_speed
            elif projectile_vertical_direction == -1:  # up shoot
                projectile[1] -= projectile_speed
            elif projectile_vertical_direction == 1:  # down shoot
                projectile[1] += projectile_speed

            # checks if the projectile goes wrong

            if projectile[1] < 0:
                projectile = None

            elif projectile[1] > screen_width:
                projectile = None

            elif projectile[0] < 0 or projectile[0] > screen_width:
                projectile = None

            # check colision with answers

            for rect, answer in answer_rects:
                if projectile is not None and rect.collidepoint(projectile[0], projectile[1]):
                    paddle_sound.play()
                    if answer == eval(problem):
                        score += 1
                        projectile = None
                        if state == LEVEL_1:
                            problem, answers = level_1()
                            projectile = None
                            pygame.time.delay(100)
                        elif state == LEVEL_2:
                            problem, answers = level_2()
                            projectile = None
                            pygame.time.delay(100)
                        elif state == LEVEL_3:
                            problem, answers = level_3()
                            projectile = None
                            pygame.time.delay(100)
                        # generate new positions only if the projectile collides with a correct answer

                        positions = generate_random_positions(
                            15, 30, 20, screen_width, screen_height, 70)
                        x_position = 500
                        y_position = 500
                    else:
                        if not lives_deducted:
                            lives -= 1
                            lives_deducted = True

                        # remove the projectile to don't remove too many lives

                        projectile = None
                    break

    # reset flag when projectile is reset or a new issue starts

    if projectile is None:
        lives_deducted = False

    if lives <= 0:
        running = False
        state = GAME_OVER

    # print victory on screen

    if state == GAME_OVER:
        screen.fill(BLACK)
        game_over_text = font2.render("Boa Tentativa!", True, WHITE)
        score_text = font3.render(f"Acertou {score} perguntas!", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 -
                    game_over_text.get_width() // 2, 280))
        screen.blit(score_text, (screen_width // 2 -
                    score_text.get_width() // 2, 320))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    # print game on screen

    elif state == VICTORY:
        screen.fill(BLACK)
        victory_text = font2.render("Parabéns! Você resistiu bravamente!", True, WHITE)
        score_text = font3.render(f"Acertou {score} perguntas!", True, WHITE)
        screen.blit(victory_text, (screen_width // 2 -
                    victory_text.get_width() // 2, 280))
        screen.blit(score_text, (screen_width // 2 -
                    score_text.get_width() // 2, 320))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()

pygame.quit()
