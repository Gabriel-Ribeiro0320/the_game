import pygame
import sys
import random

pygame.init()

# Resolução
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Wars")


# Posições para texto e imagens
menu_text_width = 350
menu_text_height = 30
smaller_text_height = menu_text_height + 75

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Fontes
font = pygame.font.SysFont(None, 70)
smaller_font = pygame.font.SysFont(None, 20)
button_font = pygame.font.SysFont(None, 40)
header_font = pygame.font.SysFont(None, 40)  # Fonte para o cabeçalho

# Carregar imagem do coração
heart_image = pygame.image.load('heart.png')  # Substitua pelo caminho para sua imagem de coração
heart_image = pygame.transform.scale(heart_image, (40, 40))  # Redimensionar imagem de coração

# Carregar imagem do personagem
character_image = pygame.image.load('character.png')  # Substitua pelo caminho para sua imagem de personagem
character_image = pygame.transform.scale(character_image, (80, 80))  # Redimensionar imagem do personagem

# Desenhar textos
def draw_text(text, font, color, surface, pos):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = pos
    surface.blit(text_obj, text_rect)

# Desenhar botões
def draw_button(text, font, color, surface, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    text_obj = font.render(text, True, WHITE)
    text_rect = text_obj.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_obj, text_rect)
    return button_rect

# Desenhar cabeçalho (pontuação, problema matemático, vidas)
def draw_header(surface, score, problem, lives):
    draw_text(f'Score: {score:04}', header_font, WHITE, surface, (20, 20))
    problem_text_width = header_font.size(problem)[0]  # Obter largura do texto do problema
    draw_text(problem, header_font, WHITE, surface, (screen_width // 2 - problem_text_width // 2, 20))
    for i in range(lives):
        surface.blit(heart_image, (screen_width - (i + 1) * 50, 15))

def draw_character(surface, x_position, y_position):
    surface.blit(character_image, (x_position, y_position))


# Gerar problema matemático aleatório e respostas para o Nível 1
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

# Gerar problema matemático aleatório e respostas para o Nível 2
def level_2():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['*', '/'])
    problem = f"{num1} {operation} {num2}"

    if operation == '*':
        correct_answer = num1 * num2
    else:
        correct_answer = num1 // num2 if num2 != 0 else num1  # Evitar divisão por zero

    answers = [correct_answer]

    while len(answers) < 4:
        wrong_answer = random.randint(1, 20)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)
    
    random.shuffle(answers)

    return problem, answers

# Gerar problema matemático aleatório e respostas para o Nível 3
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

# Estados do jogo
MENU = 'menu'
LEVEL_1 = 'level_1'
LEVEL_2 = 'level_2'
LEVEL_3 = 'level_3'
state = MENU  # Começar no menu

# Variáveis do jogo
score = 0  # pontuação inicial
problem = ""  # espaço reservado para o problema matemático atual
answers = []  # espaço reservado para as respostas
lives = 3  # número de vidas

# Variáveis do projétil
projectile_color = (255, 0, 0)  # Cor vermelha
projectile_speed = 10
projectile = None

# Velocidade de movimento
move_speed = 5

# Posição inicial do personagem
x_position = screen_width // 2  # Centralizado horizontalmente
y_position = 500  # Definido mais para baixo na tela

