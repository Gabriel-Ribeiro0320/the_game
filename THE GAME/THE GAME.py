import pygame
import sys

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


# game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw back screen

    screen.fill(BLACK)

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
    level3_button = draw_button('NÍVEL 3', button_font, BLACK, screen, 200 + (button_width + button_gap) * 2,
                                300, button_width, button_height)

    # detect clicks

    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if level1_button.collidepoint(mouse_pos):
            print("Nível 1 selecionado")
        elif level2_button.collidepoint(mouse_pos):
            print("Nível 2 selecionado")
        elif level3_button.collidepoint(mouse_pos):
            print("Nível 3 selecionado")

    # update display

    pygame.display.flip()
