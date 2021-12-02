import math
import os.path as path

import pygame.draw  # FIXME пока не доделан vis + мб не всё нужно импортить

import game_constants as g_c


class Creature:
    def __init__(self):
        """
        Инициализация класса Creature (все живые существа, способные стоять на карте).
        У каждого есть показатели здоровья, урона и скорости, соответствующая им типизация,
        а также прикреплённый к ним список летящих в него в данный момент снарядов, перемещающихся вместе с ними
        """
        self.hp = 0

        self.dmg = 0
        self.speed = 0
        self.vx = 0
        self.vy = 0
        self.types = []
        self.projectiles = []
        self.alive = True
        self.alpha = 1

    def take_damage(self, dmg):
        """
        Функция получения существом урона в количестве dmg. В случае нехватки очков жизни вызывает смерть существа.
        """
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        """ Существо перестаёт считаться живым, после чего его удалят из числа существ в main-е"""
        self.alive = False

    def draw(self, screen):
        """ Рисует живое существо """
        img = pygame.image.load("Textures/" + str(type(self).__mro__[0].__name__) + ".png").convert_alpha()
        screen.blit(img, (self.x, self.y))
        ''' рисует hp bar и его рамку '''
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y + 50, self.hp*self.alpha, 10))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y + 50, self.hp_bar_limit*self.alpha, 10), 2)



class Opponent(Creature):
    def __init__(self, group="alpha"):
        super().__init__()
        self.move_an = "-"
        self.x = 999999999999999
        self.y = 999999999999999
        self.group = group
        self.player_damage = 1
        self.distance = "-"
        self.finished = False

    def move_opponent(self, level_name):
        map_types = type(self).__mro__
        k = 0
        file = "maps/" + level_name + "/" + str(map_types[0].__name__) + "_" + self.group + "_move_map.txt"
        while not path.exists(file):
            k += 1
            file = "maps/" + level_name + "/" + str(map_types[k].__name__) + "_" + self.group + "_move_map.txt"
        with open(file) as map_file:
            map_file_lines = (map_file.read()).split("\n")
            if self.distance == "-":
                self.distance = float(map_file_lines[0][0])
            level_map = []
            for i in map_file_lines[1:-1]:
                level_map += [i.split()]
        if self.x == 999999999999999:
            self.x = float(level_map[-1][0])
            self.y = float(level_map[-1][1])
            print("I've started", self.x, self.y)
        self.move(
            level_map[int(self.x / g_c.WIDTH * len(level_map[1]))][int(self.y / g_c.HEIGHT * (len(level_map) - 1))])
        self.distance -= self.speed

    def move(self, an="-"):
        """FIXME

        :param an: при окончании движения принимает значение stop, затем враг "умирает", а герой получает урон
        :return:
        """
        if an == "stop":
            self.alive = False
            self.finished = True

        elif an != "-":
            x = float(an.split(";")[0])
            y = float(an.split(";")[1])
            dx = x - self.x
            dy = y - self.y
            if dx != 0:
                self.move_an = math.atan(dy / dx) + math.pi * int(dx < 0)
            else:
                self.move_an = math.pi / 2 * (int(dy > 0) - int(dy < 0))
        self.vx = self.speed * math.cos(self.move_an)
        self.vy = self.speed * math.sin(self.move_an)
        self.x += self.vx
        self.y += self.vy
        return 0


class Warrior(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 10
        self.dmg = 1
        self.speed = 1
        self.alpha = 7 # коэфициент для растяжения hp bar по длине изображения
        self.hp_bar_limit = self.hp # используется для обозначения рамок строки здоровья (не меняется в процессе игры)


class Bird(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 5
        self.dmg = 1
        self.speed = 20
        self.player_damage = 2
        self.alpha = 8 # коэфициент для растяжения hp bar по длине изображения
        self.hp_bar_limit = self.hp # используется для обозначения рамок строки здоровья (не меняется в процессе игры)
        self.types += ["flying"]
