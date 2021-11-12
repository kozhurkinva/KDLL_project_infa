class WarriorTower:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ShootingTower:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bullet:
    pass


class Warrior:
    pass


class ArrowTower(ShootingTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = 10


class GunTower(ShootingTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = 15
