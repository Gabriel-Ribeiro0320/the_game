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

# fonts

font = pygame.font.SysFont(None, 70)
smaller_font = pygame.font.SysFont(None, 20)
button_font = pygame.font.SysFont(None, 40)

# upload images

heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (40, 40))
character_image = pygame.image.load('character.png')
character_image = pygame.transform.scale(character_image, (60, 60))

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


def draw_header(surface, score, problem, lives):
    draw_text(f'{score:01}', font, WHITE, surface, (20, 15))
    problem_text_width = font.size(problem)[0]
    draw_text(problem, font, WHITE, surface, (screen_width // 2 - problem_text_width // 2, 10))
    for i in range(lives):
        surface.blit(heart_image, (990 - (i + 1) * 50, 15))


def draw_character(surface, x_position, y_position):
    surface.blit(character_image, (x_position, y_position))


# random positions to answers

def generate_random_positions(num_answers, square_width, square_height, screen_width, screen_height, square_gap):
    positions = []
    while len(positions) < num_answers:
        x = random.randint(70, screen_width - 70)
        y = random.randint(105, screen_height - 50)
        new_position = (x, y)
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

    while len(answers) < 15:
        wrong_answer = random.randint(1, 20)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)

    random.shuffle(answers)
    return problem, answers


def level_2():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['*', '/'])
    problem = f"({num1} {operation} {num2})"
    if operation == '*':
        correct_answer = num1 * num2
    else:
        correct_answer = num1 // num2 if num2 != 0 else num1
    answers = [correct_answer]

    while len(answers) < 15:
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

    while len(answers) < 15:
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
state = MENU

# game variables

score = 0
lives = 3
problem = ""
answers = []
positions = []
move_speed = 0.5

# projectile variables

projectile_color = RED
projectile_speed = 1
projectile = None

# character's starting position

x_position = screen_width // 2
y_position = 500

# game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_position -= move_speed
    if keys[pygame.K_RIGHT]:
        x_position += move_speed
    if keys[pygame.K_UP]:
        y_position -= move_speed
    if keys[pygame.K_DOWN]:
        y_position += move_speed

    # prevent the character from leaving the screen (horizontal)

    if x_position < 0:
        x_position = 0
    elif x_position > screen_width - 80:
        x_position = screen_width - 80

    # prevent the character from leaving the screen (vertical)

    if y_position < 80:
        y_position = 80
    elif y_position > screen_height - 80:
        y_position = screen_height - 80

    # check if the player pressed SPACE to shoot

    if keys[pygame.K_SPACE] and projectile is None:

        # projectile's initial position

        projectile = [x_position + 60, y_position+30]

    # calculates the character's rectangle to check collision
    character_rect = pygame.Rect(x_position, y_position, 60, 60)

    # clear screen

    screen.fill(BLACK)

    if state == MENU:

        # draw menu interface

        menu_text_pos = (menu_text_width, menu_text_height)
        draw_text('MATH WARS', font, WHITE, screen, menu_text_pos)
        secondary_text_pos = (menu_text_width + 70, smaller_text_height)
        draw_text('ESCOLHA A DIFICULDADE:', smaller_font, WHITE, screen, secondary_text_pos)
        secondary_text_pos_2 = (200, smaller_text_height + 400)
        draw_text(
            '*Nível 1 - Adição e Subtração *Nível 2 - Multiplicação e Divisão *Nível 3 - Expressões Númericas',
            smaller_font, WHITE, screen, secondary_text_pos_2)

        # draw buttons

        button_width = 150
        button_height = 50
        button_gap = 50

        level1_button = draw_button('NÍVEL 1', button_font, BLACK, screen, 200, 300, button_width,
                                    button_height)
        level2_button = draw_button('NÍVEL 2', button_font, BLACK, screen, 200 + button_width + button_gap,
                                    300, button_width, button_height)
        level3_button = draw_button('NÍVEL 3', button_font, BLACK, screen, 200 + (button_width + button_gap) * 2,
                                    300, button_width, button_height)

        # detect clicks

        mouse_pos = pygame.mouse.get_pos()

        # detect level and generate random positions to answers

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if level1_button.collidepoint(mouse_pos):
                state = LEVEL_1
                problem, answers = level_1()
                positions = generate_random_positions(15, 30, 20, screen_width,
                                                      screen_height, 70)
            elif level2_button.collidepoint(mouse_pos):
                state = LEVEL_2
                problem, answers = level_2()
                positions = generate_random_positions(15, 30, 20, screen_width,
                                                      screen_height, 70)
            elif level3_button.collidepoint(mouse_pos):
                state = LEVEL_3
                problem, answers = level_3()
                positions = generate_random_positions(15, 30, 20, screen_width,
                                                      screen_height, 70)

    elif state == LEVEL_1 or state == LEVEL_2 or state == LEVEL_3:

        # draw level interface

        draw_header(screen, score, problem, lives)
        pygame.draw.line(screen, WHITE, (0, 70), (screen_width, 70), 1)
        draw_character(screen, x_position, y_position)

        # stock answers

        answer_rects = []

        # draw answers

        for i in range(15):
            square_x, square_y = positions[i]
            square_rect = pygame.Rect(square_x, square_y, 60, 40)
            pygame.draw.rect(screen, BLACK, square_rect)
            text_surface = button_font.render(str(answers[i]), True, WHITE)
            text_rect = text_surface.get_rect(center=square_rect.center)
            screen.blit(text_surface, text_rect)
            answer_rects.append((square_rect, answers[i]))

        # checks collision between the character and the blocks

        collided_block = check_collision_with_blocks(character_rect, answer_rects)
        if collided_block:
            if keys[pygame.K_RIGHT] and character_rect.right > collided_block.left:
                x_position = collided_block.left - character_rect.width 

            elif keys[pygame.K_LEFT] and character_rect.left < collided_block.right:
                x_position = collided_block.right 
                
            if keys[pygame.K_DOWN] and character_rect.bottom > collided_block.top:
                y_position = collided_block.top - character_rect.height  
                
            elif keys[pygame.K_UP] and character_rect.top < collided_block.bottom:
                y_position = collided_block.bottom 

        # confer number of lives

        lives_deducted = False

        # draw projectiles and assigns functions

        if projectile is not None:
            projectile[0] += projectile_speed
            pygame.draw.circle(screen, projectile_color, (projectile[0], projectile[1]), 5)

            # checks if the projectile goes wrong

            if projectile[1] > screen_width:
                projectile = None

            if projectile[0] < 0 or projectile[0] > screen_width:
                projectile = None  


            # check colision with answers

            for rect, answer in answer_rects:
                if projectile is not None and rect.collidepoint(projectile[0], projectile[1]):
                    if answer == eval(problem):
                        score += 10
                        projectile = None
                        if state == LEVEL_1:
                            problem, answers = level_1()
                        elif state == LEVEL_2:
                            problem, answers = level_2()
                        elif state == LEVEL_3:
                            problem, answers = level_3()

                        # generate new positions only if the projectile collides with a correct answer

                        positions = generate_random_positions(15, 30, 20,
                                                              screen_width, screen_height, 70)

                    else:
                        if not lives_deducted:
                            lives -= 1
                            lives_deducted = True
                        projectile = None

                    break

    # reset flag when projectile is reset or a new issue starts

    if projectile is None:
        lives_deducted = False

    if lives <= 0:
        running = False

    pygame.display.flip()

pygame.quit()
