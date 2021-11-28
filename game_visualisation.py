import pygame
from game_constants import *


class Level:
    """Рисует задний фон и места башни/места под башни
    screen - окно для рисования
    level - номер уровня
    towers - список с номерами, обозначающими виды башен
    """

    def __init__(self, level, screen):
        self.level = level
        self.screen = screen

        self.ingame_towers = []

        self.background_img = pygame.image.load("Textures/Background" + str(self.level) + ".png").convert_alpha()
        self.screen.blit(self.background_img, (0, 0))

        self.towerspot_img = pygame.image.load("Textures/TowerSpot.png").convert_alpha()
        self.towerspot_rect = self.towerspot_img.get_rect()

        self.archertower_img = pygame.image.load("Textures/ArcherTower.png").convert_alpha()
        self.archertower_rect = self.archertower_img.get_rect()

        self.images = [self.towerspot_img, self.archertower_img]

        with open("level_designs.txt", "r") as level_design:
            design = level_design.readlines()[level].split()
            for i in range(int(design[1])):
                x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
                click = Button(x, y, self.images[0], 1)
                self.ingame_towers.append(click)

    def draw(self):
        for tower in self.ingame_towers:
            if tower.is_pressed(self.screen):
                tower.image = self.images[1]


def draw_map(screen, level, towers):
    """
    Рисует задний фон и места башни/места под башни
    screen - окно для рисования
    level - номер уровня
    towers - список с номерами, обозначающими виды башен
    """
    towers_pos = []

    background_img = pygame.image.load("Textures/Background" + str(level) + ".png").convert_alpha()
    screen.blit(background_img, (0, 0))

    towerspot_img = pygame.image.load("Textures/TowerSpot.png").convert_alpha()
    towerspot_rect = towerspot_img.get_rect()

    archertower_img = pygame.image.load("Textures/ArcherTower.png").convert_alpha()
    archertower_rect = archertower_img.get_rect()

    images = [towerspot_img, archertower_img]

    with open("level_designs.txt", "r") as level_design:
        design = level_design.readlines()[level].split()
        for i in range(int(design[1])):
            x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
            towers_pos.append([x, y])

    for tower in towers_pos:
        screen.blit(images[towers[i]], tower)


# button class
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def is_pressed(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
