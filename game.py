import ctypes

import pygame.mixer

from game_visualisation import *
from game_objects_creatures import *
from game_objects_towers import *


class Game:
    def __init__(self):
        """
        Основной класс игры.
        Здесь происзодит инициалиция размеров окна, настройка соответствущих флагов,
        поверхностей отрисовки, шрифта текста, а также инициализация меню и переменных логики игры
        """
        # General
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.mid_h, self.mid_w = self.HEIGHT / 2, self.WIDTH / 2
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.FPS = 60
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.playing, self.running = False, True,
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font_name = pygame.font.get_default_font()
        self.clock = pygame.time.Clock()

        # Sounds
        self.background_sound = pygame.mixer.Sound("background.wav")

        # Game variables and counters
        self.level_name = 0
        self.tower_types = [0] * 999
        self.towers = []
        # self.opponents = []
        self.bullets = []
        self.press_count = 0
        self.is_paused = False

        # Level object
        self.level = None

        # Menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.levels = LevelsMenu(self)
        self.curr_menu = self.main_menu

    def main_loop(self):
        """
        Основной цикл игры. Здесь происходит отрисовка уровня и непосредственно игровой процесс.
        """
        while self.playing:
            self.check_events()
            if self.BACK_KEY:
                self.press_count += 1
                if self.press_count == 1:
                    self.is_paused = True
                elif self.press_count == 2:
                    self.press_count = 0
                    self.is_paused = False
                    self.playing = False
            elif self.START_KEY:
                if self.press_count == 1:
                    self.is_paused = False
                    self.press_count = 0

            self.display.fill(self.BLACK)

            if not self.is_paused:
                self.level.draw()
            else:
                self.draw_text("Pause", 30, self.mid_w, self.mid_h)

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()
            self.clock.tick(self.FPS)

    def check_events(self):
        """
        Функция-обработчик событий pygame. В частности, обработчик нажатия пользователем соответсвутющей
        клавиши на клавиатуре и выхода из игры
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        """
        Обновление состояния флажков нажатия на кнопку
        """
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        """
        Универсальная функция отрисовки текста
        :param text: то, что будет напечатано
        :param size: размер текста
        :param x: x-положение левого верхнего угла поля с текстом
        :param y: y-положение левого верхнего угла поля с текстом
        """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
