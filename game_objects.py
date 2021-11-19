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
        if self.cause == "always_ready":
            self.ready_for_action = True
        elif self.cause == "enemy_in_range":
            pass  # FIXME
        elif self.cause == "ground_enemy_in_range":
            pass

        if self.charged_time >= self.reload_time and self.ready_for_action:
            self.charged_time = 0
            self.ready_for_action = False
            self.action()

    def reload(self):
        self.charged_time += 1

    def action(self):
        pass


class ArrowTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, "enemy_in_range")
        self.cost = 10
        self.range = 100
        self.reload_time = 10

    def action(self):
        pass


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
    pass


class StraightBullet:
    pass


class Warrior:
    def __init__(self):
        self.hp = 0
        self.dmg = 0
        self.speed = 0


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
