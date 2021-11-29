import math
import os.path as path

import pygame.draw  # FIXME пока не доделан vis + мб не всё нужно импортить

import game_constants as g_c


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
        dx = shot_creature.x - x
        dy = shot_creature.y - y
        self.time_of_flight = (dx ** 2 + dy ** 2) ** (1 / 2) / bullet_speed
        self.vx = dx / self.time_of_flight
        self.vy = (dy - self.a * self.time_of_flight ** 2 / 2) / self.time_of_flight

    def move(self):
        """
        Перемещает пулю по её собственной баллистической траектории + по траектории движения того, в кого стреляют,
        проверяет факт попадания (прошествия времени time_of_flight)
        """
        self.time_of_flight -= 1
        self.x += self.vx + self.shot_creature.vx
        self.y += self.vy + self.shot_creature.vy
        self.vy += self.a
        if self.time_of_flight <= 0:
            self.shot_creature.projectiles.pop(self.shot_creature.projectiles.index(self))
            self.shot_creature.take_damage(self.dmg)

    def draw(self, screen):
        """ Рисует пулю в полёте """
        pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y), 2)


class StraightBullet:
    pass
