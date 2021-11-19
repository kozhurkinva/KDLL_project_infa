import math
import os.path as path
import game_constants as g_c


class Tower:
    def __init__(self, x, y, cause):
        self.x = x
        self.y = y
        self.cause = cause
        self.ready_for_action = False
        self.cost = 0
        self.reload_time = 1
        self.charged_time = 0

    def check_cause(self):
        closest_enemy = None
        self.charged_time += 1  # reloading
        if self.cause == "always_ready":
            self.ready_for_action = True
        elif self.cause == "enemy_in_range":
            closest_enemy = Warrior
            pass  # FIXME
        elif self.cause == "ground_enemy_in_range":
            pass

        if self.charged_time >= self.reload_time and self.ready_for_action:
            self.charged_time = 0
            self.ready_for_action = False
            self.action(closest_enemy)

    def action(self, potential_closest_enemy_or_some_other_variable_from_checker):
        pass


class ArrowTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, "enemy_in_range")
        self.cost = 10
        self.range = 100
        self.reload_time = 10

    def action(self, closest_enemy):
        closest_enemy.projectiles.append(
            BallisticBullet("arrow", self.x, self.y))  # FIXME координаты вылета пули != x y, а зависят от них


class GunTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, "enemy_in_range")
        self.cost = 15
        self.range = 75
        self.reload_time = 8


class BombTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, "ground_enemy_in_range")
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
        У каждого есть показатели здоровья, урона и скорости, а также прикреплённый к ним список летящих в него в
        данный момент снарядов, перемещающихся вместе с ними
        """
        self.hp = 0
        self.dmg = 0
        self.speed = 0
        self.projectiles = []


class Opponent(Warrior):
    def __init__(self, group='alpha'):
        super().__init__()
        self.move_an = '-'
        self.x = '-'
        self.y = '-'
        self.group = group

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
