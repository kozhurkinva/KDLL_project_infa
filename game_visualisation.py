from game_objects_creatures import *
from game_objects_towers import *


class Level:
    def __init__(self, level, screen):
        """
        Класс уровня.
        Здесь производится загрузка всех параметров уровня: загружаются текстуры, инициализируется спрайты.
        Данные о данном уровне парсятся из текстового файла level_designs
        :param level: название текущего уровнея в формате "Level #", где # - номер уровня.
        :param screen: поверхность для отрисовки
        """
        # Для игры
        self.player_health = 20
        self.player_money = 70
        self.opponents = []
        self.towers = []
        self.allys = [Blue(200, 200)]

        # Для настройки уровня
        self.level = (level.lower()).replace(' ', '')[-1]
        self.level_name = (level.lower()).replace(' ', '')

        # Поверхность отрисовки
        self.screen = screen

        # Изображения
        self.background_img = pygame.image.load(
            "levels/level" + str(self.level) + "/Background" + ".png").convert_alpha()
        self.active_arrow_button_img = pygame.image.load("Textures/RArrowTower1.png").convert_alpha()
        self.active_bomb_button_img = pygame.image.load("Textures/RBombTower1.png").convert_alpha()
        self.active_glow_button_img = pygame.image.load("Textures/1GlowTower1.png").convert_alpha()
        self.passive_arrow_button_img = pygame.image.load("Textures/LockedArrowTower.png").convert_alpha()
        self.passive_bomb_button_img = pygame.image.load("Textures/LockedBombTower.png").convert_alpha()
        self.passive_glow_button_img = pygame.image.load("Textures/LockedGlowTower.png").convert_alpha()

        self.active_arrow_button_img = pygame.transform.scale(self.active_arrow_button_img, (
            self.active_arrow_button_img.get_size()[0] * 0.8, self.active_arrow_button_img.get_size()[1] * 0.8))
        self.active_bomb_button_img = pygame.transform.scale(self.active_bomb_button_img, (
            self.active_bomb_button_img.get_size()[0] * 0.8, self.active_bomb_button_img.get_size()[1] * 0.8))
        self.active_glow_button_img = pygame.transform.scale(self.active_glow_button_img, (
            self.active_glow_button_img.get_size()[0] * 0.8, self.active_glow_button_img.get_size()[1] * 0.8))
        self.passive_arrow_button_img = pygame.transform.scale(self.passive_arrow_button_img, (
            self.passive_arrow_button_img.get_size()[0] * 0.8, self.passive_arrow_button_img.get_size()[1] * 0.8))
        self.passive_bomb_button_img = pygame.transform.scale(self.passive_bomb_button_img, (
            self.passive_bomb_button_img.get_size()[0] * 0.8, self.passive_bomb_button_img.get_size()[1] * 0.8))
        self.passive_glow_button_img = pygame.transform.scale(self.passive_glow_button_img, (
            self.passive_glow_button_img.get_size()[0] * 0.8, self.passive_glow_button_img.get_size()[1] * 0.8))


        # Координаты и параметры для отрисовки изображений
        self.x_buttons, self.y_buttons = self.screen.get_rect().midtop
        self.x_player_money, self.y_player_money = self.screen.get_rect().topright
        self.x_player_money -= 60
        self.y_player_money += 20
        self.choosing_buttons_poss = {
            "AT_pos": (self.x_buttons - self.active_bomb_button_img.get_rect().size[0] * 1.5, self.y_buttons + 30),
            "BT_pos": (self.x_buttons, self.y_buttons + 30),
            "GT_pos": (self.x_buttons + self.active_bomb_button_img.get_rect().size[0] * 1.5, self.y_buttons + 30)
        }
        self.text_color = (0, 0, 0)

        # Кнопки
        self.choosing_buttons = {
            "Arrow": Button(self.choosing_buttons_poss["AT_pos"][0], self.choosing_buttons_poss["AT_pos"][1],
                            self.active_arrow_button_img, 1),
            "Bomb": Button(self.choosing_buttons_poss["BT_pos"][0], self.choosing_buttons_poss["BT_pos"][1],
                           self.active_bomb_button_img, 1),
            "Glow": Button(self.choosing_buttons_poss["GT_pos"][0], self.choosing_buttons_poss["GT_pos"][1],
                           self.active_glow_button_img, 1)
        }
        self.cancel_button = Button(0, 0, self.screen, 1, mouse_type=2)

        # Флажки
        self.is_choose = False
        self.choose_menu_state = False
        self.pressed_index = None

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

        # конфигурация уровня
        with open("levels/level" + str(self.level) + "/design.txt", "r") as level_design:
            design = level_design.read().split()
            for i in range(int(design[1])):
                x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
                self.towers += [TowerSpot(x, y, self.opponents)]

    def choosing_buttons_draw(self):
        """
        Отрисовка кнопок выбора башни для постройки
        """
        self.choosing_buttons["Arrow"].draw(self.screen)
        self.choosing_buttons["Bomb"].draw(self.screen)
        self.choosing_buttons["Glow"].draw(self.screen)

    def check_upgrade(self, tower_obj):
        """
        Обработчик улучшения башни
        :param tower_obj: объект башни
        """
        if not tower_obj.sprite == "TowerSpot":
            if self.player_money >= tower_obj.upgrade_cost:
                self.player_money -= tower_obj.upgrade_cost
                tower_obj.upgrade()
                print(self.player_money)
            else:
                self.text_color = (255, 0, 0)
                print("You haven't got a money")
        elif tower_obj.sprite == "TowerSpot":
            tower_obj.is_activate = False

    def check_money(self, tower_obj):
        """
        Проверка наличия соотвтетствующего количества валюты у игрока
        :param tower_obj: объект башни
        :return: строка-маркер отсутствия валюты
        """
        if self.player_money >= tower_obj.cost:
            self.player_money -= tower_obj.cost
            tower_obj.is_activate = True
            self.choose_menu_state = False
            self.pressed_index = None
            print(self.player_money)
        else:
            tower_obj.is_activate = True
            self.choose_menu_state = False
            self.text_color = (255, 0, 0)
            print("No money")
            return "No money"

    def change_buttons_img(self):
        if self.player_money < ArrowTower.cost:
            self.choosing_buttons["Arrow"].image = self.passive_arrow_button_img
        else:
            self.choosing_buttons["Arrow"].image = self.active_arrow_button_img

        if self.player_money < BombTower.cost:
            self.choosing_buttons["Bomb"].image = self.passive_bomb_button_img
        else:
            self.choosing_buttons["Bomb"].image = self.active_bomb_button_img

        if self.player_money < GlowTower.cost:
            self.choosing_buttons["Glow"].image = self.passive_glow_button_img
        else:
            self.choosing_buttons["Glow"].image = self.active_glow_button_img

    def draw(self):
        """
        Основная отрисовка уровня
        """
        self.screen.blit(self.background_img, (0, 0))
        """Отрисовка шкалы здоровья игрока"""
        pygame.draw.rect(self.screen, (255, 0, 0), (250, 8, self.player_health * 20, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (250, 8, 400, 20), 3)

        self.draw_text("HP: " + str(self.player_health), self.text_color, 20, 200,
                       self.y_player_money)
        self.draw_text("Money: " + str(self.player_money), self.text_color, 20, self.x_player_money,
                       self.y_player_money)
        self.text_color = (0, 0, 0)

        for i in range(len(self.towers)):
            if self.towers[i].is_activate:
                self.towers[i].check_cause()

            self.towers[i].pressing()

            self.change_buttons_img()

            if self.towers[i].is_pressed:
                self.pressed_index = i

            if self.towers[i].is_pressed or self.choose_menu_state:
                if self.towers[self.pressed_index].is_activate and not self.choose_menu_state:
                    self.check_upgrade(self.towers[self.pressed_index])

                elif self.towers[self.pressed_index].is_activate and self.choose_menu_state:
                    self.choose_menu_state = False

                elif not self.towers[self.pressed_index].is_activate:
                    self.choose_menu_state = True
                    if self.choosing_buttons["Arrow"].is_pressed():
                        self.towers[self.pressed_index] = ArrowTower(self.towers[self.pressed_index].x,
                                                                     self.towers[self.pressed_index].y,
                                                                     self.towers[self.pressed_index].enemy_list)
                        if self.check_money(self.towers[self.pressed_index]) == "No money":
                            self.towers[self.pressed_index] = TowerSpot(self.towers[self.pressed_index].x,
                                                                        self.towers[self.pressed_index].y,
                                                                        self.towers[self.pressed_index].enemy_list)
                            self.pressed_index = None

                    elif self.choosing_buttons["Bomb"].is_pressed():
                        self.towers[self.pressed_index] = BombTower(self.towers[self.pressed_index].x,
                                                                    self.towers[self.pressed_index].y,
                                                                    self.towers[self.pressed_index].enemy_list)
                        if self.check_money(self.towers[self.pressed_index]) == "No money":
                            self.towers[self.pressed_index] = TowerSpot(self.towers[self.pressed_index].x,
                                                                        self.towers[self.pressed_index].y,
                                                                        self.towers[self.pressed_index].enemy_list)
                            self.pressed_index = None

                    elif self.choosing_buttons["Glow"].is_pressed():
                        self.towers[self.pressed_index] = GlowTower(self.towers[self.pressed_index].x,
                                                                    self.towers[self.pressed_index].y,
                                                                    self.towers[self.pressed_index].enemy_list)
                        if self.check_money(self.towers[self.pressed_index]) == "No money":
                            self.towers[self.pressed_index] = TowerSpot(self.towers[self.pressed_index].x,
                                                                        self.towers[self.pressed_index].y,
                                                                        self.towers[self.pressed_index].enemy_list)
                            self.pressed_index = None

                    self.choosing_buttons_draw()

                    if self.cancel_button.is_pressed():
                        self.choose_menu_state = False

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
            self.opponents += opp.move_opponent(self.level_name)
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
            num_wave_opp = 0  # считает, сколько противников появится в этой волне
            for i in range(len(self.spawn_list[self.wave])):
                if (not self.wave_timer % self.spawn_list[self.wave][i][3]) and (self.spawn_list[self.wave][i][0] > 0):
                    self.spawn_list[self.wave][i][0] -= 1
                    for opp in OPPONENT_CLASSES_LIST:
                        if opp.__name__ == self.spawn_list[self.wave][i][1]:
                            self.opponents += [opp(self.spawn_list[self.wave][i][2])]
                num_wave_opp += self.spawn_list[self.wave][i][0]
            self.wave_timer += 1
            if num_wave_opp == 0:  # если эта волна кончилась, запускается следующая
                self.wave += 1
                self.wave_timer = 0


class Button:
    def __init__(self, x, y, image, scale, mouse_type=0):
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
        self.mouse_type = mouse_type
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def is_pressed(self):
        """
        Обработчик нажатия на кнопку, а также отрисовщик кнопки.
        :return: состояние кнопки (нажата или нет)
        """
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[self.mouse_type] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[self.mouse_type]:
            self.clicked = False

        return action

    def draw(self, surface):
        """
        Отрисовка кнопки
        :param surface: поверхность отрисовки
        """
        surface.blit(self.image, (self.rect.x, self.rect.y))
