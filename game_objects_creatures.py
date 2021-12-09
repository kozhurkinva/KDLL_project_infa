import math
import os.path as path

import pygame  # FIXME пока не доделан vis + мб не всё нужно импортить


class Creature:
    def __init__(self, x=999999999999999, y=999999999999999):
        """
        Инициализация класса Creature (все живые существа, способные стоять на карте).
        У каждого есть показатели здоровья, урона и скорости, соответствующая им типизация,
        а также прикреплённый к ним список летящих в него в данный момент снарядов, перемещающихся вместе с ними
        """
        self.WIDTH, self.HEIGHT = 800, 600
        self.hp = 0
        self.dmg = 0
        self.speed = 0
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.types = []
        self.projectiles = []
        self.occupied = False  # отвечает за то,сражается ли данное существо в данный момент
        self.alive = True
        self.alpha = 1
        self.hp_bar_limit = self.hp  # используется для обозначения рамок строки здоровья (не меняется в процессе игры)
        self.sprite = ""

    def take_damage(self, dmg):
        """
        Функция получения существом урона в количестве dmg. В случае нехватки очков жизни вызывает смерть существа.
        """
        pygame.mixer.Sound("takedam1.wav").play()
        pygame.mixer.Sound("takedam1.wav").stop()
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        """ Существо перестаёт считаться живым, после чего его удалят из числа существ в main-е"""
        self.alive = False

    def draw(self, screen):
        """ Рисует живое существо """
        img = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        screen.blit(img, (self.x, self.y))
        ''' рисует hp bar и его рамку '''
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y + 50, self.hp / self.alpha * img.get_width(), 10))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y + 50, img.get_width(), 10), 3)

    def fight(self, enemy):
        """
        Проверяет наличие потенциальных противников (Ally/Opponent) и в случае нахождения поднимает флаг
        .occupied, останавливая продвижение Opponent-ов; при этом 'сражающимся' будет наноситься урон в соответствии
        с их параметрами dmg
        """
        if enemy == 0:
            self.occupied = False
        elif (self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2 <= 3600 and not self.occupied:
            if "flying" not in self.types:
                self.occupied = True
                enemy.occupied = True
                self.take_damage(enemy.dmg)
                enemy.take_damage(self.dmg)


class Ally(Creature):
    def __init__(self, x, y):
        super().__init__(x, y)


class Blue(Ally):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dmg = 0.1
        self.hp = 100
        self.alpha = 100
        self.sprite = "Blue"


class Opponent(Creature):
    def __init__(self, group="alpha"):
        super().__init__()
        self.move_an = "-"
        self.group = group
        self.player_damage = 1
        self.distance = "-"
        self.finished = False

    def move_opponent(self, level_name):
        map_types = type(self).__mro__
        k = 0
        file = "levels/" + level_name + "/" + str(map_types[0].__name__) + "_" + self.group + "_move_map.txt"
        while not path.exists(file):
            k += 1
            file = "levels/" + level_name + "/" + str(map_types[k].__name__) + "_" + self.group + "_move_map.txt"
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
            level_map[int(self.x / self.WIDTH * len(level_map[1]))][int(self.y / self.HEIGHT * (len(level_map) - 1))])
        self.distance -= self.speed
        if self.distance % 40 < 20:
            self.sprite = self.sprite[:-1] + "1"
        else:
            self.sprite = self.sprite[:-1] + "2"

    def move(self, an="-"):
        """FIXME

        :param an: при окончании движения принимает значение stop, затем враг "умирает", а герой получает урон
        :return:
        """
        if not self.occupied:
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
            if self.vx >= 0:
                self.sprite = "R" + self.sprite[1:]
            else:
                self.sprite = "L" + self.sprite[1:]
        return 0


class Warrior(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 12
        self.dmg = 1
        self.speed = 1
        self.loot = 5
        self.alpha = 12  # коэфициент для растяжения hp bar по длине изображения
        self.sprite = "RWarrior1"


class Bird(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 8
        self.dmg = 1
        self.speed = 2
        self.loot = 7
        self.player_damage = 2
        self.alpha = 8  # коэфициент для растяжения hp bar по длине изображения
        self.sprite = "RBird1"
        self.types += ["flying"]


class HealingMage(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 150
        self.dmg = 5
        self.speed = 0.5
        self.loot = 70
        self.player_damage = 15
        self.alpha = 150  # коэфициент для растяжения hp bar по длине изображения
        self.sprite = "RHealingMage1"
        self.types += ["healing_aura", "spawns"]
        self.spawned_creature = "ForestSpirit"


class DefenseMage(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 500
        self.dmg = 7
        self.speed = 0.5
        self.loot = 100
        self.player_damage = 15
        self.alpha = 500  # коэфициент для растяжения hp bar по длине изображения
        self.sprite = "RDefenseMage1"
        self.types += ["protecting_aura", "spawns"]
        self.spawned_creature = "Golem"


class DamageMage(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 450
        self.dmg = 10
        self.speed = 0.75
        self.loot = 130
        self.player_damage = 15
        self.alpha = 450  # коэфициент для растяжения hp bar по длине изображения
        self.sprite = "RDamageMage1"
        self.types += ["battle_aura", "spawns"]
        self.spawned_creature = "FireSpirit"


class ForestSpirit(Opponent):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 3
        self.dmg = 5
        self.speed = 3
        self.loot = 2
        self.player_damage = 2
        self.alpha = 3  # коэфициент для растяжения hp bar по длине изображения
        self.sprite = "RForestSpirit1"
        self.types += ["healing_aura"]


OPPONENT_CLASSES_LIST = (Opponent, Warrior, Bird, HealingMage, DefenseMage, DamageMage)
