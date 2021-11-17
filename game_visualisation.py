import pygame


def draw_background(screen, level, towers):
    """Рисует задний фон и места башни/места под башни
    screen - окно для рисования
    level - номер уровня
    towers - список с номерами, обозначающими виды башен
    """
    background_img = pygame.image.load("Textures/Background" + str(level) + ".png").convert_alpha()
    screen.blit(background_img, (0, 0))
    tower_spot_img = pygame.image.load("Textures/TowerSpot.png").convert_alpha()
    level_design = open("level_designs.txt", "r")
    design = level_design.readlines()[level].split()
    for i in range(int(design[1])):
        x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
        screen.blit(tower_spot_img, (x, y))
