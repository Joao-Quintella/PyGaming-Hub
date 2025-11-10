import pygame
import sys
import os
import configparser
import subprocess

CONF_DIR = 'conf'
CONFIG_FILE = os.path.join(CONF_DIR, 'conf.ini')

def create_default_config(config):
    config['Display'] = {
        'width': '1280',
        'height': '720',
        'fullscreen': 'False'
    }
    config['Controls'] = {
        'up': 'w',
        'down': 's',
        'left': 'a',
        'right': 'd',
        'action_a': 'o',
        'action_b': 'p',
        'pause': 'enter'
    }
    config['Info'] = {
        'authors': 'Wilson Cosmo'
    }
    save_config(config)

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        print("Arquivo de configuração não encontrado, criando um novo...")
        create_default_config(config)
    else:
        config.read(CONFIG_FILE)
    return config

def save_config(config):
    conf_directory = os.path.dirname(CONFIG_FILE)

    if conf_directory and not os.path.exists(conf_directory):
        try:
            os.makedirs(conf_directory)
            print(f"Diretório '{conf_directory}' criado.")
        except OSError as e:
            print(f"Erro ao criar o diretório {conf_directory}: {e}")

    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    except Exception as e:
        print(f"Erro ao salvar o {CONFIG_FILE}: {e}")

config = load_config()

SCREEN_WIDTH = config.getint('Display', 'width')
SCREEN_HEIGHT = config.getint('Display', 'height')
FULLSCREEN = config.getboolean('Display', 'fullscreen')

controls_section = 'Controls'
CONTROLS = {
    'UP': config.get(controls_section, 'up', fallback='w'),
    'DOWN': config.get(controls_section, 'down', fallback='s'),
    'LEFT': config.get(controls_section, 'left', fallback='a'),
    'RIGHT': config.get(controls_section, 'right', fallback='d'),
    'A': config.get(controls_section, 'action_a', fallback='o'),
    'B': config.get(controls_section, 'action_b', fallback='p'),
    'PAUSE': config.get(controls_section, 'pause', fallback='enter')
}

AUTHORS = config.get('Info', 'authors')


def draw_text(surface, text, size, x, y, color=(255, 255, 255), anchor="topleft"):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if anchor == "center":
        text_rect.center = (x, y)
    elif anchor == "topleft":
        text_rect.topleft = (x, y)
    elif anchor == "midtop":
        text_rect.midtop = (x, y)

    surface.blit(text_surface, text_rect)
    return text_rect

def scan_game_directory():
    games_dir = 'games'
    game_list = []

    if not os.path.exists(games_dir):
        os.makedirs(games_dir)
        return []

    try:
        for folder_name in os.listdir(games_dir):
            game_folder_path = os.path.join(games_dir, folder_name)

            if os.path.isdir(game_folder_path):
                main_py_path = os.path.join(game_folder_path, 'main.py')
                data_inf_path = os.path.join(game_folder_path, 'data.inf')

                if os.path.exists(main_py_path) and os.path.exists(data_inf_path):
                    try:
                        game_config = configparser.ConfigParser()
                        game_config.read(data_inf_path, encoding='utf-8')

                        game_name = game_config.get('Game', 'nome', fallback=folder_name)
                        game_authors = game_config.get('Game', 'autores', fallback='Autor Desconhecido')

                        game_data = {
                            'folder': folder_name,
                            'name': game_name,
                            'authors': game_authors
                        }
                        game_list.append(game_data)

                    except Exception as e:
                        print(f"Erro ao ler data.inf em {folder_name}: {e}")
                        game_list.append({'folder': folder_name, 'name': folder_name, 'authors': 'Erro ao ler data.inf'})
                else:
                    print(f"Ignorando pasta {folder_name}: arquivos 'main.py' ou 'data.inf' ausentes.")

        return game_list

    except Exception as e:
        print(f"Erro ao ler o diretório de jogos: {e}")
        return []