# Loop do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Captura as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Move o personagem para a esquerda
    if keys[pygame.K_LEFT]:
        x_position -= move_speed

    # Move o personagem para a direita
    if keys[pygame.K_RIGHT]:
        x_position += move_speed

    #Move o personagem para cima
    if keys[pygame.K_UP]:
        y_position -= move_speed

    # Move o personagem para baixo
    if keys[pygame.K_DOWN]:
        y_position += move_speed

    # Impedir que o personagem saia da tela (horizontal)
    if x_position < 0:
        x_position = 0
    elif x_position > screen_width - 80:  # 80 é a largura do personagem
        x_position = screen_width - 80

    # Impedir que o personagem saia dos limites da tela (vertical)
    if y_position < 80:  # Impede o personagem de passar da linha de cabeçalho (80 pixels)
        y_position = 80
    elif y_position > screen_height - 80:  # 80 é a altura do personagem
        y_position = screen_height - 80

    # Verificar se o jogador pressionou ESPAÇO para atirar
    if keys[pygame.K_SPACE] and projectile is None:
        projectile = [x_position, y_position]  # Define a posição inicial do projétil

    # Desenhar fundo
    screen.fill(BLACK)

    if state == MENU:
        # Desenhar nome do jogo
        menu_text_pos = (menu_text_width, menu_text_height)
        draw_text('MATH WARS', font, WHITE, screen, menu_text_pos)

        # Desenhar textos menores
        secondary_text_pos = (menu_text_width + 70, smaller_text_height)
        draw_text('ESCOLHA A DIFICULDADE:', smaller_font, WHITE, screen, secondary_text_pos)
        secondary_text_pos_2 = (200, smaller_text_height + 400)
        draw_text('*Nível 1 - Adição e Subtração *Nível 2 - Multiplicação e Divisão *Nível 3 - Expressões Numéricas',
                  smaller_font, WHITE, screen, secondary_text_pos_2)

        # Desenhar botões
        button_width = 100
        button_height = 25
        button_gap = 150

        level1_button = draw_button('NÍVEL 1', button_font, BLACK, screen, 200, 300, button_width, button_height)
        level2_button = draw_button('NÍVEL 2', button_font, BLACK, screen, 200 + button_width + button_gap, 300,
                                    button_width, button_height)
        level3_button = draw_button('NÍVEL 3', button_font, BLACK, screen, 200 + (button_width + button_gap) * 2, 300,
                                    button_width, button_height)

        # Detectar cliques
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if level1_button.collidepoint(mouse_pos):
                print("Nível 1 selecionado")
                state = LEVEL_1
                problem, answers = level_1()  # Gerar problema e respostas
            elif level2_button.collidepoint(mouse_pos):
                print("Nível 2 selecionado")
                state = LEVEL_2
                problem, answers = level_2()  # Gerar problema e respostas
            elif level3_button.collidepoint(mouse_pos):
                print("Nível 3 selecionado")
                state = LEVEL_3
                problem, answers = level_3()  # Gerar problema e respostas

    elif state == LEVEL_1 or state == LEVEL_2 or state == LEVEL_3:
        # Desenhar o cabeçalho (pontuação, problema, vidas)
        draw_header(screen, score, problem, lives)
        pygame.draw.line(screen, WHITE, (0, 80), (screen_width, 80), 5)

        # Desenhar o personagem
        draw_character(screen, x_position, y_position)

        # Definir as posições dos quadrados
        square_width = 150
        square_height = 100
        square_gap = 100  # Espaçamento entre os quadrados
        square_y = screen_height // 4  # Posição vertical centralizada

        # Calcula a posição inicial do primeiro quadrado
        total_width = (square_width * 4) + (square_gap * 3)
        start_x = (screen_width - total_width) // 2

        # Lista para armazenar retângulos de respostas
        answer_rects = []

        # Desenhar os quadrados e as respostas
        for i in range(4):
            square_x = start_x + i * (square_width + square_gap)
            # Desenhar o quadrado para a resposta
            square_rect = pygame.Rect(square_x, square_y, square_width, square_height)
            pygame.draw.rect(screen, GRAY, square_rect)

            # Renderizar o texto da resposta dentro do quadrado
            draw_text(str(answers[i]), button_font, WHITE, screen, (square_x + 20, square_y + 30))

            # Armazena o retângulo e o valor da resposta
            answer_rects.append((square_rect, answers[i]))
        
        # Adiciona uma flag para verificar se já diminuiu vidas
        lives_deducted = False

        # Se o projétil existir, mova-o e desenhe-o
        if projectile:
            projectile[1] -= projectile_speed  # Mover projétil para cima
            pygame.draw.circle(screen, projectile_color, (projectile[0], projectile[1]), 5)  # Desenhar projétil
            # Verificar se o projétil saiu da tela
            if projectile[1] < 0:
                projectile = None  # Reiniciar o projétil
            # Verifica colisão com as respostas
            for rect, answer in answer_rects:
                if rect.collidepoint(projectile):  # Verifica se o projétil colide com uma resposta
                    print(f"Acertou a resposta: {answer}")
                    

                    if answer == eval(problem):  # Se acertar a resposta correta
                        score += 10
                        projectile = None
                        # Gera nova conta e novas respostas
                        if state == LEVEL_1:
                            problem, answers = level_1()
                        elif state == LEVEL_2:
                            problem, answers = level_2()
                        elif state == LEVEL_3:
                            problem, answers = level_3()
                    else:
                        if not lives_deducted:  # Verifica se as vidas já foram diminuídas
                            lives -= 1  # Diminuir vidas apenas uma vez
                            lives_deducted = True  # Marca que as vidas foram diminuídas
                        projectile = None  # Reiniciar o projétil após erro

                    break  # Para evitar múltiplas colisões com o mesmo projétil

    # Reiniciar a flag quando o projétil é reiniciado ou um novo problema começa
    if projectile is None:
        lives_deducted = False  # Resetar a flag
           
                
    # Condições de fim de jogo
    if lives <= 0:
        running = False  # Termina o jogo se as vidas chegarem a 0

    # Atualiza a tela
    pygame.display.flip()

    # Limita o FPS
    pygame.time.Clock().tick(60)
