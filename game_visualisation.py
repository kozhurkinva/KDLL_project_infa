import pygame
from game_objects_creatures import *
from game_objects_towers import *


class Menu:
    def __init__(self, game):
        """
        Базовый класс меню, от него наследуются остальные: главное меню, меню выбора урвней и т.д.
        :param game: игра как объект освного класса Game
        """
        self.game = game
        self.mid_h, self.mid_w = self.game.HEIGHT / 2, self.game.WIDTH / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)  # для того, чтобы можно было кастомизировать курсоры
        self.offset = 100

    def draw_cursor(self):
        self.game.draw_text('--', 15, self.cursor_rect.x, self.cursor_rect.y)

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
        self.play_main_theme()
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
        :return:
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


    def play_main_theme(self):
        """
        Воспроизведение музыки в игре
        """
        game_sound = pygame.mixer.music.load("angrybirds.mp3")
        pygame.mixer.music.play(-1)


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
            self.game.level = Level(self.game.level_name, self.game.display)
            self.run_display = False
            self.game.playing = True


class VolumeMenu(Menu):
    def __init__(self, game):
        """
        Меню настроек.
        Методы аналогичны методам MainMenu.
        Будет реализована настройка звука и некоторые другие
        :param game: объект основного класса Game
        """
        Menu.__init__(self, game)
        self.volume_state = 0.5
        self.barx, self.bary = self.mid_w - 100, self.mid_h + 20
        # self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Volume", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 30)
            pygame.draw.rect(self.game.display, (255, 255, 255), (self.barx, self.bary, 200, 50), 3)
            pygame.draw.rect(self.game.display, (255, 255, 255), (self.barx, self.bary, self.volume_state * 200, 50))
            pygame.mixer.music.set_volume(self.volume_state)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY:
            self.volume_state += 0.1
        elif self.game.DOWN_KEY:
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


