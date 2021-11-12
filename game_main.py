import pygame
import pygame.draw as dr
import game_visualisation as vis


class Game:
    def __init__(self, money=100):
        pygame.init()
        screen = pygame.display.set_mode((1000, 600))
        clock = pygame.time.Clock()

        finished = False
        while not finished:
            for our_event in pygame.event.get():
                if our_event.type == pygame.QUIT:
                    finished = True
            pygame.display.update()
            clock.tick(30)
        pygame.quit()


gggg = Game()
