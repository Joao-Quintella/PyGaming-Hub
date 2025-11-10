import pygame
import sys
import os
import configparser
import random

CONFIG_FILE = os.path.join('conf', 'conf.ini')
config = configparser.ConfigParser()

CONTROLS_KEY_CODES = {}
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FULLSCREEN = False

try:
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Arquivo de configuration do console não encontrado em {CONFIG_FILE}")

    config.read(CONFIG_FILE)

    display_section = 'Display'
    SCREEN_WIDTH = config.getint(display_section, 'width', fallback=1280)
    SCREEN_HEIGHT = config.getint(display_section, 'height', fallback=720)
    FULLSCREEN = config.getboolean(display_section, 'fullscreen', fallback=False)

    controls_section = 'Controls'
    CONTROLS_KEY_CODES['UP'] = pygame.key.key_code(config.get(controls_section, 'up', fallback='w'))
    CONTROLS_KEY_CODES['DOWN'] = pygame.key.key_code(config.get(controls_section, 'down', fallback='s'))
    CONTROLS_KEY_CODES['LEFT'] = pygame.key.key_code(config.get(controls_section, 'left', fallback='a'))
    CONTROLS_KEY_CODES['RIGHT'] = pygame.key.key_code(config.get(controls_section, 'right', fallback='d'))
    CONTROLS_KEY_CODES['A'] = pygame.key.key_code(config.get(controls_section, 'action_a', fallback='o'))
    CONTROLS_KEY_CODES['B'] = pygame.key.key_code(config.get(controls_section, 'action_b', fallback='p'))
    CONTROLS_KEY_CODES['PAUSE'] = pygame.key.key_code(config.get(controls_section, 'pause', fallback='enter'))


except Exception as e:
    print(f"ERRO: Não foi possível carregar a configuração do console: {e}")
    print("Usando controles e resolução padrão (800x600, WASD, O, P, Enter).")
    CONTROLS_KEY_CODES = {
        'UP': pygame.K_w, 'DOWN': pygame.K_s, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d,
        'A': pygame.K_o, 'B': pygame.K_p, 'PAUSE': pygame.K_RETURN
    }

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

pygame.init()

BG_COLOR = (10, 10, 10)
PLAYER_COLOR = (255, 0, 0)
PLAYER_SIZE = 50
PLAYER_SPEED = 7

display_flags = 0
if FULLSCREEN:
    display_flags = pygame.FULLSCREEN | pygame.SCALED

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display_flags)

pygame.display.set_caption(f"Jogo do Quadrado (Pressione 'Pause' para sair)")
clock = pygame.time.Clock()

player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
player_y = (SCREEN_HEIGHT - PLAYER_SIZE) // 2

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == CONTROLS_KEY_CODES['A']:
                PLAYER_COLOR = get_random_color()

            if event.key == CONTROLS_KEY_CODES['B']:
                BG_COLOR = get_random_color()

            if event.key == CONTROLS_KEY_CODES['PAUSE']:
                running = False

    keys = pygame.key.get_pressed()

    if keys[CONTROLS_KEY_CODES['UP']]:
        player_y -= PLAYER_SPEED
    if keys[CONTROLS_KEY_CODES['DOWN']]:
        player_y += PLAYER_SPEED
    if keys[CONTROLS_KEY_CODES['LEFT']]:
        player_x -= PLAYER_SPEED
    if keys[CONTROLS_KEY_CODES['RIGHT']]:
        player_x += PLAYER_SPEED

    player_x = max(0, min(player_x, SCREEN_WIDTH - PLAYER_SIZE))
    player_y = max(0, min(player_y, SCREEN_HEIGHT - PLAYER_SIZE))

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
