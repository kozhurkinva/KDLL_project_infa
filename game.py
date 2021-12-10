from game_menus import *
from game_level import *
import pygame.mixer
import pygame


class Game:
    def __init__(self):
        """
        Основной класс игры.
        Здесь происзодит инициалиция размеров окна, настройка соответствущих флагов,
        поверхностей отрисовки, шрифта текста, а также инициализация меню и переменных логики игры
        """
        # Общее
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

        # Звуки
        self.background_music = pygame.mixer.music.load("Sound/angrybirds.mp3")
        self.screem_sound = pygame.mixer.Sound("Sound/takedam1.wav")

        # Объект уровня
        self.curr_level = None
        self.level_name = ""

        # Меню и пауза
        self.main_menu = MainMenu(self)
        self.volume_set = VolumeMenu(self)
        self.credits = CreditsMenu(self)
        self.levels = LevelsMenu(self)
        self.winlose = WinLoseMenu(self)
        self.curr_menu = self.main_menu
        self.press_count = 0
        self.is_paused = False

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
                self.curr_level.draw()
            else:
                self.draw_text("Pause", 30, self.mid_w, self.mid_h)

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()
            self.clock.tick(self.FPS)

    def set_level(self):
        self.curr_level = Level(self, self.level_name, self.display)
        self.playing = True

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
