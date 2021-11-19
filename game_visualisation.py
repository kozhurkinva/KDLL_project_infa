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
    archer_tower_img = pygame.image.load("Textures/ArcherTower.png").convert_alpha()
    level_design = open("level_designs.txt", "r")
    #  FIXME вынести всё куда-нибудь
    design = level_design.readlines()[level].split()
    for i in range(int(design[1])):
        x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
        if towers[i] == 0:
            screen.blit(tower_spot_img, (x, y))
        elif towers[i] == 1:
            screen.blit(archer_tower_img, (x, y))
        else:
            pass  # FIXME
