import pygame
import random
import math

# Inicializa o Pygame
pygame.init()

# Configurações básicas da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo com Raio de Exclusão")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Função para verificar se a posição está fora do raio de exclusão
def is_outside_exclusion_radius(x, y, x_pos, y_pos, exclusion_radius):
    distance = math.sqrt((x - x_pos) ** 2 + (y - y_pos) ** 2)
    return distance > exclusion_radius


# Função para gerar posições aleatórias fora do raio de exclusão
def generate_positions(num_blocks, block_width, block_height, screen_width, screen_height, exclusion_radius, x_pos,
                       y_pos):
    positions = []

    while len(positions) < num_blocks:
        x = random.randint(0, screen_width - block_width)
        y = random.randint(0, screen_height - block_height)

        if is_outside_exclusion_radius(x, y, x_pos, y_pos, exclusion_radius):
            positions.append((x, y))

    return positions


# Variáveis de configuração dos blocos e personagem
num_blocks = 13
block_width = 30
block_height = 20
exclusion_radius = 100  # Raio de exclusão ao redor do personagem
x_pos = 400  # Posição inicial do personagem (x)
y_pos = 300  # Posição inicial do personagem (y)

# Gera as posições dos blocos fora do raio de exclusão
positions = generate_positions(num_blocks, block_width, block_height, screen_width, screen_height, exclusion_radius,
                               x_pos, y_pos)


# Função principal do jogo
def game_loop():
    # Configurações iniciais
    running = True
    clock = pygame.time.Clock()

    # Posição inicial do personagem (pode ser alterada se houver movimento)
    player_x = x_pos
    player_y = y_pos
    player_width = 40
    player_height = 40
    player_speed = 5

    # Loop principal do jogo
    while running:
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Captura as teclas pressionadas para movimentar o personagem
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
            player_y += player_speed

        # Preenche a tela com branco
        screen.fill(WHITE)

        # Desenha os blocos nas posições geradas
        for pos in positions:
            x, y = pos
            pygame.draw.rect(screen, RED, (x, y, block_width, block_height))

        # Desenha o personagem (por exemplo, um quadrado)
        pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_width, player_height))

        # Atualiza a tela
        pygame.display.flip()

        # Define a taxa de frames por segundo (FPS)
        clock.tick(30)

    # Fecha o Pygame
    pygame.quit()


# Inicia o jogo
game_loop()
