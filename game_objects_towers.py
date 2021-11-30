import math
import os.path as path

import pygame.draw  # FIXME пока не доделан vis + мб не всё нужно импортить

import game_constants as g_c
from game_objects_projectiles import *


class Tower:
    def __init__(self, x, y, cause, enemy_list):
        """
        Инициализация класса Tower (все возможные башни).
        У каждой есть своё положение на карте (x, y), причина срабатывания её действия (cause), стоимость её постройки
        (cost), время, которое должно пройти до возможности срабатывания следующего действия (reload_time), расстояние,
        на котором башня детектит происходящее (range), у некоторых - наносимый башней урон (dmg)
        и каждой передаётся список существующих на данный мамент врагов.
        Также башни имеют атрибут charged_time, хранящий в себе время простоя башни с последнего действия.
        """
        self.x = x
        self.y = y
        self.cause = cause
        self.ready_for_action = False
        self.cost = 0
        self.dmg = 0
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
        self.ready_for_action = False
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
            self.action(closest_enemy)
            self.charged_time = 0
            self.ready_for_action = False

    def action(self, potential_closest_enemy_or_some_other_variable_from_checker):
        """
        Непосредственно выполняемое башней действие, уникальное для каждой
        :param potential_closest_enemy_or_some_other_variable_from_checker: передаёт ближайшего к финишу врага,
        доступного для атак, или какой-либо другой параметр башни или окружающей среды, полученный в ходе работы чекера
        """
        pass


class ArrowTower(Tower):
    def __init__(self, x, y, enemy_list):
        """ Инициализация подкласса Tower - ArrowTower. Башня лучников выпускает стрелы """
        super().__init__(x, y, "enemy_in_range", enemy_list)
        self.cost = 10
        self.range = 100
        self.reload_time = 40
        self.dmg = 2

    def action(self, closest_enemy):
        """ Выпускает стрелу в closest_enemy """
        closest_enemy.projectiles.append(BallisticProjectile("Arrow", self.dmg, self.x, self.y, 3, closest_enemy, 0.17))
        # FIXME координаты вылета пули != x y, а зависят от них, скорость и ускорение - ??? (зависит от карты?)


class GunTower(Tower):
    def __init__(self, x, y, enemy_list):
        """ Инициализация подкласса Tower - GunTower. Башня стрелков выпускает пули """
        super().__init__(x, y, "enemy_in_range", enemy_list)
        self.cost = 15
        self.range = 75
        self.reload_time = 10
        self.dmg = 1

    def action(self, closest_enemy):
        """ Выпускает пулю в closest_enemy """
        closest_enemy.projectiles.append(StraightProjectile("Bullet", self.dmg, self.x, self.y, 5, closest_enemy))


class BombTower(Tower):
    def __init__(self, x, y, enemy_list):
        """ Инициализация подкласса Tower - BombTower. Башня подрывников выпускает не самонаводящиеся бомбы """
        super().__init__(x, y, "ground_enemy_in_range", enemy_list)
        self.cost = 25
        self.range = 60
        self.reload_time = 150
        self.dmg = 10

    def action(self, closest_enemy):
        """ Выпускает бомбу в closest_enemy (наносит урон по площади) """
        closest_enemy.projectiles.append(
            BombProjectile("Bomb", self.dmg, self.x, self.y, 2, closest_enemy, 0.17, self.enemy_list))


class ChargingTower(Tower):
    """ Прототип башни с уроном, зависящем от времени простоя """

    def __init__(self, x, y, enemy_list):
        super().__init__(x, y, "enemy_in_range", enemy_list)
        self.cost = 25
        self.range = 100
        self.reload_time = 25
        self.dmg = 1

    def action(self, closest_enemy):
        closest_enemy.projectiles.append(
            StraightProjectile("Arrow", self.dmg + (self.charged_time - self.reload_time) / 60, self.x, self.y, 1,
                               closest_enemy))
