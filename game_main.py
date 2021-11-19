import pygame
from game_constants import *
import pygame.draw as dr
import game_visualisation as vis


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        self.level = 0
        self.tower_types = [0] * 999
        self.towers = []

        finished = False
        while not finished:
            for our_event in pygame.event.get():
                if our_event.type == pygame.QUIT:
                    finished = True
                elif our_event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                else:
                    pass  # FIXME: self.level выбирается на пользовательском интерфейсе
            vis.draw_background(screen, self.level, self.tower_types)
            for elem in self.towers:
                elem.check_cause()
            pygame.display.update()
            clock.tick(30)
        pygame.quit()


gggg = Game()