class Level:
    def __init__(self, level, screen):
        """
        Класс уровня.
        Здесь производится загрузка всех параметров уровня: загружаются текстуры, инициализируется спрайты.
        Данные о данном уровне парсятся из текстового файла level_designs
        :param level: название текущего уровнея в формате "Level #", где # - номер уровня.
        :param screen: поверхность для отрисовки
        """
        self.player_health = 20
        self.player_money = 70
        self.opponents = []
        self.towers = []
        self.allys = [Blue(200, 200)]

        self.level = (level.lower()).replace(' ', '')[-1]

        self.level_name = (level.lower()).replace(' ', '')

        self.screen = screen

        self.background_img = pygame.image.load(
            "levels/level" + str(self.level) + "/Background" + ".png").convert_alpha()

        self.WIDTH, self.HEIGHT = 800, 600
        self.mid_h, self.mid_w = self.HEIGHT / 2, self.WIDTH / 2
        self.choosing_buttons = {
            "Arrow": Button(self.mid_h, self.mid_w, pygame.image.load("Textures/RArrowTower1.png"), 0.8),
            "Bomb": Button(self.mid_h + 50, self.mid_w, pygame.image.load("Textures/RBombTower1.png"), 0.8),
            "Glow": Button(self.mid_h + 100, self.mid_w, pygame.image.load("Textures/1GlowTower1.png"), 0.8)
        }
        self.is_choose = False
        self.choose_menu_state = False
        self.pressed_index = None

        self.text_color = (0, 0, 0)

        # список противников в волнах
        self.wave_timer = 0
        self.wave = 0
        with open("levels/level" + str(self.level) + "/spawn_list.txt", "r") as spawn_list:
            self.spawn_list = spawn_list.read()[:-1].split("\nwave\n")
            for wave_number in range(len(self.spawn_list)):
                self.spawn_list[wave_number] = self.spawn_list[wave_number].split("\n")
                for opp_number in range(len(self.spawn_list[wave_number])):
                    self.spawn_list[wave_number][opp_number] = self.spawn_list[wave_number][opp_number].split()
                    self.spawn_list[wave_number][opp_number][0] = int(self.spawn_list[wave_number][opp_number][0])
                    self.spawn_list[wave_number][opp_number][3] = int(self.spawn_list[wave_number][opp_number][3])

        with open("levels/level" + str(self.level) + "/design.txt", "r") as level_design:
            design = level_design.read().split()
            for i in range(int(design[1])):
                x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
                self.towers += [TowerSpot(x, y, self.opponents)]

    def draw(self):
        """
        Отрисовка башен и обработка нажатия на них пользователя.
        """
        self.screen.blit(self.background_img, (0, 0))

        self.draw_text("Player's money: " + str(self.player_money), self.text_color, 40, 400, 500)
        self.text_color = (0, 0, 0)

        for i in range(len(self.towers)):
            if self.towers[i].is_activate:
                self.towers[i].check_cause()
            self.towers[i].pressing()
            if self.towers[i].is_pressed:
                self.pressed_index = i
            if self.towers[i].is_pressed or self.choose_menu_state:
                if self.towers[self.pressed_index].is_activate and not self.choose_menu_state:
                    if not self.towers[self.pressed_index].sprite == "TowerSpot":
                        if self.player_money >= self.towers[self.pressed_index].upgrade_cost:
                            self.player_money -= self.towers[self.pressed_index].upgrade_cost
                            self.towers[self.pressed_index].upgrade()
                            print(self.player_money)
                        else:
                            self.text_color = (255, 0, 0)
                            print("You haven't got a money")
                    elif self.towers[self.pressed_index].sprite == "TowerSpot":
                        self.towers[self.pressed_index].is_activate = False
                elif not self.towers[self.pressed_index].is_activate:
                    self.choose_menu_state = True
                    if self.choosing_buttons["Arrow"].is_pressed():
                        self.towers[self.pressed_index] = ArrowTower(self.towers[self.pressed_index].x,
                                                                     self.towers[self.pressed_index].y,
                                                                     self.towers[self.pressed_index].enemy_list)
                        if self.player_money >= self.towers[self.pressed_index].cost:
                            self.player_money -= self.towers[self.pressed_index].cost
                            self.towers[self.pressed_index].is_activate = True
                            self.choose_menu_state = False
                            self.pressed_index = None
                            print(self.player_money)
                        else:
                            self.towers[self.pressed_index] = TowerSpot(self.towers[self.pressed_index].x,
                                                                        self.towers[self.pressed_index].y,
                                                                        self.towers[self.pressed_index].enemy_list)
                            self.towers[self.pressed_index].is_activate = True
                            self.choose_menu_state = False
                            self.pressed_index = None
                            self.text_color = (255, 0, 0)
                            print("No money")
                    elif self.choosing_buttons["Bomb"].is_pressed():
                        self.towers[self.pressed_index] = BombTower(self.towers[self.pressed_index].x,
                                                                    self.towers[self.pressed_index].y,
                                                                    self.towers[self.pressed_index].enemy_list)
                        if self.player_money >= self.towers[self.pressed_index].cost:
                            self.player_money -= self.towers[self.pressed_index].cost
                            self.towers[self.pressed_index].is_activate = True
                            self.choose_menu_state = False
                            self.pressed_index = None
                            print(self.player_money)
                        else:
                            self.towers[self.pressed_index] = TowerSpot(self.towers[self.pressed_index].x,
                                                                        self.towers[self.pressed_index].y,
                                                                        self.towers[self.pressed_index].enemy_list)
                            self.towers[self.pressed_index].is_activate = True
                            self.choose_menu_state = False
                            self.pressed_index = None
                            self.text_color = (255, 0, 0)
                            print("No money")
                    elif self.choosing_buttons["Glow"].is_pressed():
                        self.towers[self.pressed_index] = GlowTower(self.towers[self.pressed_index].x,
                                                                    self.towers[self.pressed_index].y,
                                                                    self.towers[self.pressed_index].enemy_list)
                        if self.player_money >= self.towers[self.pressed_index].cost:
                            self.player_money -= self.towers[self.pressed_index].cost
                            self.towers[self.pressed_index].is_activate = True
                            self.choose_menu_state = False
                            self.pressed_index = None
                            print(self.player_money)
                        else:
                            self.towers[self.pressed_index] = TowerSpot(self.towers[self.pressed_index].x,
                                                                        self.towers[self.pressed_index].y,
                                                                        self.towers[self.pressed_index].enemy_list)
                            self.towers[self.pressed_index].is_activate = True
                            self.choose_menu_state = False
                            self.pressed_index = None
                            self.text_color = (255, 0, 0)
                            print("No money")
                    self.choosing_buttons["Arrow"].draw(self.screen)
                    self.choosing_buttons["Bomb"].draw(self.screen)
                    self.choosing_buttons["Glow"].draw(self.screen)
            self.towers[i].draw(self.screen)

        self.spawn_opp()
        for opp in self.opponents:
            for al in ([0] + self.allys):
                opp.fight(al)
            if not opp.alive:
                self.opponents.pop(self.opponents.index(opp))
                self.player_money += opp.loot
            if opp.finished:
                self.player_health -= opp.player_damage
                self.player_money -= opp.loot  # в случае прохода врага деньги не добавляются
            opp.move_opponent(self.level_name)
            for projectile in opp.projectiles:
                projectile.move(self.screen)
            opp.draw(self.screen)  # FIXME временно, для тестов

        for al in self.allys:
            if not al.alive:
                self.allys.pop(self.allys.index(al))
            for projectile in al.projectiles:
                projectile.move(self.screen)
            al.draw(self.screen)

    def draw_text(self, text, color, size, x, y):
        """
        Универсальная функция отрисовки текста
        :param color: цвет текста
        :param text: то, что будет напечатано
        :param size: размер текста
        :param x: x-положение левого верхнего угла поля с текстом
        :param y: y-положение левого верхнего угла поля с текстом
        """
        font_name = pygame.font.get_default_font()
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def spawn_opp(self):
        """
        функция, создающая противников в обозначенном в self.spawn_list порядке
        """
        if self.wave < len(self.spawn_list):
            num_wave_opp = 0    # считает, сколько противников появится в этой волне
            for i in range(len(self.spawn_list[self.wave])):
                if (not self.wave_timer % self.spawn_list[self.wave][i][3]) and (self.spawn_list[self.wave][i][0] > 0):
                    self.spawn_list[self.wave][i][0] -= 1
                    for opp in OPPONENT_CLASSES_LIST:
                        if opp.__name__ == self.spawn_list[self.wave][i][1]:
                            self.opponents += [opp(self.spawn_list[self.wave][i][2])]
                num_wave_opp += self.spawn_list[self.wave][i][0]
            self.wave_timer += 1
            if num_wave_opp == 0:   # если эта волна кончилась, запускается следующая
                self.wave += 1
                self.wave_timer = 0


class Button:  # FIXME: возможно вообще уберем этот класс
    def __init__(self, x, y, image, scale):
        """
        Класс кнопки.
        Может сделать какой-то спрайт или область экрана кликабельными.
        :param x: x-коодината левого верххнего угла прямоугольника, в котором расположено изображение спрайта или кнопки
        :param y: y-коодината левого верххнего угла прямоугольника, в котором расположено изображение спрайта или кнопки
        :param image: изображение спрайта или кнопки в виде png-файла
        :param scale: масштаб  поотношению к исходному файлу с изображением
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def is_pressed(self):
        """
        Обработчик нажатия на кнопку, а также отрисовщик кнопки.
        :param surface: поверхность отрисовки
        :return: состояние кнопки (нажата или нет)
        """
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
