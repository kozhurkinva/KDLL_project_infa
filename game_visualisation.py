import pygame


def draw_background(screen):
    background_img = pygame.image.load("Textures/Background.png").convert_alpha()
    screen.blit(background_img, (0, 0))
