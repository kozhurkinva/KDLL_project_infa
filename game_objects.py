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
