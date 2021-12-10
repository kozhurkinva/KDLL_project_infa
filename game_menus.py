import pygame


class Menu:
    def __init__(self, game):
        """
        Базовый класс меню, от него наследуются остальные: главное меню, меню выбора урвней и т.д.
        :param game: игра как объект освного класса Game
        """
        self.game = game
        self.mid_h, self.mid_w = self.game.HEIGHT / 2, self.game.WIDTH / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = 100

    def draw_cursor(self):
        self.game.draw_text("--", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        """
        Основное меню. В нем осуществляется навигация по настройкам игры, а также выход из игры.
        :param game: игра как объект освного класса Game
        """
        Menu.__init__(self, game)
        self.state = "Start Game"
        self.startx, self.starty = self.mid_w, self.mid_h + 20
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 110
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        """
        Отображает меню на экране
        """
        self.run_display = True
        pygame.mixer.music.play(-1)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Maaaain Menu", 50, self.mid_w, self.mid_h - 50)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Volume", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", 40, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        """
        Отвечает за передвижение курсора пользователя - стрелочка справа от аттрибутов меню
        """
        if self.game.DOWN_KEY:
            if self.state == "Start Game":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Volume"
            elif self.state == "Volume":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start Game"
        elif self.game.UP_KEY:
            if self.state == "Start Game":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Volume":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start Game"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Volume"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"

    def check_input(self):
        """
        Обрабатывает собыия нажатия на соответствующие аттрибуты меню и осущетсвляет взаимодействия пользователя с меню
        """
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start Game":
                self.game.curr_menu = self.game.levels
            elif self.state == "Volume":
                self.game.curr_menu = self.game.volume_set
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits
            elif self.state == "Exit":
                self.game.running, self.game.playing = False, False
            self.run_display = False


class LevelsMenu(Menu):
    def __init__(self, game):
        """
        Меню выбора уровней.
        Методы аналогичны методам MainMenu.
        При нажатии на соответствующий уровень запускает игровой процесс этого уровня
        :param game: объект основного класса Game
        """
        Menu.__init__(self, game)
        self.state = "Level 1"
        self.lvl1_x, self.lvl1_y = self.mid_w, self.mid_h + 20
        self.lvl2_x, self.lvl2_y = self.mid_w, self.mid_h + 40
        self.lvl3_x, self.lvl3_y = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.lvl1_x + self.offset, self.lvl1_y)

    def display_menu(self):
        """
        Отображает меню на экране
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Levels", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 30)
            self.game.draw_text("Level 1", 15, self.lvl1_x, self.lvl1_y)
            self.game.draw_text("Level 2", 15, self.lvl2_x, self.lvl2_y)
            self.game.draw_text("Level 3", 15, self.lvl3_x, self.lvl3_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        """
        Обрабатывает собыия нажатия на соответствующие аттрибуты меню и осущетсвляет взаимодействия пользователя с меню
        """
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == "Level 1":
                self.cursor_rect.midtop = (self.lvl2_x + self.offset, self.lvl2_y)
                self.state = "Level 2"
            elif self.state == "Level 2":
                self.cursor_rect.midtop = (self.lvl3_x + self.offset, self.lvl3_y)
                self.state = "Level 3"
            elif self.state == "Level 3":
                self.cursor_rect.midtop = (self.lvl1_x + self.offset, self.lvl1_y)
                self.state = "Level 1"
        elif self.game.UP_KEY:
            if self.state == "Level 1":
                self.cursor_rect.midtop = (self.lvl3_x + self.offset, self.lvl3_y)
                self.state = "Level 3"
            elif self.state == "Level 3":
                self.cursor_rect.midtop = (self.lvl2_x + self.offset, self.lvl2_y)
                self.state = "Level 2"
            elif self.state == "Level 2":
                self.cursor_rect.midtop = (self.lvl1_x + self.offset, self.lvl1_y)
                self.state = "Level 1"
        elif self.game.START_KEY:
            self.game.level_name = self.state
            self.game.set_level()
            self.run_display = False


class VolumeMenu(Menu):
    def __init__(self, game):
        """
        Меню настроек.
        Методы аналогичны методам MainMenu.
        Будет реализована настройка звука и некоторые другие
        :param game: объект основного класса Game
        """
        Menu.__init__(self, game)
        self.volume_state = 1.
        self.barx, self.bary = self.mid_w - 200, self.mid_h + 20

    def display_menu(self):
        """
        Отображает меню на экране
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Volume", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 30)
            pygame.draw.rect(self.game.display, (255, 255, 255), (self.barx, self.bary, 400, 50), 3)
            pygame.draw.rect(self.game.display, (255, 255, 255), (self.barx, self.bary, self.volume_state * 400, 50))
            pygame.mixer.music.set_volume(self.volume_state)
            self.game.screem_sound.set_volume(self.volume_state)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        """
        Обрабатывает собыия нажатия на соответствующие аттрибуты меню и осущетсвляет взаимодействия пользователя с меню
        """
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY:
            if self.volume_state < 0.9:
                self.volume_state += 0.1
        elif self.game.DOWN_KEY:
            if self.volume_state > 0.1:
                self.volume_state -= 0.1


class CreditsMenu(Menu):
    def __init__(self, game):
        """
        Меню валюты или очков.
        Методы аналогичны методам MainMenu.
        Позже будет встроено в логику работы программы
        :param game: объект основного класса Game
        """
        Menu.__init__(self, game)

    def display_menu(self):
        """
        Отображает меню на экране
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Credits", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20)
            self.game.draw_text("Made by me", 15, self.game.WIDTH / 2, self.game.HEIGHT / 2 + 10)
            self.blit_screen()


class WinLoseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = False

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            if self.state:
                self.game.draw_text("Ah Gooood! You Win!!!", 50, self.game.mid_w, self.game.mid_h - 20)
            else:
                self.game.draw_text("Ah Shit! You Lose!", 50, self.game.mid_w, self.game.mid_h + 10)
            self.blit_screen()
