import pygame
from game_constants import *
import pygame.draw as dr
import game_visualisation as vis


class Game:
    def __init__(self, money=100):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        self.towers = [0] * 999

        finished = False
        while not finished:
            for our_event in pygame.event.get():
                if our_event.type == pygame.QUIT:
                    finished = True
            vis.draw_background(screen, 1, self.towers)
            pygame.display.update()
            clock.tick(30)
        pygame.quit()


gggg = Game()
