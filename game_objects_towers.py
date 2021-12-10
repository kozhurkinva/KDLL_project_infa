import pygame.draw

import game_objects_projectiles as o_p


class Tower:
    def __init__(self, x, y, cause, enemy_list, sprite):
        """
        Инициализация класса Tower (все возможные башни).
        У каждой есть своё положение на карте (x, y), причина срабатывания её действия (cause), стоимость её постройки
        (cost), время, которое должно пройти до возможности срабатывания следующего действия (reload_time), расстояние,
        на котором башня детектит происходящее (range), у некоторых - наносимый башней урон (dmg)
        и каждой передаётся список существующих на данный мамент врагов + название файла с картинкой башни.
        Также башни имеют атрибут charged_time, хранящий в себе время простоя башни с последнего действия.
        """
        self.x = x
        self.y = y
        self.cause = cause
        self.level = 1
        self.ready_for_action = False
        self.cost = 0
        self.dmg = 0
        self.reload_time = 1
        self.charged_time = 0
        self.range = 0
        self.enemy_list = enemy_list
        self.sprite = sprite

        # for clicking and choosing a type of the tower
        self.clicked = False
        self.is_activate = False
        self.is_pressed = False
        self.default_image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()

        # for drawing
        # self.image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        self.image = self.default_image
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y)

    def check_cause(self):
        """
        Проверяет выполнение личного условия башни, изменяет в связи с этим флаг ready_for_action.
        Возможные условия:
        never_ready - башня никогда не активирует self.action()
        always_ready - готова работать вне зависимости от внешних условий и нуждается лишь во времени на перезарядку
        enemy_in_range - враг находится в радиусе поражения башни
        *_enemy_in_range - особый подвид врага * (определяется через его type) находится в радиусе поражения башни

        В случае выполнения личного условия срабатывания и прохождения достаточного для перезарядки времени, функция
        вызывает срабатывание особого для башни действия (action).
        """
        self.glow_up()
        closest_enemy = None
        self.charged_time += 1  # reloading
        self.ready_for_action = False
        if self.cause == "never_ready":
            pass
        elif self.cause == "always_ready":
            self.ready_for_action = True
        elif self.cause == "enemy_in_range":
            closest_enemy = None
            range_for_closest = 999999999999999
            for enemy in self.enemy_list:
                if (self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2 <= self.range ** 2:
                    self.ready_for_action = True
                    if enemy.distance <= range_for_closest:
                        closest_enemy = enemy
                        range_for_closest = enemy.distance
        elif self.cause == "ground_enemy_in_range":
            closest_enemy = None
            range_for_closest = 999999999999999
            for enemy in self.enemy_list:
                if (self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2 <= self.range ** 2 and "flying" not in enemy.types:
                    self.ready_for_action = True
                    if enemy.distance <= range_for_closest:
                        closest_enemy = enemy
                        range_for_closest = enemy.distance

        if self.charged_time >= self.reload_time and self.ready_for_action:
            self.action(closest_enemy)
            self.charged_time = 0
            self.ready_for_action = False

    def glow_up(self):
        """ Функция для возможного изменения характеристик или внешнего вида башен в зависимости от внешних факторов"""
        pass

    def action(self, potential_closest_enemy_or_some_other_variable_from_checker):
        """
        Непосредственно выполняемое башней действие, уникальное для каждой
        :param potential_closest_enemy_or_some_other_variable_from_checker: передаёт ближайшего к финишу врага,
        доступного для атак, или какой-либо другой параметр башни или окружающей среды, полученный в ходе работы чекера
        """
        pass

    def relocate(self, direction):
        """ Меняет ориентацию башни, чтобы та смотрела в сторону врага, в которого стреляет (direction) """
        self.sprite = direction + self.sprite[1:]
        self.image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y)

    def draw(self, display):
        """
        Отрисовывает изображение башни на поверххности display
        :param display: поверхность отрисовки
        """
        display.blit(self.image, (self.image_rect.x, self.image_rect.y))

    def pressing(self):
        """
        Обработчик нажатия на башню
        :return: флажок состояния кнопки, нажата или нет
        """
        self.is_pressed = False
        pos = pygame.mouse.get_pos()

        if self.image_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.is_pressed = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False


class TowerSpot(Tower):
    def __init__(self, x, y, enemy_list):
        """ Пустое место для башен """
        super().__init__(x, y, "never_ready", enemy_list, "TowerSpot")
        self.cost = 0
        self.upgrade_cost = 0

    def upgrade(self):
        pass


class ArrowTower(Tower):
    cost = 10

    def __init__(self, x, y, enemy_list):
        """ Инициализация подкласса Tower - ArrowTower. Башня лучников выпускает стрелы """
        super().__init__(x, y, "enemy_in_range", enemy_list, "LArrowTower1")
        self.level = 1
        self.cost = ArrowTower.cost
        self.upgrade_cost = 20
        self.range = 150
        self.reload_time = 40
        self.dmg = 3

    def upgrade(self):
        """ Улучшение башни лучников (увеличивает характеристики и меняет спрайт), запускает заново перезарядку """
        self.charged_time = 0
        if self.level == 1:
            self.upgrade_cost = 35
            self.sprite = self.sprite[0] + "ArrowTower2"
            self.range = 170
            self.reload_time = 35
            self.dmg = 5
        elif self.level == 2:
            self.upgrade_cost = 0
            self.sprite = self.sprite[0] + "ArrowTower3"
            self.range = 180
            self.reload_time = 30
            self.dmg = 6
        self.level += 1
        self.image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y)

    def action(self, closest_enemy):
        """ Выпускает стрелу в closest_enemy, также в случае необходимости меняет направление обзора на врага """
        if closest_enemy.x > self.x:
            sprite = "RArrow"
            self.relocate("R")
        else:
            sprite = "LArrow"
            self.relocate("L")
        closest_enemy.projectiles.append(
            o_p.BallisticProjectile(sprite, self.dmg, self.x, self.y, 3, closest_enemy, 0.17))


