import pygame
import sys
import random

pygame.init()

# resolution

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Wars")

# positions for text

menu_text_width = 350
menu_text_height = 30
smaller_text_height = menu_text_height + 75

# colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# fonts

font = pygame.font.SysFont(None, 70)
smaller_font = pygame.font.SysFont(None, 20)
button_font = pygame.font.SysFont(None, 40)
header_font = pygame.font.SysFont(None, 40)  # Font for the header


# Load heart image

heart_image = pygame.image.load('heart.png')  # Replace with the path to your heart image
heart_image = pygame.transform.scale(heart_image, (40, 40))  # Resize heart image

# Load character image

character_image = pygame.image.load('character.png')
character_image = pygame.transform.scale(character_image, (80, 80))

# draw texts

def draw_text(text, font, color, surface, pos):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = pos
    surface.blit(text_obj, text_rect)

# draw buttons

def draw_button(text, font, color, surface, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    text_obj = font.render(text, True, WHITE)
    text_rect = text_obj.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_obj, text_rect)
    return button_rect

# Draw header (score, math problem, lives)
def draw_header(surface, score, problem, lives):

    # Draw score on the left
    draw_text(f'Score: {score:04}', header_font, WHITE, surface, (20, 20))

    # Draw the math problem in the center
    problem_text_width = header_font.size(problem)[0]  # Get width of the problem text
    draw_text(problem, header_font, WHITE, surface, (screen_width // 2 - problem_text_width // 2, 20))

    # Draw hearts (lives) on the right
    for i in range(lives):
        surface.blit(heart_image, (screen_width - (i + 1) * 50, 15))

def draw_character(surface,x_position,y_position):
    surface.blit(character_image, (x_position, y_position))

# Generating questions for level 1
def level_1():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-'])
    problem = f"{num1} {operation} {num2}"
    if operation == '+':
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2
    answers = [correct_answer]
    while len(answers) < 4:
        wrong_answer = random.randint(1, 20)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)
    
    random.shuffle(answers)
    return problem, answers

# Generating questions for level 2
def level_2():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['*', '/'])
    problem = f"{num1} {operation} {num2}"
    if operation == '*':
        correct_answer = num1 * num2
    else:
        correct_answer = num1 // num2 if num2 != 0 else num1  # Avoid division by zero
    answers = [correct_answer]
    while len(answers) < 4:
        wrong_answer = random.randint(1, 20)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)
    
    random.shuffle(answers)
    return problem, answers

# Generating questions for level 3

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
    while len(answers) < 4:
        wrong_answer = random.randint(1, 50)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)
    
    random.shuffle(answers)
    return problem, answers


# game state

MENU = 'menu'
LEVEL_1 = 'level_1'
LEVEL_2 = 'level_2'
LEVEL_3 = 'level_3'
state = MENU  # start at menu

# variables for the game
score = 0  # initial score
problem = ""  # placeholder for the current math problem
answers = []  # placeholder for the answers
lives = 3  # number of lives

# Variáveis do projétil
projectile_color = (255, 0, 0)  # color red
projectile_speed = 1
projectile = None

