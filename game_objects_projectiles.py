import pygame.draw

global_projectiles = []  # снаряды, не привязанные к врагам


class Projectile:
    def __init__(self, sprite, dmg, x, y, shot_creature):
        """Инициализация класса Projectile - снаряда, наносящего dmg урона и летящего из точки (x,y)
        в соответствующее существо shot_creature"""
        self.shot_creature = shot_creature
        self.dmg = dmg
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self, screen):
        """ Рисует пулю в полёте """
        img = pygame.image.load("Textures/" + self.sprite + ".png").convert_alpha()
        screen.blit(img, (self.x, self.y))

    def relocate(self, direction):
        """
        Если снаряд в полёте должен поменять направление , в этой функции изменится его спрайт
        (direction принимает значения "L" и "R" и поворачивает снаряд соотв влево или вправо)
        """
        if self.sprite[0] == "R" or self.sprite[0] == "L":
            self.sprite = direction + self.sprite[1:]


class BallisticProjectile(Projectile):
    def __init__(self, sprite, dmg, x, y, projectile_speed, shot_creature, gravity_acceleration):
        """Инициализация подкласса Projectile - BallisticProjectile.
        От параметра projectile_speed зависит собственная скорость снаряда,
        от gravity_acceleration - ускорение свободного падения"""
        super().__init__(sprite, dmg, x, y, shot_creature)
        self.a = gravity_acceleration
        dx = shot_creature.x - x
        dy = shot_creature.y - y
        self.time_of_flight = (dx ** 2 + dy ** 2) ** (1 / 2) / projectile_speed
        self.vx = dx / self.time_of_flight
        self.vy = (dy - self.a * self.time_of_flight ** 2 / 2) / self.time_of_flight

    def move(self, screen):
        """
        Перемещает пулю по её собственной баллистической траектории + по траектории движения того, в кого стреляют,
        проверяет факт попадания (прошествия времени time_of_flight), при попадании наносит урон, иначе рисует снаряд
        """
        self.time_of_flight -= 1
        self.x += self.vx + self.shot_creature.vx
        self.y += self.vy + self.shot_creature.vy
        self.vy += self.a
        if self.vx + self.shot_creature.vx > 0:
            self.relocate("R")
        else:
            self.relocate("L")
        if self.time_of_flight <= 0:
            self.shot_creature.projectiles.pop(self.shot_creature.projectiles.index(self))
            self.shot_creature.take_damage(self.dmg)
        else:
            self.draw(screen)


class StraightProjectile(Projectile):
    def __init__(self, sprite, dmg, x, y, projectile_speed, shot_creature):
        """Инициализация подкласса Projectile - StraightProjectile.
        От параметра projectile_speed зависит собственная скорость снаряда"""
        super().__init__(sprite, dmg, x, y, shot_creature)
        dx = shot_creature.x - x
        dy = shot_creature.y - y
        self.time_of_flight = (dx ** 2 + dy ** 2) ** (1 / 2) / projectile_speed
        self.vx = dx / self.time_of_flight
        self.vy = dy / self.time_of_flight

    def move(self, screen):
        """
        Перемещает пулю по её собственной прямолинейной траектории + по траектории движения того, в кого стреляют,
        проверяет факт попадания (прошествия времени time_of_flight), при попадании наносит урон, иначе рисует снаряд
        """
        self.time_of_flight -= 1
        self.x += self.vx + self.shot_creature.vx
        self.y += self.vy + self.shot_creature.vy
        if self.time_of_flight <= 0:
            self.shot_creature.projectiles.pop(self.shot_creature.projectiles.index(self))
            self.shot_creature.take_damage(self.dmg)
        else:
            self.draw(screen)


class BombProjectile(BallisticProjectile):
    def __init__(self, sprite, dmg, x, y, projectile_speed, shot_creature, gravity_acceleration, enemy_list):
        """Инициализация подкласса Projectile - BallisticProjectile.
            От параметра projectile_speed зависит собственная скорость снаряда,
            от gravity_acceleration - ускорение свободного падения
            blow_radius - радиус взрыва бомбы, в котором враги получат урон"""
        super().__init__(sprite, dmg, x, y, projectile_speed, shot_creature, gravity_acceleration)
        self.enemy_list = enemy_list
        self.blow_radius = 50

    def move(self, screen):
        """
        Перемещает пулю по её собственной баллистической траектории,
        проверяет факт соприкосновения с землёй (прошествия времени time_of_flight),
        в случае соприкосновения взрывается, иначе рисует снаряд
        """
        self.time_of_flight -= 1
        self.x += self.vx
        self.y += self.vy
        self.vy += self.a
        if self.time_of_flight <= 0:
            global_projectiles.pop(global_projectiles.index(self))
            self.blow(screen)
        else:
            self.draw(screen)

    def blow(self, screen):
        """ Рисует спрайт взрыва, наносит урон врагам в радиусе взрыва """
        img = pygame.image.load("Textures/Blow.png").convert_alpha()
        screen.blit(img, (self.x, self.y))
        for opp in self.enemy_list:
            if (opp.x - self.x) ** 2 + (opp.y - self.y) ** 2 <= self.blow_radius ** 2:
                opp.take_damage(self.dmg)