class GunTower(Tower):
    cost = 15

    def __init__(self, x, y, enemy_list):
        """ Инициализация подкласса Tower - GunTower. Башня стрелков выпускает пули """
        super().__init__(x, y, "enemy_in_range", enemy_list, "LGunTower1")
        self.cost = GunTower.cost
        self.upgrade_cost = 20
        self.range = 100
        self.reload_time = 13
        self.dmg = 2

    def upgrade(self):
        """ Улучшение башни стрелков (увеличивает характеристики и меняет спрайт), запускает заново перезарядку """
        self.charged_time = 0
        if self.level == 1:
            self.upgrade_cost = 35
            self.sprite = self.sprite[0] + "GunTower2"
            self.range = 125
            self.reload_time = 11
            self.dmg = 2.4
        elif self.level == 2:
            self.upgrade_cost = 0
            self.sprite = self.sprite[0] + "GunTower3"
            self.range = 150
            self.reload_time = 9
            self.dmg = 3
        self.level += 1
        self.image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y)

    def action(self, closest_enemy):
        """ Выпускает пулю в closest_enemy """
        if closest_enemy.x > self.x:
            sprite = "RBullet"
            self.relocate("R")
        else:
            sprite = "LBullet"
            self.relocate("L")
        closest_enemy.projectiles.append(o_p.StraightProjectile(sprite, self.dmg, self.x, self.y, 5, closest_enemy))


class BombTower(Tower):
    cost = 25

    def __init__(self, x, y, enemy_list):
        """ Инициализация подкласса Tower - BombTower. Башня подрывников выпускает не самонаводящиеся бомбы """
        super().__init__(x, y, "ground_enemy_in_range", enemy_list, "LBombTower1")
        self.cost = BombTower.cost
        self.upgrade_cost = 30
        self.range = 90
        self.reload_time = 120
        self.dmg = 20

    def upgrade(self):
        """ Улучшение башни подрывников (увеличивает характеристики и меняет спрайт), запускает заново перезарядку """
        self.charged_time = 0
        if self.level == 1:
            self.upgrade_cost = 35
            self.sprite = self.sprite[0] + "BombTower2"
            self.range = 110
            self.reload_time = 110
            self.dmg = 30
        elif self.level == 2:
            self.upgrade_cost = 50
            self.sprite = self.sprite[0] + "BombTower3"
            self.range = 90
            self.reload_time = 130
            self.dmg = 45
        self.level += 1
        self.image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y)

    def action(self, closest_enemy):
        """ Выпускает бомбу в closest_enemy (наносит урон по площади), меняет ориентацию при нужде """
        if closest_enemy.x > self.x:
            self.relocate("R")
        else:
            self.relocate("L")
        o_p.global_projectiles.append(
            o_p.BombProjectile("Bomb", self.dmg, self.x, self.y, 2, closest_enemy, 0.17, self.enemy_list))


class GlowTower(Tower):
    cost = 25

    def __init__(self, x, y, enemy_list):
        """ Инициализация подкласса Tower - GlowTower. Светящаяся башня выпускает усиленные временем снаряды """
        super().__init__(x, y, "enemy_in_range", enemy_list, "1GlowTower1")
        self.cost = GlowTower.cost
        self.upgrade_cost = 30
        self.range = 100
        self.reload_time = 100
        self.dmg = 5
        self.dmg_up = 1.7  # коэффициент, на который умножается кол-во секунд простоя

    def glow_up(self):
        """ Изменяет внешний вид маяка в зависимости от времени простоя (спрайт зависит от первой цифры) """
        if self.charged_time > 3 * self.reload_time:
            self.sprite = "4" + self.sprite[1:]
        elif self.charged_time > 2 * self.reload_time:
            self.sprite = "3" + self.sprite[1:]
        elif self.charged_time > self.reload_time:
            self.sprite = "2" + self.sprite[1:]
        else:
            self.sprite = "1" + self.sprite[1:]
        self.image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y)

    def upgrade(self):
        """
        Улучшение светящуюся башню (увеличивает характеристики и меняет спрайт), запускает заново перезарядку,
        стоимость и характеристики зависят от номера улучшения (self.level)
        """
        self.charged_time = 0
        if self.level == 1:
            self.upgrade_cost = 35
            self.sprite = "1GlowTower2"
            self.range = 125
            self.reload_time = 100
            self.dmg = 7
            self.dmg_up = 2.5
        elif self.level == 2:
            self.upgrade_cost = 0
            self.sprite = "1GlowTower3"
            self.range = 150
            self.reload_time = 100
            self.dmg = 10
            self.dmg_up = 4
        self.level += 1
        self.image = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y)

    def action(self, closest_enemy):
        """
        Выпускает снаряд-свечение, урон которого зависит от self.charged_time
        (каждую секунду простоя урон увеличивается на 1, но не больше, чем на 2 * self.reload_time)
        """
        if self.charged_time > 3 * self.reload_time:
            self.charged_time = 3 * self.reload_time
        closest_enemy.projectiles.append(
            o_p.StraightProjectile(self.sprite[0] + "Glow",
                                   self.dmg + self.dmg_up * (self.charged_time - self.reload_time) / 60, self.x, self.y,
                                   1, closest_enemy))
