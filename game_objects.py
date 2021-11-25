import math
import os.path as path
import game_constants as g_c


class Tower:
    def __init__(self, x, y, cause, enemy_list):
        """
        Инициализация класса Tower (все возможные башни).
        У каждой есть своё положение на карте (x, y), причина срабатывания её действия (cause), стоимость её постройки
        (cost), время, которое должно пройти до возможности срабатывания следующего действия (reload_time), расстояние,
        на котором башня детектит происходящее (range) и каждой передаётся список существующих на данный мамент врагов.
        Также башни имеют атрибут charged_time, хранящий в себе время простоя башни с последнего действия
        """
        self.x = x
        self.y = y
        self.cause = cause
        self.ready_for_action = False
        self.cost = 0
        self.reload_time = 1
        self.charged_time = 0
        self.range = 0
        self.enemy_list = enemy_list

    def check_cause(self):
        """
        Проверяет выполнение личного условия башни, изменяет в связи с этим флаг ready_for_action.
        Возможные условия:
        always_ready - готова работать вне зависимости от внешних условий и нуждается лишь во времени на перезарядку
        enemy_in_range - враг находится в радиусе поражения башни
        *_enemy_in_range - особый подвид врага * (определяется через его type) находится в радиусе поражения башни

        В случае выполнения личного условия срабатывания и прохождения достаточного для перезарядки времени, функция
        вызывает срабатывание особого для башни действия (action).
        """
        closest_enemy = None
        self.charged_time += 1  # reloading
        if self.cause == "always_ready":
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
            self.charged_time = 0
            self.ready_for_action = False
            self.action(closest_enemy)

    def action(self, potential_closest_enemy_or_some_other_variable_from_checker):
        """
        Непосредственно выполняемое башней действие, уникальное для каждой
        :param potential_closest_enemy_or_some_other_variable_from_checker: передаёт ближайшего к финишу врага,
        доступного для атак, или какой-либо другой параметр башни или окружающей среды, полученный в ходе работы чекера
        """
        pass


class ArrowTower(Tower):
    def __init__(self, x, y, enemy_list):
        super().__init__(x, y, "enemy_in_range", enemy_list)
        self.cost = 10
        self.range = 100
        self.reload_time = 10

    def action(self, closest_enemy):
        closest_enemy.projectiles.append(
            BallisticBullet("arrow", self.x, self.y))  # FIXME координаты вылета пули != x y, а зависят от них


class GunTower(Tower):
    def __init__(self, x, y, enemy_list):
        super().__init__(x, y, "enemy_in_range", enemy_list)
        self.cost = 15
        self.range = 75
        self.reload_time = 8


class BombTower(Tower):
    def __init__(self, x, y, enemy_list):
        super().__init__(x, y, "ground_enemy_in_range", enemy_list)
        self.cost = 25
        self.range = 60
        self.reload_time = 15


class BallisticBullet:
    def __init__(self, sprite, x, y):
        pass


class StraightBullet:
    pass


class Warrior:
    def __init__(self):
        """
        Инициализация класса Warrior (все живые существа, способные стоять на карте).
        У каждого есть показатели здоровья, урона и скорости, соответствующая им типизация,
        а также прикреплённый к ним список летящих в него в данный момент снарядов, перемещающихся вместе с ними
        """
        self.hp = 0
        self.dmg = 0
        self.speed = 0
        self.types = []
        self.projectiles = []


class Opponent(Warrior):
    def __init__(self, group='alpha'):
        super().__init__()
        self.move_an = '-'
        self.x = '-'
        self.y = '-'
        self.group = group
        # self.distance = 0  #  FIXME self.distance достаётся из файла

    def move_opponent(self):
        map_types = type(self).__mro__
        k = 0
        file = 'maps/now/' + str(map_types[0].__name__) + self.group + '_move_map.txt'
        while not path.exists(file):
            k += 1
            file = 'maps/now/' + str(map_types[k].__name__) + self.group + '_move_map.txt'
        with open(file) as map_file:
            MAP = []
            for i in (map_file.read()).split('\n'):
                MAP += i.split()
        if self.x == '-':
            self.x = MAP[-1][0]
            self.y = MAP[-1][1]
        self.move(MAP[int(self.x / g_c.WIDTH * len(MAP[0]))][int(self.y / g_c.HEIGHT * (len(MAP) - 1))])

    def move(self, an='-'):
        if an == 'stop':
            pass
            # FIXME тут ГГ должен получить урон, + self.death()
        elif an != '-':
            self.move_an = float(an)
        self.x += self.speed * math.cos(self.move_an)
        self.y += self.speed * math.sin(self.move_an)