# velocity
move_speed = 1

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

    # capture key presses
    keys = pygame.key.get_pressed()

    # move the character to the left
    if keys[pygame.K_LEFT]:
        x_position -= move_speed

    # move the character to the right
    if keys[pygame.K_RIGHT]:
        x_position += move_speed

    # move the character to the up
    if keys[pygame.K_UP]:
        y_position -= move_speed

    # move the character to the down
    if keys[pygame.K_DOWN]:
        y_position += move_speed

    # prevent the character from leaving the screen (horizontal)

    if x_position < 0:
        x_position = 0
    elif x_position > screen_width - 80:  # 80 is the width of the character
        x_position = screen_width - 80

    # prevent the character from leaving the screen (vertical)

    if y_position < 80:  # prevents the character from going beyond the header line (80 pixels)
        y_position = 80
    elif y_position > screen_height - 80:  # 80 is the character's height
        y_position = screen_height - 80

    # check if the player pressed SPACE to shoot
    if keys[pygame.K_SPACE] and projectile is None:
        projectile = [x_position, y_position]  # sets the initial position of the projectile

    # draw back screen

    screen.fill(BLACK)

    if state == MENU:
        # draw game name
        menu_text_pos = (menu_text_width, menu_text_height)
        draw_text('MATH WARS', font, WHITE, screen, menu_text_pos)

        # draw smaller texts
        secondary_text_pos = (menu_text_width + 70, smaller_text_height)
        draw_text('ESCOLHA A DIFICULDADE:', smaller_font, WHITE, screen, secondary_text_pos)
        secondary_text_pos_2 = (200, smaller_text_height + 400)
        draw_text('*Nível 1 - Adição e Subtração *Nível 2 - Multiplicação e Divisão *Nível 3 - Expressões Númericas',
                  smaller_font, WHITE, screen, secondary_text_pos_2)

        # draw buttons
        button_width = 100
        button_height = 25
        button_gap = 150

        level1_button = draw_button('NÍVEL 1', button_font, BLACK, screen, 200, 300, button_width, button_height)
        level2_button = draw_button('NÍVEL 2', button_font, BLACK, screen, 200 + button_width + button_gap, 300,
                                    button_width, button_height)
        level3_button = draw_button('NÍVEL 3', button_font, BLACK, screen, 200 + (button_width + button_gap) * 2, 300,
                                    button_width, button_height)

        # detect clicks
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if level1_button.collidepoint(mouse_pos):
                print("Nível 1 selecionado")
                state = LEVEL_1
                problem, answers = level_1()  # generate level 1 problem and answers
            elif level2_button.collidepoint(mouse_pos):
                print("Nível 2 selecionado")
                state = LEVEL_2
                problem, answers = level_2()  # generate level 2 problem and answers
            elif level3_button.collidepoint(mouse_pos):
                print("Nível 3 selecionado")
                state = LEVEL_3
                problem, answers = level_3()  # generate level 3 problem and answer

    elif state == LEVEL_1 or state == LEVEL_2 or state == LEVEL_3:

        # draw the header (score, math problem, lives)
        draw_header(screen, score, problem, lives)
        pygame.draw.line(screen, WHITE, (0, 80), (screen_width, 80), 5)

        draw_character(screen,x_position,y_position)

        # define the positions of the squares
        square_width = 150
        square_height = 100
        square_gap = 100  # spacing between squares
        square_y = screen_height // 4  # centered vertical position

        # calculates the starting position of the first square
        total_width = (square_width * 4) + (square_gap * 3)
        start_x = (screen_width - total_width) // 2

        # list to store answer rectangles
        answer_rects = []
        
        # draw the squares and answers
        for i in range(4):
            square_x = start_x + i * (square_width + square_gap)
            # draw the square for the answer
            square_rect = pygame.Rect(square_x, square_y, square_width, square_height)
            pygame.draw.rect(screen, GRAY, square_rect)

            # render response text inside square
            draw_text(str(answers[i]), button_font, WHITE, screen, (square_x + 20, square_y + 30))

            # stores the rectangle and the response value
            answer_rects.append((square_rect, answers[i]))

        # add a flag to check if lives have already been reduced
        lives_deducted = False

        # if the projectile exists, move it and draw it
        if projectile:
            projectile[1] -= projectile_speed  # move projectile up
            pygame.draw.circle(screen, projectile_color, (projectile[0], projectile[1]), 5)  # Desenhar projétil

            # check if the projectile left the screen
            if projectile[1] < 0:
                projectile = None  # restart the projectile

            # check collision with responses
            for rect, answer in answer_rects:
                if rect.collidepoint(projectile):  # checks if the projectile collides with a response
                    print(f"Acertou a resposta: {answer}")
                    

                    if answer == eval(problem):  
                        score += 10
                        projectile = None

                        if state == LEVEL_1:
                            problem, answers = level_1()
                        elif state == LEVEL_2:
                            problem, answers = level_2()
                        elif state == LEVEL_3:
                            problem, answers = level_3()
                    else:
                        if not lives_deducted:  
                            lives -= 1  
                            lives_deducted = True  
                        projectile = None  

                    break  # to avoid multiple collisions with the same projectile

    # reset flag when projectile is reset or a new issue starts
    if projectile is None:
        lives_deducted = False  # reset flag
           
                
    if lives <= 0:
        running = False  

    pygame.display.flip()

pygame.quit()