def launch_game(game_folder_name):
    print(f"Tentando iniciar o jogo da pasta: {game_folder_name}")
    game_path = os.path.join('games', game_folder_name, 'main.py')

    if os.path.exists(game_path):
        pygame.quit()

        try:
            subprocess.run([sys.executable, game_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"O jogo falhou ao executar: {e}")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")

        main()

    else:
        print(f"Erro: 'main.py' não encontrado para o jogo na pasta '{game_folder_name}'")


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ['Biblioteca de Jogos', 'Ajuda', 'Configuração', 'Sobre', 'Sair']
        self.selected_option = 0
        self.title_font_size = 74
        self.option_font_size = 50

    def handle_event(self, event):
        global current_state

        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)

            if key_name == CONTROLS['DOWN']:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif key_name == CONTROLS['UP']:
                self.selected_option = (self.selected_option - 1) % len(self.options)

            elif key_name == CONTROLS['A']:
                selected = self.options[self.selected_option]
                if selected == 'Biblioteca de Jogos':
                    current_state = game_library_screen
                elif selected == 'Ajuda':
                    current_state = help_screen
                elif selected == 'Configuração':
                    current_state = settings_screen
                elif selected == 'Sobre':
                    current_state = about_screen
                elif selected == 'Sair':
                    pygame.quit()
                    sys.exit()

    def draw(self):
        self.screen.fill((20, 20, 40))
        draw_text(self.screen, "PyGaming Hub", self.title_font_size, SCREEN_WIDTH // 2, 100, color=(255, 200, 0), anchor="center")

        for i, option in enumerate(self.options):
            y_pos = 250 + i * (self.option_font_size + 15)

            if i == self.selected_option:
                color = (255, 255, 0)
                draw_text(self.screen, f"> {option}", self.option_font_size, SCREEN_WIDTH // 2, y_pos, color=color, anchor="center")
            else:
                color = (255, 255, 255)
                draw_text(self.screen, option, self.option_font_size, SCREEN_WIDTH // 2, y_pos, color=color, anchor="center")

class GameLibrary:
    def __init__(self, screen):
        self.screen = screen
        self.games = []
        self.selected_game = 0
        self.title_font_size = 60
        self.option_font_size = 40
        self.message = ""

    def on_enter(self):
        self.games = scan_game_directory()
        self.selected_game = 0
        if not self.games:
            self.message = "Nenhum jogo encontrado. (Verifique /games/ e os data.inf)"
        else:
            self.message = ""

    def handle_event(self, event):
        global current_state
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)

            if key_name == CONTROLS['B']:
                current_state = main_menu_screen

            if not self.games:
                return

            if key_name == CONTROLS['DOWN']:
                self.selected_game = (self.selected_game + 1) % len(self.games)
            elif key_name == CONTROLS['UP']:
                self.selected_game = (self.selected_game - 1) % len(self.games)
            elif key_name == CONTROLS['A']:
                selected_game_data = self.games[self.selected_game]
                launch_game(selected_game_data['folder'])

    def draw(self):
        self.screen.fill((40, 20, 20))
        draw_text(self.screen, "Biblioteca de Jogos", self.title_font_size, SCREEN_WIDTH // 2, 50, color=(255, 100, 100), anchor="center")

        if self.message:
            draw_text(self.screen, self.message, 30, SCREEN_WIDTH // 2, 150, color=(255, 255, 255), anchor="center")

        for i, game_data in enumerate(self.games):
            y_pos = 200 + i * (self.option_font_size + 10)

            display_name = game_data['name']

            if i == self.selected_game:
                color = (255, 255, 0)
                draw_text(self.screen, f"> {display_name}", self.option_font_size, SCREEN_WIDTH // 2, y_pos, color=color, anchor="center")
            else:
                color = (255, 255, 255)
                draw_text(self.screen, display_name, self.option_font_size, SCREEN_WIDTH // 2, y_pos, color=color, anchor="center")

        draw_text(self.screen, f"Pressione '{CONTROLS['B']}' para Voltar", 25, 20, SCREEN_HEIGHT - 30, color=(200, 200, 200), anchor="topleft")



class HelpScreen:
    def __init__(self, screen):
        self.screen = screen

    def on_enter(self):
        pass

    def handle_event(self, event):
        global current_state
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if key_name == CONTROLS['B']:
                current_state = main_menu_screen

    def draw(self):
        self.screen.fill((20, 40, 20))
        draw_text(self.screen, "Ajuda", 60, SCREEN_WIDTH // 2, 50, color=(100, 255, 100), anchor="center")

        draw_text(self.screen, "Controles do Menu:", 40, 100, 150, color=(255, 255, 255), anchor="topleft")
        draw_text(self.screen, f"Cima:     {CONTROLS['UP'].upper()}", 35, 120, 210, color=(200, 200, 200), anchor="topleft")
        draw_text(self.screen, f"Baixo:    {CONTROLS['DOWN'].upper()}", 35, 120, 250, color=(200, 200, 200), anchor="topleft")
        draw_text(self.screen, f"Esquerda: {CONTROLS['LEFT'].upper()}", 35, 120, 290, color=(200, 200, 200), anchor="topleft")
        draw_text(self.screen, f"Direita: {CONTROLS['RIGHT'].upper()}", 35, 120, 330, color=(200, 200, 200), anchor="topleft")

        draw_text(self.screen, f"Confirmar (Ação A): {CONTROLS['A'].upper()}", 35, 120, 400, color=(200, 200, 200), anchor="topleft")
        draw_text(self.screen, f"Voltar    (Ação B): {CONTROLS['B'].upper()}", 35, 120, 440, color=(200, 200, 200), anchor="topleft")

        draw_text(self.screen, f"Pause:            {CONTROLS['PAUSE'].upper()}", 35, 120, 480, color=(200, 200, 200), anchor="topleft")


        draw_text(self.screen, f"Pressione '{CONTROLS['B']}' para Voltar", 25, 20, SCREEN_HEIGHT - 30, color=(200, 200, 200), anchor="topleft")

class SettingsScreen:
    def __init__(self, screen):
        self.screen = screen

    def on_enter(self):
        pass

    def handle_event(self, event):
        global current_state
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if key_name == CONTROLS['B']:
                current_state = main_menu_screen

    def draw(self):
        self.screen.fill((40, 20, 40))
        draw_text(self.screen, "Configuração", 60, SCREEN_WIDTH // 2, 50, color=(200, 100, 255), anchor="center")

        draw_text(self.screen, "Esta tela é um protótipo.", 35, SCREEN_WIDTH // 2, 200, anchor="center")
        draw_text(self.screen, "Aqui você poderia ajustar resolução", 35, SCREEN_WIDTH // 2, 250, anchor="center")
        draw_text(self.screen, "e remapear os controles.", 35, SCREEN_WIDTH // 2, 300, anchor="center")

        draw_text(self.screen, "Os valores atuais estão em conf.ini", 30, SCREEN_WIDTH // 2, 400, color=(200, 200, 200), anchor="center")

        draw_text(self.screen, f"Pressione '{CONTROLS['B']}' para Voltar", 25, 20, SCREEN_HEIGHT - 30, color=(200, 200, 200), anchor="topleft")

class AboutScreen:
    def __init__(self, screen):
        self.screen = screen
        self.game_list = []

    def on_enter(self):
        self.game_list = scan_game_directory()

    def handle_event(self, event):
        global current_state
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if key_name == CONTROLS['B']:
                current_state = main_menu_screen

    def draw(self):
        self.screen.fill((20, 40, 40))
        draw_text(self.screen, "Sobre", 60, SCREEN_WIDTH // 2, 50, color=(100, 200, 255), anchor="center")

        draw_text(self.screen, "Console Arcade em Python", 40, SCREEN_WIDTH // 2, 150, anchor="center")

        draw_text(self.screen, f"Autor do Console: {AUTHORS}", 35, SCREEN_WIDTH // 2, 210, anchor="center")
        draw_text(self.screen, "Usando a biblioteca Pygame.", 30, SCREEN_WIDTH // 2, 250, anchor="center")

        draw_text(self.screen, "Autores dos Jogos:", 40, 100, 320, color=(255, 200, 0), anchor="topleft")

        y_pos = 370

        if not self.game_list:
            draw_text(self.screen, "Nenhum jogo encontrado na pasta /games/", 25, 120, y_pos, color=(200, 200, 200), anchor="topleft")
        else:

            for game_data in self.game_list:

                if y_pos > SCREEN_HEIGHT - 80:
                    draw_text(self.screen, "...", 25, 120, y_pos, color=(200, 200, 200), anchor="topleft")
                    break

                game_title = game_data['name']
                game_authors = game_data['authors']


                draw_text(self.screen, f"• {game_title}", 30, 120, y_pos, color=(255, 255, 255), anchor="topleft")
                draw_text(self.screen, f"  por: {game_authors}", 25, 140, y_pos + 30, color=(200, 200, 200), anchor="topleft")

                y_pos += 70

        draw_text(self.screen, f"Pressione '{CONTROLS['B']}' para Voltar", 25, 20, SCREEN_HEIGHT - 30, color=(200, 200, 200), anchor="topleft")


def main():
    global screen, clock, current_state
    global main_menu_screen, game_library_screen, help_screen, settings_screen, about_screen

    pygame.init()
    pygame.font.init()

    display_flags = 0
    if FULLSCREEN:
        display_flags = pygame.FULLSCREEN | pygame.SCALED

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display_flags)
    pygame.display.set_caption("PyGaming Hub")
    clock = pygame.time.Clock()

    main_menu_screen = MainMenu(screen)
    game_library_screen = GameLibrary(screen)
    help_screen = HelpScreen(screen)
    settings_screen = SettingsScreen(screen)
    about_screen = AboutScreen(screen)

    current_state = main_menu_screen

    if hasattr(current_state, 'on_enter'):
        current_state.on_enter()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            old_state = current_state
            current_state.handle_event(event)

            if current_state != old_state and hasattr(current_state, 'on_enter'):
                current_state.on_enter()

        current_state.draw()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
