import pygame
from game_constants import *
import pygame.draw as dr
from game_visualisation import *
import game_visualisation


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        self.level = 0
        self.tower_types = [0] * 999
        self.towers = []
        self.button = Button(x=50, y=50, image=pygame.image.load("Textures/StartButton.png").convert_alpha(), scale=0.5)
        self.button1 = Button(x=500, y=50, image=pygame.image.load("Textures/StopButton.png").convert_alpha(), scale=0.5)

        finished = False
        while not finished:

            draw_background(screen, self.level, self.tower_types)

            if self.button.is_pressed(screen):
                print("Game starts!")
            if self.button1.is_pressed(screen):
                finished = True

            for our_event in pygame.event.get():
                if our_event.type == pygame.QUIT:
                    finished = True
                elif our_event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                else:
                    pass  # FIXME: self.level выбирается на пользовательском интерфейсе

            for elem in self.towers:
                elem.check_cause()

            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()

gggg = Game()
