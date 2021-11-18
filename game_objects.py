import math
import os.path as path
import game_constants as g_c

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.action = None
        self.cause = None


class ArrowTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = 10


class GunTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = 15


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
        if an != '-':
            self.move_an = float(an)
        elif an == 'stop':
            pass
            # FIXME тут ГГ должен получить урон, + self.death()
        self.x += self.speed * math.cos(self.move_an)
        self.y += self.speed * math.sin(self.move_an)
