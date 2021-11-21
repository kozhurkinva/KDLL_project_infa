import pygame
from game_constants import *


def draw_background(screen, level, towers):
    """Рисует задний фон и места башни/места под башни
    screen - окно для рисования
    level - номер уровня
    towers - список с номерами, обозначающими виды башен
    """
    background_img = pygame.image.load("Textures/Background" + str(level) + ".png").convert_alpha()
    screen.blit(background_img, (0, 0))
    tower_spot_img = pygame.image.load("Textures/TowerSpot.png").convert_alpha()
    with open("level_designs.txt", "r") as level_design:
        design = level_design.readlines()[level].split()
        for i in range(int(design[1])):
            x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
            background_img.blit(tower_spot_img, (x, y))

def get_level_image():
    pass


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
