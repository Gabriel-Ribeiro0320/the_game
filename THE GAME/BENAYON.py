import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definindo as dimensões da tela
screen_width = 800
screen_height = 600

# Criando a janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Over Test")

# Fonte para o texto
font = pygame.font.Font(None, 70)
font2 = pygame.font.Font(None, 50)
font3 = pygame.font.Font(None, 25)
smaller_font = pygame.font.SysFont(None, 20)

# Variáveis do jogo
score = 5  # Apenas um exemplo de pontuação
state = "GAME_OVER"  # Definimos o estado como GAME_OVER para testar
running = True

# Loop do jogo
while running:
    if state == "GAME_OVER":
        screen.fill(BLACK)
        game_over_text = font2.render("Boa Tentativa!", True, WHITE)
        score_text = font3.render(f"Você respondeu {score} certas!", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 280))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 320))
        pygame.display.flip()

        # Adicionando uma verificação para fechar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Finalizando o Pygame
pygame.quit()
sys.exit()
