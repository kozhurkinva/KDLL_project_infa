import pygame
from game_constants import *
import pygame.draw as dr
from game_visualisation import *
import game_visualisation


class Game:
    def __init__(self):
        pygame.init()
        # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        self.level = 0
        self.tower_types = [0] * 999
        self.towers = []
        self.start_button = Button(x=50, y=400, image=pygame.image.load("Textures/StartButton.png").convert_alpha(),
                                   scale=0.5)
        self.stop_button = Button(x=600, y=400, image=pygame.image.load("Textures/StopButton.png").convert_alpha(),
                                  scale=0.5)
        self.start_flag = False
        self.is_config = True
        finished = False

        while not finished:

            if not self.start_flag:
                if self.start_button.is_pressed(screen):
                    print("Game starts!")
                    self.level += 1  # FIXME: тестовая штука, потом изменится обязательно!
                    self.start_flag = True

            if self.start_flag:
                if self.is_config:
                    cur_level = Level(level=self.level, screen=screen)
                    self.is_config = False
                else:
                    cur_level.draw()


            for our_event in pygame.event.get():
                if our_event.type == pygame.QUIT:
                    finished = True
                elif our_event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                else:
                    pass  # FIXME: self.level выбирается на пользовательском интерфейсе

            for elem in self.towers:
                elem.check_cause()

            if self.stop_button.is_pressed(screen):
                finished = True

            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()


gggg = Game()
