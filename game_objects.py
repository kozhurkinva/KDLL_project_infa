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
        self.dmg = 2

    def action(self, closest_enemy):
        closest_enemy.projectiles.append(
            BallisticBullet("arrow", self.dmg, self.x, self.y, 2,
                            closest_enemy,
                            1 / 6))  # FIXME координаты вылета пули != x y, а зависят от них, скорость и ускорение - ???


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
    def __init__(self, sprite, dmg, x, y, bullet_speed, shot_creature, gravity_acceleration):
        """Инициализация класса BallisticBullet - пули, летящие по баллистической траектории из точки (x,y)
        в соответствующее существо shot_creature. bullet_speed - её скорость по оси x"""
        self.shot_creature = shot_creature
        self.dmg = dmg
        self.x = x
        self.y = y
        self.a = gravity_acceleration
        self.sprite = sprite
        dx = x - shot_creature.x
        dy = y - shot_creature.y
        self.time_of_flight = (dx ** 2 + dy ** 2) ** (1 / 2) / bullet_speed
        self.vx = dx / self.time_of_flight
        self.vy = (dy + self.a * self.time_of_flight ** 2 / 2) / self.time_of_flight

    def move(self):
        """
        Перемещает пулю по её собственной баллистической траектории + по траектории движения того, в кого стреляют,
        проверяет факт попадания (прошествия времени time_of_flight)
        """
        self.time_of_flight -= 1
        self.x += self.vx + self.shot_creature.vx
        self.y += self.vy + self.shot_creature.vy
        self.vy -= self.a
        if self.time_of_flight <= 0:
            self.shot_creature.projectiles.pop(self.shot_creature.projectiles.index(self))
            self.shot_creature.take_damage(self.dmg)

    def draw(self):
        """ Рисует пулю в полёте """
        pass


class StraightBullet:
    pass


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
        self.types = []
        self.projectiles = []

    def take_damage(self, dmg):
        """
        Функция получения существом урона в количестве dmg. В случае нехватки очков жизни вызывает смерть существа.
        """
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        pass


class Opponent(Creature):
    def __init__(self, group='alpha'):
        super().__init__()
        self.move_an = '-'
        self.x = '-'
        self.y = '-'
        self.group = group
        self.distance = "-"

    def move_opponent(self):
        map_types = type(self).__mro__
        k = 0
        file = 'maps/now/' + str(map_types[0].__name__) + self.group + '_move_map.txt'
        while not path.exists(file):
            k += 1
            file = 'maps/now/' + str(map_types[k].__name__) + self.group + '_move_map.txt'
        with open(file) as map_file:
            MAP = []
            for i in ((map_file.read()).split('\n'))[1:]:
                MAP += i.split()
        if self.x == '-':
            self.x = MAP[-1][0]
            self.y = MAP[-1][1]
        if self.distance == "-":
            self.distance = float(MAP[0][0])
        self.move(MAP[int(self.x / g_c.WIDTH * len(MAP[1]))][int(self.y / g_c.HEIGHT * (len(MAP) - 1))])
        self.distance -= self.speed

    def move(self, an='-'):
        if an == 'stop':
            pass
            # FIXME тут ГГ должен получить урон, + self.death()
        elif an != '-':
            x = float(an.split(";")[0])
            y = float(an.split(";")[1])
            dx = self.x - x
            dy = self.y - y
            if dx != 0:
                self.move_an = math.atan(dy / dx) + math.pi / 2 * int(dx < 0)
            else:
                self.move_an = math.pi / 2 * (int(dy > 0) - int(dy < 0))
        self.x += self.speed * math.cos(self.move_an)
        self.y += self.speed * math.sin(self.move_an)


class Warrior(Opponent):
    def __init__(self):
        super().__init__()
        self.hp = 10
        self.dmg = 1
        self.speed = 1
